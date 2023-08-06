import json
import os

from base64 import b64encode
from pathlib import Path
from typing import Dict, List

from .constants import PIPELINE_ENV_VAR, PIPELINE_INPUT_ATTR, PIPELINE_NAME_ATTR
from .pfs import PFS
from .utils import expand_include, get_entrypoint, package_inclusions, script_to_module


def convert_to_specification(script: os.PathLike, image: str, include: List[Path]) -> Dict:
    inclusions = expand_include(include)
    pipeline_source = script_to_module(script, inclusions)
    entrypoint = get_entrypoint(pipeline_source.module)
    encoded_source = b64encode(pipeline_source.script)
    encoded_original = b64encode(pipeline_source.original)

    include_tar = b64encode(package_inclusions(inclusions))

    pipeline_name = getattr(entrypoint, PIPELINE_NAME_ATTR)
    name = dict(name=pipeline_name) if pipeline_name is not None else {}
    pipeline_input = getattr(entrypoint, PIPELINE_INPUT_ATTR)
    if isinstance(pipeline_input, PFS):
        pipeline_input = dict(pfs=pipeline_input.serialize())

    return dict(
        pipeline=name,
        input=pipeline_input,
        transform=dict(
            cmd=["python3", "-m", "script_to_pipeline.entrypoint", encoded_source.decode(), include_tar.decode()],
            image=image,
            env={PIPELINE_ENV_VAR: "True"},
        ),
        metadata=dict(
            annotations=dict(
                encoded_source=encoded_original.decode(),
            ),
        )
    )


def write_pipeline(pipeline: os.PathLike, specification: Dict) -> None:
    pipeline = Path(pipeline)
    if not pipeline.exists():
        payload = dict(
            pipeline=dict(name=pipeline.stem),
            description="",
            input=dict(),
        )
    else:
        try:
            payload = json.loads(pipeline.read_bytes())
        except json.decoder.JSONDecodeError:
            raise RuntimeError(f"Could not read file: {pipeline}")
    if specification["pipeline"]:
        payload["pipeline"] = specification["pipeline"]
    if specification["input"]:
        payload["input"] = specification["input"]
    payload["transform"] = specification["transform"]
    payload["metadata"] = specification["metadata"]
    try:
        with pipeline.open("w") as file:
            json.dump(payload, file, indent=2)
    except IOError as err:
        raise RuntimeError(
            f"Could not create file: {pipeline}"
        ) from err
    return

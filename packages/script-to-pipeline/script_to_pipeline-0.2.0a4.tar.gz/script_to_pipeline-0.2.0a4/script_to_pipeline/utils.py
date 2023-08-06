import json
import os
import sys
import tarfile

from contextlib import redirect_stdout
from io import BytesIO
from inspect import getfullargspec, getmembers, isfunction
from importlib import import_module
from pathlib import Path
from shutil import rmtree
from subprocess import run
from tempfile import TemporaryDirectory, NamedTemporaryFile
from types import ModuleType
from typing import Callable, Iterable, List, Optional
from urllib.parse import urlparse

from .constants import ENTRYPOINT_ATTR, PIPELINE_ENV_VAR
from .models import PipelineSource
from .pfs import PFS


def in_container() -> bool:
    return bool(os.environ.get(PIPELINE_ENV_VAR))


def is_entrypoint(func: Callable) -> bool:
    return hasattr(func, ENTRYPOINT_ATTR)


def is_remote_location(location: str) -> bool:
    try:
        result = urlparse(location)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def nbconvert(notebook: bytes) -> bytes:
    command = [
        "jupyter-nbconvert",
        "--stdin",
        "--stdout",
        "--to=python",
        "--TagRemovePreprocessor.enabled=True",
        "--TagRemovePreprocessor.remove_cell_tags=pachyderm-ignore"
    ]
    result = run(command, capture_output=True, input=notebook)
    return result.stdout


def script_to_module(location: os.PathLike, inclusions: List[Path]) -> PipelineSource:

    location = Path(location)
    original = source = location.read_bytes()
    if location.suffix == ".ipynb":
        source = nbconvert(original)

    module_name = "__pipeline_script"
    with TemporaryDirectory() as tempdir:
        test_script = Path(tempdir, f"{module_name}.py")
        test_script.write_bytes(source)
        for inclusion in inclusions:
            target = Path(tempdir, inclusion)
            target.parent.mkdir(parents=True, exist_ok=True)
            inclusion.link_to(target)
        sys.path.append(tempdir)
        try:
            with open(os.devnull, "w") as devnull:
                with redirect_stdout(devnull):
                    module = import_module(module_name)
            del sys.modules[module_name]
        except ImportError as err:
            raise RuntimeError(
                "Could not import the script. "
                "The script must be entirely self contained. "
                "Are all your dependencies installed? "
            ) from err
        assert sys.path.pop() == tempdir

    pipeline_source = PipelineSource(module, location, original, source)
    return pipeline_source


def get_entrypoint(module: ModuleType) -> Callable:
    """Returns the only function within the specified module marked with the
    @pipeline decorator.

    Args:
        module: The module to search.

    Raises:
        RuntimeError: If none or multiple entrypoints are found.

    Returns:
        Entrypoint function to the pipeline.
    """
    entrypoints = [
        func for _name, func in getmembers(module, isfunction)
        if is_entrypoint(func)
    ]
    if not entrypoints:
        raise RuntimeError(
            "No entrypoints found. "
            "Did you mark a function with the @pipeline decorator?"
        )
    if len(entrypoints) > 1:
        raise RuntimeError(
            "Multiple entrypoints found. "
            "Please only mark a single function with the @pipeline decorator."
        )
    return entrypoints[0]


def expand_include(include: Iterable[Path]) -> List[Path]:
    inclusions = set()
    for path in include:
        if path.is_dir():
            inclusions.update(expand_include(path.rglob("*")))
        else:
            inclusions.add(path)
    return list(inclusions)


def package_inclusions(inclusions: List[Path]) -> bytes:
    io_bytes = BytesIO()
    total_size = 0
    with tarfile.open(fileobj=io_bytes, mode="w:gz") as tar:
        for inclusion in inclusions:
            info = tarfile.TarInfo(str(inclusion))
            info.size = inclusion.stat().st_size
            total_size += info.size
            with inclusion.open("rb") as file:
                tar.addfile(info, file)
            if total_size > 102400:
                raise RuntimeError(
                    f"Cannot include more than 100KB of extra files. Attempted to include: {inclusions}"
                )
    io_bytes.seek(0)
    return io_bytes.read()


def create_test_datum(pipeline_function: Callable, pipeline_input: Optional[PFS]) -> Callable:

    if pipeline_input is None:
        def no_input_error(*args, **kwargs):
            raise RuntimeError(
                "Cannot run \"test_datum\" method. "
                "No PFS input was specified within the \"pipeline\" declaration. "
            )
        return no_input_error

    def test_datum(output_dir: Optional[os.PathLike] = None, **kwargs) -> None:
        signature = getfullargspec(pipeline_function)
        if "out" not in signature.args:
            raise RuntimeError(
                "Expected argument \"out\" to pipeline function. "
                "This argument must be provided to use the \"test_datum\" function. "
            )
        if "datum" not in signature.args:
            raise RuntimeError(
                f"Expected argument \"datum\" to the pipeline function. "
                "This argument must be provided to use the \"test_datum\" function. "
            )
        mount_path = pipeline_input.mount_path
        if not mount_path.exists():
            raise NotADirectoryError(
                f"Expected {mount_path} to exist. "
            )

        output_dir = mount_path.parent.joinpath("out") if not output_dir else Path(output_dir)
        if output_dir.exists():
            rmtree(output_dir)
        output_dir.mkdir()

        list_datum_spec = output_dir.joinpath(".datum-spec.json")
        list_datum_spec.write_text(json.dumps(
            dict(input=dict(pfs=pipeline_input.serialize()))
        ))
        output = run(["pachctl", "list", "datum", "--file", list_datum_spec], capture_output=True)

        for line in output.stdout.splitlines()[1:]:
            _, datum, *__ = line.split()
            datum_path = datum.decode().split(":/")[1]
            datum_file = mount_path.joinpath(datum_path)
            print(f"Testing pipeline with datum: {datum_file}")
            if datum_file.exists():
                return pipeline_function(datum=datum_file, out=output_dir, **kwargs)

        raise RuntimeError("No datums found locally")

    return test_datum

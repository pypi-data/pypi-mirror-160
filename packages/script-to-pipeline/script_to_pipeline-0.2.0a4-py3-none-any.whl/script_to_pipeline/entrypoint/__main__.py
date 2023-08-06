import sys
import tarfile

from base64 import b64decode
from importlib import import_module
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from script_to_pipeline.utils import get_entrypoint


if __name__ == "__main__":
    if len(sys.argv) > 1:

        source = b64decode(sys.argv[1])
        with TemporaryDirectory() as tempdir:
            Path(tempdir, "script.py").write_bytes(source)
            if len(sys.argv) > 2:
                include_tar = BytesIO(b64decode(sys.argv[2]))
                with tarfile.open(fileobj=include_tar, mode="r:gz") as tar:
                    tar.extractall(tempdir)

            sys.path.append(tempdir)
            script = import_module("script")
            try:
                entrypoint = get_entrypoint(script)
            except RuntimeError:
                print("WARNING: No entrypoint found.")
            else:
                entrypoint()
    else:
        print("nothing to run")

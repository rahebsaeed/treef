# treef/builder.py
from pathlib import Path
from . import exceptions
import logging 

log = logging.getLogger("treef")


def build_structure(structure, root_dir):
    """
    Creates the files and folders from the parsed structure in two passes:
    1. Create all directories.
    2. Create all files.
    This is more efficient and prevents errors where a file is created
    before its parent directory exists.
    """
    root = Path(root_dir)

    # --- Pass 1: Create all directories ---
    log.debug("Creating directories...")
    dirs_to_create = [item for item in structure if item['type'] == 'dir']
    for item in dirs_to_create:
        path = root / item['path']
        try:
            path.mkdir(parents=True, exist_ok=True)
            log.debug(f"Created directory: {path}")
        except OSError as e:
            raise exceptions.BuildError(f"Failed to create directory '{path}': {e}")

    # --- Pass 2: Create all files ---
    log.debug("Creating files...")
    files_to_create = [item for item in structure if item['type'] == 'file']
    for item in files_to_create:
        path = root / item['path']
        try:
            # The parent directory is guaranteed to exist from the first pass.
            path.touch()
            log.debug(f"Created file: {path}")
        except OSError as e:
            raise exceptions.BuildError(f"Failed to create file '{path}': {e}")
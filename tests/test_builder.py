import pytest
from pathlib import Path
from treef import builder

# A pytest "fixture" that provides a clean, temporary directory for each test
@pytest.fixture
def tmp_path(tmpdir):
    return Path(str(tmpdir))

def test_builder_creates_structure(tmp_path):
    """
    Tests if the builder can correctly create a nested structure of files and folders.
    """
    # 1. Arrange: Define the input structure and the root directory for the test
    structure_to_build = [
        {'path': 'src', 'type': 'dir'},
        {'path': 'src/api', 'type': 'dir'},
        {'path': 'src/api/auth.js', 'type': 'file'},
        {'path': 'src/app.js', 'type': 'file'},
        {'path': 'package.json', 'type': 'file'},
    ]

    # 2. Act: Run the function we are testing
    builder.build_structure(structure_to_build, root_dir=tmp_path)

    # 3. Assert: Check if the files and directories actually exist on the filesystem
    assert (tmp_path / "src").is_dir()
    assert (tmp_path / "src" / "api").is_dir()
    assert (tmp_path / "src" / "api" / "auth.js").is_file()
    assert (tmp_path / "src" / "app.js").is_file()
    assert (tmp_path / "package.json").is_file()

def test_builder_empty_structure(tmp_path):
    """
    Tests if the builder does nothing and does not error on an empty structure list.
    """
    # 1. Arrange
    empty_structure = []

    # 2. Act
    builder.build_structure(empty_structure, root_dir=tmp_path)

    # 3. Assert: Check that nothing was created
    # list(tmp_path.iterdir()) will list all items in the directory
    assert len(list(tmp_path.iterdir())) == 0
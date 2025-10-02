# tests/test_parser.py
import pytest
from pathlib import Path
from treef import parser, exceptions
import os

@pytest.fixture
def tmp_path(tmpdir) -> Path:
    """A pytest fixture that provides a modern pathlib.Path object for a temporary directory."""
    return Path(str(tmpdir))

def test_parser_valid_tree(tmp_path):
    """
    Tests if the parser can correctly process a standard, valid tree string.
    """
    tree_content = """
    # This is a comment, it should be ignored
    /src
        ├── /api
        │   └── auth.js
        └── app.js
    .gitignore
    """
    expected_structure = [
        {'path': 'src', 'type': 'dir'},
        {'path': os.path.join('src', 'api'), 'type': 'dir'},
        {'path': os.path.join('src', 'api', 'auth.js'), 'type': 'file'},
        {'path': os.path.join('src', 'app.js'), 'type': 'file'},
        {'path': '.gitignore', 'type': 'file'},
    ]

    # --- FIX: Write the temporary file with UTF-8 encoding ---
    fake_tree_file = tmp_path / "project.tree"
    fake_tree_file.write_text(tree_content, encoding='utf-8')

    result = parser.parse_tree_file(str(fake_tree_file))

    assert set(tuple(d.items()) for d in result) == set(tuple(d.items()) for d in expected_structure)

def test_parser_malformed_line_raises_error(tmp_path):
    """
    Tests if the parser correctly raises a ParsingError for a bad line.
    """
    malformed_content = """
    /src
        -- this-line-is-wrong.js
    """
    # --- FIX: Write the temporary file with UTF-8 encoding ---
    fake_tree_file = tmp_path / "bad.tree"
    fake_tree_file.write_text(malformed_content, encoding='utf-8')

    with pytest.raises(exceptions.ParsingError) as excinfo:
        parser.parse_tree_file(str(fake_tree_file))

    assert "Malformed line 3" in str(excinfo.value)
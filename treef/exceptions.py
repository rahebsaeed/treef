class TreefError(Exception):
    """Base exception for all errors raised by treef."""
    pass

class FileDiscoveryError(TreefError):
    """Raised when there's an issue finding the .tree file."""
    pass

class ParsingError(TreefError):
    """Raised for syntax errors within the .tree file."""
    pass

class BuildError(TreefError):
    """Raised when file/folder creation fails."""
    pass

class FileRenameError(TreefError):
    """Raised when the final rename operation fails."""
    pass
# treef/parser.py
import os
import re
from . import exceptions

def parse_tree_file(file_path):
    """
    Parses a .tree file into a list of nodes, each with a full path and type.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except IOError as e:
        raise exceptions.ParsingError(f"Cannot read file '{file_path}': {e}")

    parsed_structure = []
    path_stack = []
    level_stack = [-1]

    # This regex is now simpler: it just separates the prefix from the name.
    # The prefix is any combination of tree chars and spaces at the start.
    # The name is everything after that.
    line_regex = re.compile(r'^(?P<prefix>[│\s├─└]*)(?P<name>.*)')

    for line_num, line in enumerate(lines, 1):
        line = line.rstrip()
        if not line.strip():
            continue

        content = line.split('#', 1)[0].rstrip()
        if not content:
            continue

        match = line_regex.match(content)
        prefix = match.group('prefix')
        name = match.group('name')


        # 1. Validate the name. It cannot be empty or start with invalid characters.
        if not name.strip() or name.startswith('-'):
            raise exceptions.ParsingError(
                f"Malformed line {line_num}: Invalid name or structure in '{line}'"
            )

        # 2. Validate the prefix structure. The last non-space character must be a valid tree connector.
        stripped_prefix = prefix.rstrip()
        if stripped_prefix and not stripped_prefix.endswith(('├──', '└──', '│', '├', '└')):
             raise exceptions.ParsingError(
                f"Malformed line {line_num}: Invalid tree structure characters in '{line}'"
            )

        
        indentation = len(prefix)
        name = name.lstrip() 

        if name.startswith('/') or name.endswith('/'):
            node_type = 'dir'
            clean_name = name.strip('/').strip()
        else:
            node_type = 'file'
            clean_name = name

        if not clean_name:
             raise exceptions.ParsingError(
                f"Malformed line {line_num}: Missing name after prefix in '{line}'"
            )

        while indentation <= level_stack[-1]:
            path_stack.pop()
            level_stack.pop()

        full_path = os.path.join(*path_stack, clean_name)
        parsed_structure.append({'path': full_path, 'type': node_type})

        if node_type == 'dir':
            path_stack.append(clean_name)
            level_stack.append(indentation)

    if not parsed_structure:
        raise exceptions.ParsingError("The .tree file is empty or contains no valid structure.")
        
    return parsed_structure
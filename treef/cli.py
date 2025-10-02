# treef/cli.py
import click
import os
import time
import logging
from . import parser, builder, exceptions, logger

# Configure the logger ONCE when the application starts.
logger.configure_logger()

# Get the logger instance for use in this file.
log = logging.getLogger("treef")


# --- START OF MODIFICATION 1: Update find_tree_file ---
def find_tree_file(directory):
    """
    Scans the directory for .tree files.
    - If one is found, returns its path as a string.
    - If multiple are found, returns a sorted list of their paths.
    - If none are found, raises FileDiscoveryError.
    """
    tree_files = [f for f in os.listdir(directory) if f.endswith('.tree')]
    
    if not tree_files:
        raise exceptions.FileDiscoveryError("No .tree file found in this directory.")
    
    if len(tree_files) == 1:
        return tree_files[0]  # Return the single file path
    
    return sorted(tree_files)  # Return the list of multiple files
# --- END OF MODIFICATION 1 ---


# --- START OF MODIFICATION 2: Add a new function for user choice ---
def prompt_for_choice(options):
    """
    Given a list of file options, prints them and prompts the user to choose one.
    Returns the chosen filename or None if the user cancels.
    """
    click.echo(click.style("Multiple .tree files found. Please choose one to process:", fg="yellow"))
    
    for i, option in enumerate(options, 1):
        click.echo(f"  {click.style(str(i), fg='green')}: {option}")
    
    while True:
        choice = click.prompt(click.style("Enter the number of the file to use (or 'q' to quit)", bold=True), type=str, default="", show_default=False)
        
        if choice.lower() == 'q':
            return None
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                # Adjust for 0-based index
                return options[choice_num - 1]
            else:
                click.echo(click.style(f"Error: Please enter a number between 1 and {len(options)}.", fg="red"), err=True)
        except ValueError:
            click.echo(click.style("Error: Invalid input. Please enter a number.", fg="red"), err=True)
# --- END OF MODIFICATION 2 ---


@click.command()
@click.option('--verbose', is_flag=True, help="Enable detailed debug logging.")
def main(verbose):
    """
    Scaffolds a project directory from a .tree file.
    """
    if verbose:
        log.setLevel(logging.DEBUG)

    start_time = time.time()
    log.info("Starting treef...")
    tree_file_path = None

    try:
        # This part of the try block remains the same
        found_item = find_tree_file('.')
        
        if isinstance(found_item, list):
            tree_file_path = prompt_for_choice(found_item)
            if not tree_file_path:
                log.warning("Selection cancelled by user. Aborting.")
                return
        else:
            tree_file_path = found_item

        log.info(f"Processing tree definition file: {tree_file_path}")
        structure = parser.parse_tree_file(tree_file_path)
        final_filename = os.path.splitext(tree_file_path)[0] + '.treef'
        for item in structure:
            if os.path.normpath(item['path']) == os.path.normpath(final_filename):
                raise exceptions.BuildError(
                    f"Validation Error: The definition file '{tree_file_path}' "
                    f"cannot contain its own final name ('{final_filename}'). "
                    "Please remove this line from the file."
                )
        builder.build_structure(structure, root_dir='.')
        processed_file_path = rename_to_processed(tree_file_path)
        log.debug(f"Renamed '{tree_file_path}' to '{processed_file_path}'")

    # --- START OF THE ENHANCEMENT ---
    except exceptions.TreefError as e:
        # Check if this is the specific "file not found" error
        if isinstance(e, exceptions.FileDiscoveryError):
            log.error(str(e)) # Log the simple error message
            
            # Use click.echo to provide styled, actionable guidance
            click.echo("\n" + click.style("💡 To get started, create a file with a .tree extension (e.g., 'project.tree').", bold=True))
            click.echo(click.style("Here is an example of what you can put inside it:", fg="yellow"))
            
            example_text = """
    # This is a comment. Lines starting with # are ignored.

    /src
        ├── /components
        ├── /utils
        └── main.js
    /tests
    README.md
    package.json
            """
            click.echo(example_text)
        else:
            # For all other controlled errors (ParsingError, BuildError, etc.), use the old behavior
            log.error(f"A controlled error occurred: {e}")
            if tree_file_path:
                log.error(f"Please check the contents of '{tree_file_path}' for errors.")
        return # Exit gracefully
    # --- END OF THE ENHANCEMENT ---
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}", exc_info=verbose)
        return

    end_time = time.time()
    log.info(f"Successfully built project in {end_time - start_time:.2f} seconds.")

# The rename_to_processed function and the rest of the file remain the same...
def rename_to_processed(file_path):
    """Renames a .tree file to .treef."""
    base_name = os.path.splitext(file_path)[0]
    new_path = f"{base_name}.treef"
    if os.path.exists(new_path):
        raise exceptions.FileRenameError(f"Cannot rename to '{new_path}' because it already exists.")
    os.rename(file_path, new_path)
    return new_path

if __name__ == '__main__':
    main()
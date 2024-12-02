import os

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource file, given its relative path from the project root.
    """
    # Get the absolute path to the project root directory (two levels up from this file)
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

    # Construct the absolute path to the resource
    abs_path = os.path.normpath(os.path.join(project_root, relative_path))

    return abs_path

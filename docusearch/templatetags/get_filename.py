import os
from django_jinja import library


@library.global_function
def get_filename(filepath):
    """
    Parses the filename from a document path if no filepath present returns
    `Document`
    """
    if filepath:
        return os.path.basename(filepath)

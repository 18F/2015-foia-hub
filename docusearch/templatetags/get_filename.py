import os
from django_jinja import library


@library.global_function
def get_filename(filepath):
    """ Parses the filename from a document path """
    return os.path.basename(filepath)

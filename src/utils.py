import os


def is_valid_file(parser, file):
    if not os.path.exists(file):
        parser.error(f"File {file} does not exist!")
    else:
        return file

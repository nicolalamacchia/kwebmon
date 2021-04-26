import os


def fixture_path(fixture_file):
    return os.path.join(
        os.path.join(os.path.dirname(__file__), "fixtures"),
        fixture_file
    )

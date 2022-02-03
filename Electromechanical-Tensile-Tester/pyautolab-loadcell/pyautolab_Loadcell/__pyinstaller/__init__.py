def get_hook_dirs():
    """Hook method for pyinstaller."""
    from pathlib import Path

    package_folder = Path(__file__).parent
    return [str(package_folder.absolute())]

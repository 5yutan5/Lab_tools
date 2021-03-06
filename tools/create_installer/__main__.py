"""Module allowing for `python -m tools.create_installer`."""
import argparse
import inspect
import platform
import shutil
import subprocess  # nosec
import tarfile
from pathlib import Path

import PyInstaller.__main__ as pyinstaller  # noqa: N813
from PyInstaller import DEFAULT_DISTPATH
from rich.console import Console

import tools

PROJECT_ROOT_PATH = Path(inspect.getfile(tools)).parents[1]
_console = Console(force_terminal=True)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="This program generates resources for Qt Applications.")
    parser.add_argument(
        "main_script_path",
        type=Path,
        help="Main script path for application.",
    )
    parser.add_argument(
        "-n",
        "--name",
        help="Application name.",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Application version",
        default=None,
    )
    return parser.parse_args()


def _create_app(main_script_path: Path, dist_path: Path, title: str) -> Path:
    commands = ["--clean", "-y", str(main_script_path), "-n", title]
    if platform.system() == "Darwin":
        commands.append("--windowed")
    pyinstaller.run(commands)
    dir_app_path = dist_path / (f"{title}.app" if platform.system() == "Darwin" else title)
    if not dir_app_path.exists():
        raise FileNotFoundError(f"Cannot find {title} executable") from None
    if not dir_app_path.is_dir():
        raise NotADirectoryError(f"{dir_app_path} is not a directory")
    if platform.system() == "Darwin":
        shutil.rmtree(Path(DEFAULT_DISTPATH) / title)
    return dir_app_path


def _output_tar(target_dir_path: Path, tar_file_name: str) -> None:
    tarfile_path = Path(DEFAULT_DISTPATH) / f"{tar_file_name}.tar.gz"
    if tarfile_path.exists():
        _console.log("Removing previous tar file...")
        tarfile_path.unlink()
    with tarfile.open(tarfile_path.as_posix(), "w:gz") as tar:
        tar.add(target_dir_path, target_dir_path.name)


def _output_zip(target_dir_path: Path, archive_name: str) -> None:
    archive_path = target_dir_path.parent / archive_name
    if archive_path.exists():
        _console.log("Removing previous zip file...")
        archive_path.unlink()
    shutil.make_archive(archive_path.as_posix(), "zip", target_dir_path.parent, target_dir_path.name)


def _create_dmg(target_dir_path: Path, dmg_file_name: str, license_path: Path) -> None:
    dmg_path = Path(DEFAULT_DISTPATH) / f"{dmg_file_name}-installer.dmg"
    options = {
        "--volname": f"{dmg_file_name}-Installer",
        "--window-pos": (200, 120),
        "--window-size": (411, 201),
        "--icon-size": 100,
        "--icon": (target_dir_path.name, 40, 50),
        "--app-drop-link": (220, 50),
        "--format": "UDBZ",
        "--eula": license_path.relative_to(Path.cwd()),
    }

    if dmg_path.exists():
        _console.log("Removing previous installer...")
        dmg_path.unlink()

    commands = ["create-dmg"]
    for option, values in options.items():
        commands.append(str(option))
        if type(values) is not tuple:
            commands.append(str(values))
            continue
        for value in values:
            commands.append(str(value))
    commands.append(dmg_path.relative_to(Path.cwd()).as_posix())
    commands.append(target_dir_path.relative_to(Path.cwd()).as_posix())
    subprocess.run(commands)


def _create_windows_installer(target_dir_path: Path, installer_name: str, license_path: Path) -> None:
    template_nsi_path = Path(__file__).parent / "template.nsi"
    nsi_text = template_nsi_path.read_text()
    nsi_text = (
        nsi_text.replace("$${app_name}", target_dir_path.name)
        .replace("$${exe_name}", target_dir_path.name)
        .replace("$${installer_path}", f"{Path(DEFAULT_DISTPATH) / installer_name}-installer.exe")
        .replace("$${license_path}", str(license_path))
    )
    _console.print("Generated NSI script------")
    _console.print(nsi_text)
    _console.print("--------------------------")
    _console.log("Creating nsi file...")

    temp_nis_path = PROJECT_ROOT_PATH / "install.nsi"
    temp_nis_path.write_text(nsi_text)
    subprocess.run(["makensis", "install.nsi"])
    temp_nis_path.unlink()


def _main() -> None:
    args = _parse_args()
    main_script_path: Path = args.main_script_path
    title: str = args.name
    version: str | None = args.version

    _console.log("Creating application...")
    app_path = _create_app(main_script_path, Path(DEFAULT_DISTPATH), title)
    license_file_path = PROJECT_ROOT_PATH / "tools" / "create_installer" / "LICENSE.txt"
    output_file_name = f"{title}-none" if version is None else f"{title}-{version}"

    _console.log("Archiving the application folder...")
    if platform.system() == "Darwin":
        _output_tar(app_path, output_file_name)
    elif platform.system() == "Windows":
        _output_zip(app_path, output_file_name)

    _console.log("Creating installer...")
    if platform.system() == "Darwin":
        _create_dmg(app_path, output_file_name, license_file_path)
    elif platform.system() == "Windows":
        _create_windows_installer(app_path, output_file_name, license_file_path)

    _console.log(f"Removing the {title} application folder...")
    shutil.rmtree(app_path)
    _console.log("Build finished successfully!", style="green")


if __name__ == "__main__":
    _main()

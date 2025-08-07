from pathlib import Path
from quingo.core.quingo_logger import quingo_err, quingo_info
import quingo.global_config as gc
import distutils.spawn
import requests
import json


def get_text(link):
    r = requests.get(link)
    return r.text


def set_compiler_path(path_str):
    path = Path(path_str)
    if path_str.startswith("~"):
        path = path.expanduser()
    if not path.exists():
        quingo_err("cannot find the compiler at {}".format(path_str))
        return False

    path_file = gc.mlir_compiler_config_path

    with path_file.open("w") as f:
        f.write(str(path))

    return True


def download_latest_quingoc():
    latest_release_url = (
        "https://gitee.com/api/v5/repos/{owner}/{repo}/releases/latest".format(
            owner="quingo", repo="quingoc-release"
        )
    )

    try:
        latest_release = get_text(latest_release_url)
        release_info = json.loads(latest_release)
        assets = release_info["assets"]
        quingoc_asset = None
        for asset in assets:
            if "name" in asset and asset["name"].startswith("quingoc"):
                quingoc_asset = asset
                break
        if quingoc_asset is None:
            quingo_err("failed to download quingoc from gitee.")
            return False

        quingoc_url = (
            quingoc_asset["browser_download_url"] + "/" + quingoc_asset["name"]
        )
        quingoc_response = requests.get(quingoc_url)

    except Exception as e:
        raise RuntimeError(
            "Failed to parse information retrieved from gitee with the "
            "following error: {}".format(e)
        )

    with gc.default_mlir_compiler_path.open("wb") as f:
        f.write(quingoc_response.content)

    gc.default_mlir_compiler_path.chmod(0o744)

    return True


def retrieve_compiler_path_from_file(config_file):
    compiler_path = None
    with config_file.open("r") as f:
        compiler_path = f.read()
        if not Path(compiler_path).exists():
            quingo_err("The compiler path is incorrect: {}".format(compiler_path))
            return None
    return compiler_path


def get_mlir_path():
    if gc.mlir_compiler_config_path.exists():
        read_path = retrieve_compiler_path_from_file(gc.mlir_compiler_config_path)
        if read_path is not None:
            return read_path

    # failed to read the path from the file, find the compiler executable from default path
    quingoc_path = distutils.spawn.find_executable(
        "quingoc", str(gc.default_mlir_compiler_path.parent)
    )
    if quingoc_path is not None:
        return quingoc_path

    # find the compiler executable from the system directly
    quingoc_path = distutils.spawn.find_executable("quingoc")

    if quingoc_path is None:
        quingo_info(
            "Cannot find the compiler.\n"
            "  To resolve this problem, you can install quingoc with two ways:\n"
            '  1. run the following command "python -m quingo.install_quingoc"\n'
            "  2. Download quingoc from https://gitee.com/quingo/quingoc-release/"
            "releases and save it at a directory in the system path \n"
            "or configure its path by calling this method inside python:\n"
            "     `quingo.set_mlir_compiler_path(<path-to-quingoc>)`"
        )
        raise RuntimeError(
            "Cannot find the mlir-based quingoc compiler in the system path."
        )

    return quingoc_path


def set_mlir_compiler_path(mlir_path_str):
    set_compiler_path(mlir_path_str, True)

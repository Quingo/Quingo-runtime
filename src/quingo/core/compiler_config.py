from pathlib import Path
from .utils import quingo_err
import quingo.global_config as gc
import distutils.spawn
import requests
import json


def get_text(link):
    r = requests.get(link)
    return r.text


def set_compiler_path(path_str, is_mlir=False):
    path = Path(path_str)
    if path_str.startswith('~'):
        path = path.expanduser()
    if not path.exists():
        quingo_err("cannot find the compiler at {}".format(path_str))
        return False

    if is_mlir:
        path_file = gc.mlir_compiler_config_path
    else:
        path_file = gc.xtext_compiler_config_path

    with path_file.open('w') as f:
        f.write(str(path))

    return True


def download_latest_quingoc():
    latest_release_url = "https://gitee.com/api/v5/repos/{owner}/{repo}/releases/latest".format(
        owner="quingo", repo="quingoc-release")

    try:
        latest_release = get_text(latest_release_url)
        release_info = json.loads(latest_release)
        assets = release_info['assets']
        quingoc_asset = None
        for asset in assets:
            if 'name' in asset and asset['name'].startswith('quingoc'):
                quingoc_asset = asset
                break
        if quingoc_asset is None:
            quingo_err("failed to download quingoc from gitee.")
            return False

        quingoc_url = quingoc_asset['browser_download_url'] + \
            '/' + quingoc_asset['name']
        quingoc_response = requests.get(quingoc_url)

    except Exception as e:
        raise RuntimeError("Failed to parse information retrieved from gitee with the "
                           "following error: {}".format(e))

    with gc.default_mlir_compiler_path.open('wb') as f:
        f.write(quingoc_response.content)

    gc.default_mlir_compiler_path.chmod(0o744)

    return True


def retrieve_compiler_path_from_file(config_file):
    compiler_path = None
    with config_file.open('r') as f:
        compiler_path = f.read()
        if not Path(compiler_path).exists():
            quingo_err(
                "The compiler path is incorrect: {}".format(compiler_path))
            return None
    return compiler_path


def get_mlir_path():
    if gc.mlir_compiler_config_path.exists():
        read_path = retrieve_compiler_path_from_file(
            gc.mlir_compiler_config_path)
        if read_path is not None:
            return read_path

    # failed to read the path from the file, find the compiler executable from default path
    quingoc_path = distutils.spawn.find_executable(
        'quingoc', str(gc.default_mlir_compiler_path.parent))
    if quingoc_path is not None:
        return quingoc_path

    # find the compiler executable from the system directly
    quingoc_path = distutils.spawn.find_executable('quingoc')
    return quingoc_path


def get_xtext_path():
    if not gc.xtext_compiler_config_path.exists():
        quingo_err('cannot find the file specifying the xtext compiler path.')
        return None
    return retrieve_compiler_path_from_file(gc.xtext_compiler_config_path)


def set_xtext_compiler_path(xtext_path_str):
    set_compiler_path(xtext_path_str, False)


def set_mlir_compiler_path(mlir_path_str):
    set_compiler_path(mlir_path_str, True)

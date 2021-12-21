import requests
import json
import distutils.spawn
import subprocess
from pathlib import Path
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

def download_latest_quingoc():
    
    latest_release_url = "https://gitee.com/api/v5/repos/{owner}/{repo}/releases/latest".format(
        owner = "hpcl_quanta", repo = "quingo-runtime")

    try:
        latest_release = requests.get(latest_release_url).text
        release_info = json.loads(latest_release)
        assets = release_info['assets']
        quingoc_asset = None
        for asset in assets:
            if 'name' in asset and asset['name'].startswith('quingo-c'):
                quingoc_asset = asset
                break
        if quingoc_asset is None:
            raise RuntimeError("ailed to download quingoc from giteeF. ")

        quingoc_url = quingoc_asset['browser_download_url'] + '/' + quingoc_asset['name']
        quingoc_response = requests.get(quingoc_url)

        mlir_compiler_path = Path.home() / 'quingo-compiler'
        with mlir_compiler_path.open('wb') as f:
            f.write(quingoc_response.content)

        mlir_compiler_path.chmod(0o744)

    except Exception as e:
        raise RuntimeError("Failed to parse information retrieved from gitee with the "
                           "following error: {}".format(e))

    quingoc_install_prefix = ' --prefix=/usr/local'
    quingoc_install_extra_option = ' --exclude-subdir'
    quingoc_install_cmd = 'sudo '+ str(mlir_compiler_path) + quingoc_install_prefix + quingoc_install_extra_option

    ret_value = subprocess.run(quingoc_install_cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,text = True, shell = True)

    if(ret_value.returncode != 0):
        raise RuntimeError("Failed to install lastest quingo compiler with the"
                           "following error: {}".format(ret_value.stderr))
    
    mlir_compiler_path.unlink()

def friendly(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.

    It modifies the run() method so that it prints a friendly greeting.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        quingoc_path = distutils.spawn.find_executable('quingoc')
        print("quingoc path: {}".format(quingoc_path))
        if quingoc_path is None:
            download_latest_quingoc()

        orig_run(self)

    command_subclass.run = modified_run
    return command_subclass


@friendly
class CustomDevelopCommand(develop):
    pass


@friendly
class CustomInstallCommand(install):
    pass


setup(cmdclass={
    'install': CustomInstallCommand,
    'develop': CustomDevelopCommand,})

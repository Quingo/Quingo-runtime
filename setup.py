import requests
import json
import distutils.spawn
import subprocess
import platform
import zipfile
import shutil
from pathlib import Path
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def set_path_env_on_Linux(install_path):
    """Set path environment to contain the milr quingo compiler on Linux.
    """
   
    shell_cmd = "if [-f \"{}\"]\nthen\n \
                    echo 'export PATH={}:$PATH' >> {}\n \
                elif [-f \"{}\"]\nthen\n \
                    echo 'export PATH={}:$PATH' >> {}\n \
                else\n \
                    echo 'export PATH={}:$PATH' >> {}\n \
                fi\n"

    mlir_compiler_execute_path = install_path / 'bin'

    bash_profile = Path.home() / '.bash_profile'
    bashrc = Path.home() / '.bashrc'

    set_env_cmd = shell_cmd.format(bashrc,mlir_compiler_execute_path,bashrc,bash_profile,mlir_compiler_execute_path,bash_profile,mlir_compiler_execute_path,bashrc)

    ret_value = subprocess.run(set_env_cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,text = True, shell = True)

    if(ret_value.returncode != 0):
        raise RuntimeError("Failed add \"{}\" to path environment with the"
                           "following error: {}".format(mlir_compiler_execute_path,ret_value.stderr))
    
    print("Installed mlir quingo compiler at directory:{}".format(mlir_compiler_execute_path))


def install_on_Linux(mlir_compiler_path):
    """Install quingo compiler on Linux.
    """

    mlir_compiler_path.chmod(0o744)

    mlir_compiler_install_path = Path.home() / '.local' 
    mlir_compiler_install_prefix = ' --prefix=' + str(mlir_compiler_install_path)
    mlir_compiler_install_extra_option = ' --exclude-subdir'
    mlir_compiler_install_cmd = str(mlir_compiler_path) + mlir_compiler_install_prefix + mlir_compiler_install_extra_option

    ret_value = subprocess.run(mlir_compiler_install_cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,text = True, shell = True)

    if(ret_value.returncode != 0):
        raise RuntimeError("Failed to install lastest quingo compiler with the"
                           "following error: {}".format(ret_value.stderr))
    
    set_path_env_on_Linux(mlir_compiler_install_path)
    return


def set_path_on_Windows(install_path):
    """Set path environment to contain the milr quingo compiler on Windows.
    """
    # Nothing to do, quingo-runtime will search the default install path
    # Default path is Path.home() / '.quingo'

    return


def install_on_Windows(mlir_compiler_path):
    """Install quingo compiler on Windows.
    """

    mlir_compiler_install_path = Path.home() / '.quingo' 

    zip_file = zipfile.ZipFile(mlir_compiler_path)
    zip_list = zip_file.namelist()
    zip_file.extractall(mlir_compiler_install_path)
    zip_file.close()

    files = [file for file in mlir_compiler_install_path.glob("*/*") if file.is_file()]
    for file in files:
        file.replace(mlir_compiler_install_path / file.name)

    set_path_on_Windows(mlir_compiler_install_path)
    return


def download_and_install_latest_quingoc():
    """Download the latest mlir quingo compiler.
    """

    latest_release_url = "https://gitee.com/api/v5/repos/{owner}/{repo}/releases/latest".format(
        owner = "hpcl_quanta", repo = "quingo-runtime")

    try:
        latest_release = requests.get(latest_release_url).text
        release_info = json.loads(latest_release)
        assets = release_info['assets']
        quingoc_asset = None
        for asset in assets:
            if 'name' in asset and ((asset['name'].endswith('.sh') and platform.system() == 'Linux') 
                                    or (asset['name'].endswith('.zip') and platform.system() == 'Windows')):
                quingoc_asset = asset
                break
        if quingoc_asset is None:
            raise RuntimeError("Failed to download quingo compiler from gitee. ")

        quingoc_url = quingoc_asset['browser_download_url'] + '/' + quingoc_asset['name']
        quingoc_response = requests.get(quingoc_url)

        mlir_compiler_path = Path.home() / 'quingo-compiler'
        with mlir_compiler_path.open('wb') as f:
            f.write(quingoc_response.content)

    except Exception as e:
        raise RuntimeError("Failed to parse information retrieved from gitee with the "
                           "following error: {}".format(e))

    if(platform.system()=='Windows'):
        install_on_Windows(mlir_compiler_path)
    elif(platform.system()=='Linux'):
        install_on_Linux(mlir_compiler_path)
    else:
        raise RuntimeError("Failed to install quingo compiler on {}. Currently supports Windows and Linux.".format(platform.system()))
    
    mlir_compiler_path.unlink()
    return


def friendly(command_subclass):
    """A decorator for classes subclassing one of the setuptools commands.

    It modifies the run() method so that it prints a friendly greeting.
    """
    orig_run = command_subclass.run

    def modified_run(self):
        default_path = Path.home() / '.quingo'
        quingoc_path = distutils.spawn.find_executable('quingoc', str(default_path))
        if quingoc_path is None:
            quingoc_path = distutils.spawn.find_executable('quingoc')

        if quingoc_path is None:
            download_and_install_latest_quingoc()

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

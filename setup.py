import requests
import json
import distutils.spawn
import subprocess
import platform
import zipfile
import shutil
import tempfile
from pathlib import Path
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def set_path_env_on_Linux(install_path):
    """Set path environment to contain the milr quingo compiler on Linux.
    """
    quingoc_dir = install_path / 'bin'

    ret_value = subprocess.run("echo $PATH", stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, shell=True)

    if ret_value.returncode != 0:
        raise RuntimeError("Failed to retrieve system path using 'echo $PATH'.")

    if str(quingoc_dir.absolute()) in ret_value.stdout:
        return

    bash_profile = Path.home() / '.bash_profile'
    bashrc = Path.home() / '.bashrc'
    shell_cmd = "if [-f \"{bashrc_path}\"]\nthen\n \
                    echo 'export PATH={quingoc_dir_path}:$PATH' >> {bashrc_path}\n \
                elif [-f \"{bash_profile_path}\"]\nthen\n \
                    echo 'export PATH={quingoc_dir_path}:$PATH' >> {bash_profile_path}\n \
                fi\n"
    set_env_cmd = shell_cmd.format(
        bashrc_path=bashrc, bash_profile_path=bash_profile, quingoc_dir_path=quingoc_dir)

    ret_value = subprocess.run(set_env_cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, shell=True)

    if(ret_value.returncode != 0):
        raise RuntimeError("Failed add \"{}\" to path environment with the"
                           "following error: {}".format(quingoc_dir, ret_value.stderr))

    print("Installed mlir quingo compiler at directory:{}".format(quingoc_dir))


def install_on_Linux(mlir_compiler_path):
    """Install quingo compiler on Linux.
    """
    mlir_compiler_path.chmod(0o744)
    quingoc_install_dir = Path.home() / '.local'

    mlir_compiler_install_cmd = '"{}" --prefix="{}" --exclude-subdir'.format(
        mlir_compiler_path, quingoc_install_dir)

    print("mlir_compiler_install_cmd: ", mlir_compiler_install_cmd)

    ret_value = subprocess.run(mlir_compiler_install_cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, shell=True)
    if(ret_value.returncode != 0):
        raise RuntimeError("Failed to install lastest quingo compiler with the"
                           "following error: {}".format(ret_value.stderr))

    set_path_env_on_Linux(quingoc_install_dir)


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


def install_compiler(os_name, mlir_compiler_path):
    assert os_name in ['Linux', 'Windows']
    if(os_name == 'Windows'):
        install_on_Windows(mlir_compiler_path)
    if(os_name == 'Linux'):
        install_on_Linux(mlir_compiler_path)


def download_compiler(os_name, tmp_dir_name):
    assert os_name in ['Linux', 'Windows']
    os_dl_suffix = {
        'Linux': '.sh',
        'Windows': '.zip'
    }
    dl_file_suffix = os_dl_suffix[os_name]

    latest_release_url = "https://gitee.com/api/v5/repos/{owner}/{repo}/releases/latest".format(
        owner="hpcl_quanta", repo="quingo-runtime")

    try:
        latest_release = requests.get(latest_release_url).text
        release_info = json.loads(latest_release)
        assets = release_info['assets']
        quingoc_asset = None
        for asset in assets:
            if 'name' in asset and asset['name'].endswith(dl_file_suffix):
                quingoc_asset = asset
                break
        if quingoc_asset is None:
            raise RuntimeError("Failed to download quingo compiler from gitee.")

        quingoc_url = quingoc_asset['browser_download_url'] + '/' + quingoc_asset['name']
        quingoc_response = requests.get(quingoc_url)

        mlir_compiler_path = tmp_dir_name / quingoc_asset['name']
        with mlir_compiler_path.open('wb') as tmp_dl_file:
            num_bytes = tmp_dl_file.write(quingoc_response.content)
            print("installation file has been downloaded to tmp file {} ({} bytes). ".format(
                mlir_compiler_path, num_bytes))
        return mlir_compiler_path

    except Exception as e:
        raise RuntimeError("Failed to parse information retrieved from gitee with the "
                           "following error: {}".format(e))


def download_and_install_latest_quingoc():
    """Download the latest mlir quingo compiler.
    """
    os_name = platform.system()
    if os_name not in ['Linux', 'Windows']:
        raise SystemError("Currently pip installation does not support {}".format(os_name))

    tmp_dir = tempfile.TemporaryDirectory()
    tmp_dir_path = Path(tmp_dir.name)

    mlir_compiler_path = download_compiler(os_name, tmp_dir_path)
    install_compiler(os_name, mlir_compiler_path)

    shutil.rmtree(tmp_dir_path)


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
    'develop': CustomDevelopCommand, })

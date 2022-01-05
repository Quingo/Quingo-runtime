import pathlib
import re
import requests
import json
import distutils.spawn
import subprocess
import platform
import zipfile
import shutil
import tempfile
import datetime
from pathlib import Path

def backup_compiler(quingoc_path):

    backup_path = quingoc_path.parent / "quingoc_backup"

    if not backup_path.exists():
        backup_path.mkdir(exist_ok=True)

    backup_file = quingoc_path.name + \
        datetime.datetime.now().strftime('%F')

    shutil.move(quingoc_path, backup_path/backup_file)


def set_path_env_on_Linux(install_path):
    """Set path environment to contain the milr quingo compiler on Linux.
    """

    ret_value = subprocess.run("echo $PATH", stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, shell=True)

    if ret_value.returncode != 0:
        raise RuntimeError(
            "Failed to retrieve system path using 'echo $PATH'.")

    if str(install_path.absolute()) in ret_value.stdout:
        return

    bash_profile = Path.home() / '.bash_profile'
    bashrc = Path.home() / '.bashrc'
    shell_cmd = "if [ -f \"{bashrc_path}\" ]\nthen\n \
                    echo 'export PATH={quingoc_dir_path}:$PATH' >> {bashrc_path}\n \
                elif [ -f \"{bash_profile_path}\" ]\nthen\n \
                    echo 'export PATH={quingoc_dir_path}:$PATH' >> {bash_profile_path}\n \
                fi\n"
    set_env_cmd = shell_cmd.format(
        bashrc_path=bashrc, bash_profile_path=bash_profile, quingoc_dir_path=install_path)

    ret_value = subprocess.run(set_env_cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, shell=True)

    if(ret_value.returncode != 0):
        raise RuntimeError("Failed add \"{}\" to path environment with the"
                           "following error: {}".format(install_path, ret_value.stderr))

    print("Installed mlir quingo compiler at directory:{}".format(install_path))


def install_on_Linux(mlir_compiler_path, old_version_path=None):
    """Install quingo compiler on Linux.
    """

    mlir_compiler_path.chmod(0o744)

    if old_version_path is not None:
        mlir_compiler_install_dir = old_version_path.parent
    else:
        mlir_compiler_install_dir = Path.home() / '.local'
        

    mlir_compiler_install_cmd = '"{}" --prefix="{}" --exclude-subdir'.format(
        mlir_compiler_path, mlir_compiler_install_dir)

    print("mlir_compiler_install_cmd: ", mlir_compiler_install_cmd)

    ret_value = subprocess.run(mlir_compiler_install_cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, shell=True)
    if(ret_value.returncode != 0):
        raise RuntimeError("Failed to install lastest quingo compiler with the"
                           "following error: {}".format(ret_value.stderr))
    
    if old_version_path is not None:
        mlir_compiler_exec_path = mlir_compiler_install_dir
        shutil.copy(str(mlir_compiler_install_dir/ 'bin' / 'quingoc'), str(mlir_compiler_exec_path))
    else:
        mlir_compiler_exec_path = mlir_compiler_install_dir / 'bin'

    set_path_env_on_Linux(mlir_compiler_exec_path)


def set_path_on_Windows(install_path):
    """Set path environment to contain the milr quingo compiler on Windows.
    """
    # Nothing to do, quingo-runtime will search the default install path
    # Default path is Path.home() / '.quingo'

    return


def install_on_Windows(mlir_compiler_path, old_version_path=None):
    """Install quingo compiler on Windows.
    """

    if old_version_path is not None:
        mlir_compiler_install_path = old_version_path.parent
    else:
        mlir_compiler_install_path = Path.home() / '.quingo'

    zip_file = zipfile.ZipFile(mlir_compiler_path)
    zip_list = zip_file.namelist()
    zip_file.extractall(mlir_compiler_install_path)
    zip_file.close()

    set_path_on_Windows(mlir_compiler_install_path)


def set_path_env_on_Darwin(install_path):
    """Set path environment to contain the milr quingo compiler on Darwin.
    """

    set_path_env_on_Linux(install_path)


def install_on_Darwin(mlir_compiler_path, old_version_path=None):
    """Install quingo compiler on Darwin.
    """

    if old_version_path is not None:
        mlir_compiler_install_path = old_version_path.parent
        mlir_compiler_exec_path = mlir_compiler_install_path
    else:
        mlir_compiler_install_path = Path.home() / '.local'
        mlir_compiler_exec_path = mlir_compiler_install_path / 'bin'

    if not mlir_compiler_exec_path.exists():
        mlir_compiler_exec_path.mkdir(exist_ok=True)

    try:
        # mount dmg file
        mount_cmd = "hdiutil attach " + str(mlir_compiler_path)

        ret_value = subprocess.run(mount_cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, shell=True)
        if(ret_value.returncode != 0):
            raise RuntimeError("Failed to mount lastest quingo compiler dmg file with the"
                               "following error: {}".format(ret_value.stderr))

        mlir_compiler_exec_file = pathlib.Path(
            "/Volumes/" + mlir_compiler_path.stem) / 'quingoc.app' / 'Contents' / 'Resources' / 'bin' / 'quingoc'

        shutil.copy(str(mlir_compiler_exec_file), str(mlir_compiler_exec_path))
    
    except Exception as e:
        raise RuntimeError("Failed to copy quingo compiler {} to '{}' with the "
                           "following error: {}".format(mlir_compiler_exec_file, mlir_compiler_exec_path, e))

    finally:
        # umount dmg file
        umount_cmd = "hdiutil detach " + str("/Volumes/" + mlir_compiler_path.stem)

        ret_value = subprocess.run(umount_cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True, shell=True)
        if(ret_value.returncode != 0):
            raise RuntimeError("Failed to umount lastest quingo compiler dmg file with the"
                               "following error: {}".format(ret_value.stderr))

    set_path_env_on_Darwin(mlir_compiler_exec_path)


def install_compiler(os_name, mlir_compiler_path, old_version_path=None):
    assert os_name in ['Linux', 'Windows', 'Darwin']

    if old_version_path is not None:
        backup_compiler(old_version_path)

    if(os_name == 'Windows'):
        install_on_Windows(mlir_compiler_path,
                           old_version_path)
    if(os_name == 'Linux'):
        install_on_Linux(mlir_compiler_path,
                         old_version_path)
    if(os_name == 'Darwin'):
        install_on_Darwin(mlir_compiler_path,
                         old_version_path)


def download_compiler(os_name, tmp_dir_name):
    assert os_name in ['Linux', 'Windows', 'Darwin']
    os_dl_suffix = {
        'Linux': '.sh',
        'Windows': '.zip',
        'Darwin': '.dmg'
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
            raise RuntimeError(
                "Failed to download quingo compiler from gitee.")

        quingoc_url = quingoc_asset['browser_download_url'] + \
            '/' + quingoc_asset['name']
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


def download_and_install_latest_quingoc(old_version_path=None):
    """Download the latest mlir quingo compiler.
    """
    os_name = platform.system()
    if os_name not in ['Linux', 'Windows', 'Darwin']:
        raise SystemError(
            "Currently pip installation does not support {}".format(os_name))

    tmp_dir = tempfile.TemporaryDirectory()
    tmp_dir_path = Path(tmp_dir.name)

    mlir_compiler_path = download_compiler(os_name, tmp_dir_path)
    install_compiler(os_name, mlir_compiler_path, old_version_path)

    shutil.rmtree(tmp_dir_path)

def get_lastest_version():
    """Get lastest quingo compiler version
    """

    latest_release_url = "https://gitee.com/api/v5/repos/{owner}/{repo}/releases/latest".format(
        owner="hpcl_quanta", repo="quingo-runtime")

    try:
        latest_release = requests.get(latest_release_url).text
        release_info = json.loads(latest_release)
        find_version = re.search(r'\d+\.\d+\.\d+', release_info['tag_name'])
        if find_version is not None:
            lastest_version = find_version.group()
        else:
            raise RuntimeError(
                "Failed to get lastest version of quingo compiler from gitee.")

    except Exception as e:
        raise RuntimeError("Failed to parse information retrieved from gitee with the "
                           "following error: {}".format(e))

    return lastest_version


def get_current_version():
    """Get current quingo compiler version
    """

    get_current_version_cmd = "{} --version".format(quingoc_path)

    ret_value = subprocess.run(get_current_version_cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, shell=True)
    if(ret_value.returncode != 0):
        raise RuntimeError("Failed to get local quingo compiler version with the"
                           "following error: {}".format(ret_value.stderr))

    find_version = re.search(r'\d+\.\d+\.\d+', ret_value.stdout.split()[0])
    if find_version is not None:
        current_version = find_version.group()
    else:
        raise RuntimeError(
            "Failed to get version of local quingo compiler from {}.".format(quingoc_path))

    return current_version


def check_update(quingoc_path):
    """Check local quingo compiler whether is latest version 
    """
    return True
    if get_current_version() == get_lastest_version():
        return False
    else:
        return True


if __name__ == "__main__":
    default_path = Path.home() / '.quingo'
    quingoc_path = distutils.spawn.find_executable(
        'quingoc', str(default_path))

    if quingoc_path is None:
        quingoc_path = distutils.spawn.find_executable('quingoc')

    if quingoc_path is None:
        download_and_install_latest_quingoc()
    else:
        if check_update(quingoc_path):
            download_and_install_latest_quingoc(pathlib.Path(quingoc_path))

from quingo import Quingo_task
import pytest
from pathlib import Path
import shutil
import os


@pytest.fixture(scope="module")
def qcis_fn():
    return "bell.qcis"


cur_dir = Path(__file__).parent
bell_qu_fn = cur_dir / "test_qu" / "bell.qu"


def test_default_build_dir():
    task = Quingo_task(bell_qu_fn, "bell")
    build_dir = task.build_dir

    print(build_dir)
    assert task.parent_work_dir == None
    assert str(build_dir).startswith("/tmp/")
    assert build_dir.exists()
    assert build_dir.is_dir()
    assert build_dir.name.startswith("qg")


def test_default_build_dir_debug():
    task = Quingo_task(bell_qu_fn, "bell", debug_mode=True)
    build_dir = task.build_dir

    print(build_dir)
    assert str(task.parent_work_dir) == os.path.join(os.getcwd(), "build")
    assert build_dir.exists()
    assert build_dir.is_dir()
    assert build_dir.name.startswith("qg")

    shutil.rmtree(str(build_dir))


def test_custom_build_dir_no_delete():
    build_under = cur_dir / "build-test"
    task = Quingo_task(
        bell_qu_fn, "bell", build_under=build_under, delete_build_dir=False
    )
    build_dir = task.build_dir

    print(build_dir)
    assert task.parent_work_dir == build_under
    assert build_dir.exists()
    assert build_dir.is_dir()
    assert build_dir.name.startswith("qg")

    shutil.rmtree(str(build_dir))


def test_custom_build_dir_with_delete():
    build_under = cur_dir / "build"
    task = Quingo_task(
        bell_qu_fn, "bell", build_under=build_under, delete_build_dir=True
    )
    build_dir = task.build_dir

    print(build_dir)
    assert task.parent_work_dir == build_under
    assert build_dir.exists()
    assert build_dir.is_dir()
    assert build_dir.name.startswith("qg")

    del task

    assert not build_dir.exists()

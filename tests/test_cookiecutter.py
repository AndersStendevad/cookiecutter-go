"""tests for cookiecutter"""

import pytest

from subprocess import run


def test_bake_project(bake):
    """check if cookiecutter will even bake"""
    pass


def test_pytest_in_baked_project(bake, helper):
    """check pytest in baked project"""
    helper.install_package(".")
    helper.check_result(run("tox -e pytest", shell=True, capture_output=True))


def test_pre_commit_in_baked_project(bake, helper):
    """check pre-commit in baked project"""
    helper.check_result(
        run("pre-commit run --all-files", shell=True, capture_output=True)
    )



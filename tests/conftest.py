""" Conftest for cookiecutter tests. """

import pytest
import json
import os

from pathlib import Path
from subprocess import run, CompletedProcess


class Helper:
    @staticmethod
    def check_result(result: CompletedProcess):
        """Check result of subprocess.run().

        Parameters:
        ===========
        result: CompletedProcess:
            Result of subprocess.run().

        Returns:
        ========
        None
        """
        stderr = result.stderr.decode("utf-8")
        stdout = result.stdout.decode("utf-8")
        if result.stderr and "SetuptoolsDeprecationWarning" not in stderr:
            raise Exception(stderr)
        if "ERROR:" in stdout:
            raise Exception(stdout)
        if "FAILED" in stdout:
            raise Exception(stdout)
        if "WARNING" in stdout:
            raise Exception(stdout)

    @classmethod
    def install_package(cls, package: str):
        """Install package.

        Parameters:
        ===========
        package: str:
            Package to install with pip.
        Returns:
        ========
        None
        """
        cls.check_result(
            run(
                ["pip", "install", "--disable-pip-version-check", package],
                capture_output=True,
            )
        )

    @classmethod
    def setup_git(cls):
        """Setup git.

        Parameters:
        ===========
        None

        Returns:
        ========
        None
        """
        cls.check_result(run(["git", "init", "--quiet"], capture_output=True))
        cls.check_result(run(["git", "add", "."], capture_output=True))


@pytest.fixture(scope="session")
def helper():
    """Helper for tests."""
    return Helper


@pytest.fixture
def cookiecutter_dict():
    """Return a cookiecutter dict."""
    with open("cookiecutter.json") as file:
        return json.load(file)


@pytest.fixture
def bake(cookies, cookiecutter_dict, helper):
    """Bake a cookiecutter project."""
    result = cookies.bake(extra_context=cookiecutter_dict)

    assert result.exit_code == 0
    assert result.exception is None

    path = result.project_path
    prev_cwd = Path.cwd()
    os.chdir(path)

    helper.setup_git()
    helper.install_package("pre-commit")
    helper.install_package("tox")
    yield {"path": path, "prev_cwd": prev_cwd}
    os.chdir(prev_cwd)

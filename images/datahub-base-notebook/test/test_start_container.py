# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import logging
import pytest

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "env,expected_server",
    [
        # (["JUPYTER_ENABLE_LAB=yes"], "lab"),
        (None, "notebook"),
    ],
)
def test_start_notebook(container, http_client, env, expected_server):
    """Test the notebook start-notebook script"""
    LOGGER.info(
        f"Test that the start-notebook launches the {expected_server} server from the env {env} ..."
    )
    c = container.run(
        tty=True,
        environment=env,
        command=["start-notebook.sh"],
    )
    resp = http_client.get("http://localhost:8888")
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    assert resp.status_code == 200, "Server is not listening"
    assert (
        f"Executing the command: jupyter {expected_server}" in logs
    ), f"Not the expected command (jupyter {expected_server}) was launched"
    # Checking warning messages
    if not env:
        msg = "WARN: Jupyter Notebook deprecation notice"
        assert msg in logs, f"Expected warning message {msg} not printed"


def test_tini_entrypoint(container, pid=1, command="tini"):
    """Check that tini is launched as PID 1

    Credits to the following answer for the ps options used in the test:
    https://superuser.com/questions/632979/if-i-know-the-pid-number-of-a-process-how-can-i-get-its-name
    """
    LOGGER.info(f"Test that {command} is launched as PID {pid} ...")
    c = container.run(
        tty=True,
        command=["start.sh"],
    )
    # Select the PID 1 and get the corresponding command
    cmd = c.exec_run(f"ps -p {pid} -o comm=")
    output = cmd.output.decode("utf-8").strip("\n")
    assert output == command, f"{command} shall be launched as pid {pid}, got {output}"

@pytest.mark.parametrize(
    "expected_server",
    [
        ("notebook"),
    ],
)
def test_jupyter_lab_exists(container, http_client, expected_server):
    """Check that the jupyter lab endpoint exists"""
    LOGGER.info(f"Checking that jupyter lab endpoint exists when using jupyter {expected_server}")
    c = container.run(
        tty=True,
        command=["start-notebook.sh"],
    )
    resp = http_client.get("http://localhost:8888/lab")
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    assert resp.status_code == 200, "Jupyter lab is not running"
    assert (
        f"Executing the command: jupyter {expected_server}" in logs
    ), f"Not the expected command (jupyter {expected_server}) was launched"

@pytest.mark.parametrize(
    "expected_server",
    [
        ("notebook"),
    ],
)
def test_jupyter_notebook_exists(container, http_client, expected_server):
    """Check that the jupyter notebook endpoint exists"""
    LOGGER.info(f"Checking that jupyter notebook endpoint exists when using jupyter {expected_server}")
    c = container.run(
        tty=True,
        command=["start-notebook.sh"],
    )
    resp = http_client.get("http://localhost:8888/tree")
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    assert resp.status_code == 200, "Jupyter notebook(/tree) is not running "
    assert (
        f"Executing the command: jupyter {expected_server}" in logs
    ), f"Not the expected command (jupyter {expected_server}) was launched"

@pytest.mark.parametrize(
    "expected_server",
    [
        ("notebook"),
    ],
)
def test_server_extensions_start(container, http_client, expected_server):
    """Check that the server extensions start"""
    LOGGER.info(f"Checking that server extensions start when using jupyter {expected_server}")
    c = container.run(
        tty=True,
        command=["start-notebook.sh"],
    )
    resp = http_client.get("http://localhost:8888")
    logs = c.logs(stdout=True).decode("utf-8")
    LOGGER.debug(logs)
    assert resp.status_code == 200, "Server is not listening"
    assert (
        "Error loading server extension" not in logs
    ), f"Server Extension(s) failed to start"
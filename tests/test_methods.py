"""Tests for Tunnel RPC methods."""
from tunnel_rpc.methods import eval_commands


def test_eval_commands(docker_api_client, tunnel_container_factory):
    """Tests the command evaluation method.

    eval_commands should return a string
    eval_commands logs should contain both stderr and stdout

    """
    ls_container = tunnel_container_factory()
    ls_logs = eval_commands(docker_api_client, ls_container, ['ls'])
    assert isinstance(ls_logs, str), "eval_commands should return a string"

    stdout_container = tunnel_container_factory()
    stdout_logs = eval_commands(docker_api_client, stdout_container, [
        'echo 43'
    ])
    assert "43" in stdout_logs, "eval_commands should contain stdout"

    stderr_container = tunnel_container_factory()
    stderr_logs = eval_commands(docker_api_client, stderr_container, [
        'echo 43 1>&2'
    ])
    assert "43" in stderr_logs, "eval_commands should contain stderr"

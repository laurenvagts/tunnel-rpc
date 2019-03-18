# -*- coding: utf-8 -*-
"""Tests for Tunnel RPC methods.

"""
from tunnel_rpc.methods import eval_commands, parse_output


def test_eval_commands(docker_api_client, tunnel_container_factory):
    """Tests the command evaluation method.

    eval_commands should return a string
    eval_commands logs should contain both stderr and stdout

    """
    ls_container = tunnel_container_factory()
    ls_logs = eval_commands(docker_api_client, ls_container, ["ls"])
    assert isinstance(ls_logs, str), "eval_commands should return a string"

    stdout_container = tunnel_container_factory()
    stdout_logs = eval_commands(
        docker_api_client, stdout_container, ["echo 43"]
    )
    assert "43" in stdout_logs, "eval_commands should contain stdout"

    stderr_container = tunnel_container_factory()
    stderr_logs = eval_commands(
        docker_api_client, stderr_container, ["echo 43 1>&2"]
    )
    assert "43" in stderr_logs, "eval_commands should contain stderr"


def test_parse_output():
    """Test the parse output method.

    parse_output should return a list of tuples
    parse_output should ignore preambles
    parse_output should append every command log

    """

    response = parse_output("$ \r\n0\r\n")
    assert isinstance(response, list), "parse_output should return a list"
    assert isinstance(
        response[0], tuple
    ), "parse_output should return a list of tuples"

    response = parse_output("should not show up \r\n$ \r\n0\r\n")
    assert all(
        not isinstance(item, str) or "should not show up" not in item
        for t_item in response
        for item in t_item
    ), "parse_output should ignore preambles"

    for length in range(2, 10):
        output = "$ \r\n0\r\n" * length
        response = parse_output(output)
        assert (
            len(response) == length
        ), "parse_output should append every command log"

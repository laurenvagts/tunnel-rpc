# -*- coding: utf-8 -*-
"""RPC Methods available for Tunnel RPC.

    Includes any helper methods needed to run @method annotated rpc calls.

    THe current calls are:

        * run:  run arbitrary commands on a docker bash instance
                with persistent state between commands.

"""
import os
from docker import APIClient

__all__ = ["run"]


def create_container(api_client):
    """Creates a basic REPL bash container in Docker.

    Args:
        api_client (ApiClient): the client to be used for container creation.

    Returns:
        (str) the container's id.

    """
    container = api_client.create_container(
        image="bash:latest",
        stdin_open=True,
        tty=True,
        command=[
            "bash",
            "-c",
            "while read CMD ; "
            "do echo '$ '$CMD ; "
            "eval $CMD ; echo $? ; done",
        ],
    )
    api_client.start(container)
    return container


def eval_commands(client, cont, commands):
    """Evaluates commands in a docker container.

    Keeps stdin open and runs commands on same environment.

    Args:
        client (APIClient): API interaction client for a Docker host
        cont (str): Container's ID used to run the commands
        commands (List[str]): Commands to run

    Returns:
        (str) The stdout/stderr combined output

    """
    socket = client.attach_socket(cont, params={"stdin": 1, "stream": 1})
    file_descriptor = socket.fileno()

    for cmd in commands:
        cmd += "\n"
        os.write(file_descriptor, cmd.encode("utf-8"))
    socket.close()

    client.stop(cont)
    client.wait(cont)

    return client.logs(cont, stdout=True, stderr=True).decode()


def parse_output(output):
    """Store all terminal lines associated with the program run commands.

    Args:
        output(str): Container with pre-run commands in terminal

    Returns:
        (list) The contents of the terminal

    """
    preamble = True
    commands = []
    buffer = []
    for line in output.rstrip("\r\n").split("\r\n"):
        if line.startswith("$ "):
            if preamble:
                preamble = False
            else:
                commands.append(
                    (buffer[0], "\n".join(buffer[1:-1]), int(buffer[-1]))
                )
            buffer.clear()
        buffer.append(line)
    commands.append((buffer[0], "\n".join(buffer[1:-1]), int(buffer[-1])))
    return commands


def run(request=None):
    """Runs commands in a docker container and parses the log output.

    Args:
        request (dict): requested commands to run

    Returns:
        (list) parsed outputs

    """
    api_client = APIClient()
    container = create_container(api_client)
    lines = eval_commands(api_client, container, request["commands"])
    results = parse_output(lines)
    api_client.remove_container(container)
    return results

import os
from typing import List
from docker import APIClient
from docker.errors import APIError
from jsonrpcserver import method


def eval_commands(client: APIClient,
                  cont: str,
                  commands: List[str]) -> str:
    """Evaluates commands in a docker container.

    Keeps stdin open and runs commands on same environment.

    Args:
        client : API interaction client for a Docker host
        cont : Container's ID used to run the commands
        commands : Commands to run

    Returns:
        The stdout/stderr combined output

    """
    try:

        socket = client.attach_socket(cont, params={'stdin': 1, 'stream': 1})
        fd = socket.fileno()

        for cmd in commands:
            cmd += '\n'
            os.write(fd, cmd.encode('utf-8'))
        socket.close()

        client.stop(cont)
        client.wait(cont)

        return client.logs(cont, stdout=True, stderr=True).decode()

    except APIError as e:
        raise e


def parse_output(output):
    preamble = True
    commands = []
    buffer = []
    for line in output.rstrip('\r\n').split('\r\n'):
        if line == '':
            continue
        if line.startswith('$ '):
            if preamble:
                preamble = False
            else:
                commands.append(
                    (buffer[0], "\n".join(buffer[1:-1]), int(buffer[-1])))
            buffer.clear()
        buffer.append(line)
    commands.append((buffer[0], "\n".join(buffer[1:-1]), int(buffer[-1])))
    return commands


@method
def run(request=None):
    api = APIClient()
    bash = api.create_container(
        image='bash:latest',
        stdin_open=True,
        tty=True,
        command=['bash', '-c', """
while read CMD ; do
 echo "\\$ $CMD" ;
 eval $CMD ;
 echo $? ;
done"""]
    )

    api.start(bash)

    lines = eval_commands(api, bash, request['commands'])
    results = parse_output(lines)
    api.remove_container(bash)
    return results

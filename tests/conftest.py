import pytest


@pytest.fixture()
def docker_api_client():
    import docker
    return docker.APIClient()


@pytest.fixture()
def tunnel_container_factory(docker_api_client):
    def _factory():
        container = docker_api_client.create_container(
            image='bash:latest',
            stdin_open=True,
            tty=True,
            command=['bash', '-c', 'while read CMD ; do echo "\\$ $CMD" ; '
                                   'eval $CMD ; echo $? ; done']
        )
        docker_api_client.start(container)
        return container


    return _factory

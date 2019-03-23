# -*- coding: utf-8 -*-
"""Pytest Fixtures for Tunnel RPC.

"""
import pytest


@pytest.fixture()
def docker_api_client():
    """Provides a docker-api client.

    """
    import docker

    return docker.APIClient()


@pytest.fixture()
# pragma pylint: disable=redefined-outer-name
def tunnel_container_factory(docker_api_client):
    """Provides a container creation factory.

        Assumes The tunnel_rpc create_container works properly.

    """
    from tunnel_rpc.methods import create_container

    return lambda: create_container(docker_api_client)

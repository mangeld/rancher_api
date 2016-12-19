from random import choice

from rancher import api
from rancher.engine import RequestAdapter
from rancher.models import RancherEnvironment


DOCKER_COMPOSE = """
nginx:
    image: nginx:latest
"""

class TestEnvironmentIsListed:

    def test_enviroments_are_listed(self):
        settings = api.ApiSettings()
        http_client = RequestAdapter()
        client = api.RancherApi(settings, http_client)

        settings.url = "http://rancher.habitissimo.lan:8080/v1"

        env = choice(client.envs)
        assert isinstance(env, RancherEnvironment)

    def test_create_env_with_docker_compose(self):
        settings = api.ApiSettings()
        settings.url = "http://rancher.habitissimo.lan:8080/v1"
        http_client = RequestAdapter()
        client = api.RancherApi(settings, http_client)

        account = client.get_account("Default")
        environment = client.create_env(
            "created-from-python-with-compose",
            account,
            docker_compose=DOCKER_COMPOSE
        )
        service_count = len(environment.services)
        environment.remove()

        assert service_count == 1

    def test_create_env(self):
        settings = api.ApiSettings()
        http_client = RequestAdapter()
        client = api.RancherApi(settings, http_client)

        settings.url = "http://rancher.habitissimo.lan:8080/v1"

        account = client.get_account("Default")
        environment = client.create_env('created-from-python', account)
        environment.remove()


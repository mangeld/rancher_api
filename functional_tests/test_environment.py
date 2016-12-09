from random import choice

from rancher import api
from rancher.engine import RequestAdapter
from rancher.models import RancherEnvironment


class TestEnvironmentIsListed:

    def test_enviroments_are_listed(self):
        settings = api.ApiSettings()
        http_client = RequestAdapter()
        client = api.RancherApi(settings, http_client)

        settings.url = "http://rancher.habitissimo.lan:8080/v1"

        env = choice(client.list_envs())
        assert isinstance(env, RancherEnvironment)

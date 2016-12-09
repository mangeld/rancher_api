from rancher.api import RancherApi, ApiSettings, RequestAdapter

from mock import MagicMock


class TestListStack:

    def test_request_adapter_is_called(self):
        settings = ApiSettings()
        http_client = RequestAdapter()
        http_client.get = MagicMock()

        settings.url = "http://test.com"
        api = RancherApi(settings, http_client)
        api.list_envs()

        http_client.get.assert_called()

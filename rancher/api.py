from rancher.models import RancherEnvironment


class ApiSettings:
    url = None
    access_key = None
    secret_key = None
    environment = None


class RancherApi:

    def __init__(self, settings, request_adapter):
        self.settings = settings
        self.http = request_adapter

    def create_env(self, env_definition):
        pass

    def list_envs(self):
        envs = self.http.get(self.settings.url + '/environments')['data']
        return [RancherEnvironment.from_dict(i) for i in envs]

    def remove_env(self, environment):
        self.http.post(environment.actions.remove)

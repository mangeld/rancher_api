try:
    from functools import lru_cache
except ImportError:
    from rancher.utils import dummy_lru_cache as lru_cache

from rancher.models import RancherEnvironment, RancherApiHome, RancherAccount
from rancher.errors import ApiException, ExistentObjectException
from rancher.engine import RequestAdapter


class ApiSettings:
    url = None
    access_key = None
    secret_key = None
    account = None


class RancherApi:

    def __init__(self, settings, request_adapter):
        self.settings = settings
        self.http = request_adapter

    @classmethod
    def client(cls, url):
        settings = ApiSettings()
        settings.url = url
        http_client = RequestAdapter()
        return cls(settings, http_client)

    @property
    @lru_cache(maxsize=10)
    def links(self):
        response = self.http.get(self.settings.url)
        return RancherApiHome.from_dict(response.json()).links

    @property
    @lru_cache(maxsize=100)
    def accounts(self):
        response = self.http.get(self.links.accounts)
        if not response.ok:
            raise ApiException(response.json()['message'])
        return [RancherAccount.from_dict(i) for i in response.json()['data']]

    @property
    def envs(self):
        envs = self.http.get(self.settings.url + '/environments').json()['data']
        return [RancherEnvironment.from_dict(i) for i in envs]

    @property
    def projects(self):
        return [i for i in self.accounts if i.type == 'project']


    def get_env(self, name=None):
        for env in self.envs:
            if env.name.lower() == name.lower():
                return env

    def get_project(self, name=None):
        """
        Search a project by name in a case-insensitive form.
        """
        for project in self.projects:
            if project.name.lower() == name.lower():
                return project

    def get_account(self, name=None):
        """
        Search an account by name in a case-insensitive form.
        """
        for account in self.accounts:
            if account.name.lower() == name.lower():
                return account
        return None

    def create_env(self, name, account, description="", docker_compose="", rancher_compose=""):
        if not isinstance(account, RancherAccount):
            raise TypeError(
                'Provide a RancherAccount object'
                ' for the parameter account'
            )

        if not account.type == 'project':
            raise TypeError(
                "An account with type 'project' "
                "has to be given. Provided one was"
                " of type: {}"
                .format(account.type)
            )

        data = {
            'name': name,
            'description': description,
            'dockerCompose': docker_compose,
            'rancherCompose': rancher_compose,
            'startOnCreate': True,
        }
        response = self.http.post(
            self.settings.url + "/projects/{}/environment".format(account.id),
            json=data
        )
        if not response.ok:
            if response.status_code == 422:
                raise ExistentObjectException("The environment already exists")
            message = response.json()['message']
            raise ApiException(message)

        return RancherEnvironment.from_dict(response.json())

    def remove_env(self, environment):
        environment.remove()

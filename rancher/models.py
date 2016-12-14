from functools import lru_cache

from rancher.engine import Model, JsonMarshable


class RancherEnvironmentActions(Model, JsonMarshable):
    upgrade = ""
    update = ""
    remove = ""
    addouputs = ""
    activateservices = ""
    deactivateservices = ""
    exportconfig = ""


class RancherEnvironmentService(Model, JsonMarshable):
    name = ""
    state = ""
    id = ""
    created = ""
    created_ts = ""
    current_scale = ""


class RancherEnvironmentLinks(Model, JsonMarshable):
    account = ""
    composeConfig = ""
    configItemStatuses = ""
    self = ""
    services = ""


class RancherEnvironment(Model, JsonMarshable):
    id = None
    environment = None
    name = ""
    description = ""
    docker_compose = ""
    rancher_compose = ""
    created_ts = ""
    start_services = True
    uuid = ""
    actions = RancherEnvironmentActions
    links = RancherEnvironmentLinks

    @property
    @lru_cache(maxsize=128)
    def services(self):
        data = self._http.get(self.links.services).json()['data']
        #import ipdb; ipdb.set_trace()
        return [RancherEnvironmentService.from_dict(i) for i in data]

    def remove(self):
        self._http.post(self.actions.remove)


class RancherService:
    pass

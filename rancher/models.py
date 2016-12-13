from rancher.engine import Model, JsonMarshable


class RancherEnvironmentActions(Model, JsonMarshable):
    upgrade = ""
    update = ""
    remove = ""
    addouputs = ""
    activateservices = ""
    deactivateservices = ""
    exportconfig = ""


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

    def remove(self):
        self._http.post(self.actions.remove)

class RancherService:
    pass

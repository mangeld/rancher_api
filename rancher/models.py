from rancher.engine import Model, JsonMarshable


class RancherEnvironment(Model, JsonMarshable):
    id = None
    environment = None
    name = ""
    description = ""
    docker_compose = ""
    rancher_compose = ""
    start_services = True


class RancherService:
    pass

from rancher.engine import Model


class RancherEnvironment(Model):
    id = None
    environment = None
    name = ""
    description = ""
    docker_compose = ""
    rancher_compose = ""
    start_services = True


class RancherService:
    pass

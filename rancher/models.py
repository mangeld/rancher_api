from rancher.engine import Model, JsonMarshable
from rancher.exceptions import NotRunningException
import websocket


class RancherApiHomeLinks(Model, JsonMarshable):
    accounts = ""
    addOutputsInputs = ""
    agents = ""
    amazonec2Configs = ""
    apiKeys = ""
    auditLogs = ""
    azureConfigs = ""
    azureadconfigs = ""
    backupTargets = ""
    backups = ""
    certificates = ""
    composeProjects = ""
    composeServices = ""
    configItemStatuses = ""
    configItems = ""
    containerEvents = ""
    containerExecs = ""
    containers = ""
    credentials = ""
    databasechangeloglocks = ""
    databasechangelogs = ""
    digitaloceanConfigs = ""
    dnsServices = ""
    dockerBuilds = ""
    environmentUpgrades = ""
    environments = ""
    extensionPoints = ""
    externalDnsEvents = ""
    externalEvents = ""
    externalHandlerExternalHandlerProcessMaps = ""
    externalHandlerProcesses = ""
    externalHandlers = ""
    externalHostEvents = ""
    externalServiceEvents = ""
    externalServices = ""
    externalStoragePoolEvents = ""
    externalVolumeEvents = ""
    githubconfigs = ""
    haConfigInputs = ""
    haConfigs = ""
    healthcheckInstanceHostMaps = ""
    hostAccesses = ""
    hostApiProxyTokens = ""
    hosts = ""
    identities = ""
    images = ""
    instanceLinks = ""
    instances = ""
    ipAddresses = ""
    kubernetesServices = ""
    labels = ""
    ldapconfigs = ""
    loadBalancerConfigs = ""
    loadBalancerServices = ""
    localAuthConfigs = ""
    machineDrivers = ""
    machines = ""
    mounts = ""
    networks = ""
    openldapconfigs = ""
    packetConfigs = ""
    passwords = ""
    physicalHosts = ""
    ports = ""
    processDefinitions = ""
    processExecutions = ""
    processInstances = ""
    projectMembers = ""
    projects = ""
    pullTasks = ""
    register = ""
    registrationTokens = ""
    registries = ""
    registryCredentials = ""
    resourceDefinitions = ""
    scalePolicys = ""
    schemas = ""
    self = ""
    serviceConsumeMaps = ""
    serviceEvents = ""
    serviceExposeMaps = ""
    serviceProxies = ""
    services = ""
    settings = ""
    snapshotBackupInputs = ""
    snapshots = ""
    statsAccesses = ""
    storagePools = ""
    taskInstances = ""
    tasks = ""
    typeDocumentations = ""
    ubiquityConfigs = ""
    userPreferences = ""
    virtualMachines = ""
    volumes = ""


class RancherApiHome(Model, JsonMarshable):
    actions = ""
    id = ""
    links = RancherApiHomeLinks


class RancherAccount(Model, JsonMarshable):
    name = ""
    allow_system_role = ""
    created = ""
    created_ts = ""
    description = ""
    id = ""
    state = ""
    type = ""
    uuid = ""


class RancherEnvironmentActions(Model, JsonMarshable):
    upgrade = ""
    update = ""
    remove = ""
    addouputs = ""
    activateservices = ""
    deactivateservices = ""
    exportconfig = ""


class RancherServiceActions(Model, JsonMarshable):
    update = ""
    restart = ""
    remove = ""
    setservicelinks = ""
    removeservicelink = ""
    upgrade = ""
    addservicelink = ""
    deactivate = ""


class RancherServiceLaunchConfig(Model, JsonMarshable):
    labels = ""
    image_uuid = ""
    environment = ""


class RancherServiceLinks(Model, JsonMarshable):
    self = ""
    account = ""
    consumedbyservices = ""
    evironment = ""
    instances = ""
    service_expose_maps = ""
    container_stats = ""


class RancherEnvironmentService(Model, JsonMarshable):
    name = ""
    state = ""
    id = ""
    created = ""
    created_ts = ""
    current_scale = ""
    launch_config = RancherServiceLaunchConfig
    links = RancherServiceLinks
    actions = RancherServiceActions

    def __repr__(self):
        return "<{o.__class__.__name__} {o.name} ({o.state})>".format(o=self)

    def stop(self):
        self._http.post(self.actions.deactivate)

    def remove(self):
        self._http.post(self.actions.remove)

    @property
    def labels(self):
        return getattr(self.launch_config, 'labels', None)

    @property
    def environment(self):
        return self.launch_config.environment

    @property
    def instances(self):
        data = self._http.get(self.links.instances).json()['data']
        return [RancherEnvironmentServiceInstance.from_dict(i) for i in data]


class RancherEnvironmentServiceInstanceLinks(Model, JsonMarshable):
    self = ""
    account = ""
    credentials = ""
    healthcheckInstanceHostMaps = ""
    hosts = ""
    instanceLabels = ""
    instanceLinks = ""
    instances = ""
    mounts = ""
    ports = ""
    registryCredential = ""
    serviceEvents = ""
    serviceExposeMaps = ""
    services = ""
    targetInstanceLinks = ""
    volumes = ""
    stats = ""
    containerStats = ""


class RancherEnvironmentServiceInstanceActions(Model, JsonMarshable):
    update = ""
    stop = ""
    restart = ""
    migrate = ""
    logs = ""
    setlabels = ""
    execute = ""
    proxy = ""


class RancherEnvironmentServiceInstance(Model, JsonMarshable):
    id = ""
    type = ""
    links = RancherEnvironmentServiceInstanceLinks
    actions = RancherEnvironmentServiceInstanceActions
    state = ""
    name = ""
    account_id = ""
    created_ts = ""
    created = ""
    data_volumes = ""

    @property
    def running(self):
        return self.state == 'running'

    def __repr__(self):
        return "<{o.__class__.__name__} {o.name} ({o.state})>".format(o=self)

    def execute(self, command=list(), attach_stdin=False, attach_stdout=False, tty=False, open_ws=False):
        if self.state != 'running':
            raise NotRunningException("Can't execute a command on an stopped container.")
        response = self._http.post(
            self.actions.execute,
            json={
                'command': command,
                'attachStdin': attach_stdin,
                'attachStdout': attach_stdout,
                'tty': tty,
            }
        )

        if open_ws:
            token = response.json()['token']
            ws_url = response.json()['url']
            ws = websocket.WebSocket()
            ws.connect("{}?token={}".format(ws_url, token))
            return ws


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
    health_state = ""
    state = ""
    rancher_compose = ""
    created_ts = ""
    start_services = True
    uuid = ""
    actions = RancherEnvironmentActions
    links = RancherEnvironmentLinks

    @property
    def services(self):
        data = self._http.get(self.links.services).json()['data']
        return [RancherEnvironmentService.from_dict(i) for i in data]

    def remove(self):
        self._http.post(self.actions.remove)

    def stop(self):
        self._http.post(self.actions.deactivateservices)


class RancherService:
    pass

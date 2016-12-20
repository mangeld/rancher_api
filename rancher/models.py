from rancher.engine import Model, JsonMarshable


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


class RancherServiceLaunchConfig(Model, JsonMarshable):
    labels = ""
    image_uuid = ""
    environment = ""


class RancherEnvironmentService(Model, JsonMarshable):
    name = ""
    state = ""
    id = ""
    created = ""
    created_ts = ""
    current_scale = ""
    launch_config = RancherServiceLaunchConfig

    @property
    def labels(self):
        return self.launch_config.labels

    @property
    def environment(self):
        return self.launch_config.environment


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
    def services(self):
        data = self._http.get(self.links.services).json()['data']
        #import ipdb; ipdb.set_trace()
        return [RancherEnvironmentService.from_dict(i) for i in data]

    def remove(self):
        self._http.post(self.actions.remove)


class RancherService:
    pass

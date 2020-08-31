from typing import List

from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.driver_context import (
    InitCommandContext,
    AutoLoadCommandContext,
    ResourceCommandContext,
    AutoLoadDetails,
    CancellationContext,
    ResourceRemoteCommandContext,
)
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext

from cloudshell.cp.core.cancellation_manager import CancellationContextManager
from cloudshell.cp.core.request_actions import (
    DeployVMRequestActions,
    DeployedVMActions,
    GetVMDetailsRequestActions,
)
from cloudshell.cp.openstack import constants
from cloudshell.cp.openstack.flows import delete_instance
from cloudshell.cp.openstack.flows import DeployAppFromNovaImgFlow
from cloudshell.cp.openstack.flows import PowerFlow
from cloudshell.cp.openstack.flows import GetVMDetailsFlow
from cloudshell.cp.openstack.flows import refresh_ip
from cloudshell.cp.openstack.models import OSNovaImgDeployedApp
from cloudshell.cp.openstack.models import OSNovaImgDeployApp
from cloudshell.cp.openstack.os_api.api import OSApi
from cloudshell.cp.openstack.os_api.services import validate_conf_and_connection
from cloudshell.cp.openstack.resource_config import OSResourceConfig


class OpenstackShell2GDriver(ResourceDriverInterface):
    SHELL_NAME = constants.SHELL_NAME

    def __init__(self):
        pass

    def initialize(self, context: InitCommandContext):
        pass

    def get_inventory(self, context: AutoLoadCommandContext) -> AutoLoadDetails:
        """Check connection to OpenStack."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Autoload command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            os_api = OSApi(conf, logger)
            validate_conf_and_connection(os_api, conf)
            return AutoLoadDetails([], [])

    def Deploy(
        self,
        context: ResourceCommandContext,
        request: str,
        cancellation_context: CancellationContext,
    ) -> str:
        """Deploy image."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Deploy command")
            logger.debug(f"Request: {request}")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            cancellation_manager = CancellationContextManager(cancellation_context)
            DeployVMRequestActions.register_deployment_path(OSNovaImgDeployApp)
            request_actions = DeployVMRequestActions.from_request(request, api)
            os_api = OSApi(conf, logger)
            return DeployAppFromNovaImgFlow(
                conf, cancellation_manager, os_api, logger
            ).deploy(request_actions)

    def PowerOn(self, context: ResourceRemoteCommandContext, ports: List[str]):
        """Method spins up the VM."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting PowerOn command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            DeployedVMActions.register_deployment_path(OSNovaImgDeployedApp)
            resource = context.remote_endpoints[0]
            actions = DeployedVMActions.from_remote_resource(resource, api)
            os_api = OSApi(conf, logger)
            return PowerFlow(os_api, actions.deployed_app, logger).power_on()

    def remote_refresh_ip(
        self,
        context: ResourceRemoteCommandContext,
        ports: List[str],
        cancellation_context: CancellationContext,
    ):
        """Retrieves the VM's updated IP address from the OpenStack."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Remote Refresh IP command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            DeployedVMActions.register_deployment_path(OSNovaImgDeployedApp)
            resource = context.remote_endpoints[0]
            actions = DeployedVMActions.from_remote_resource(resource, api)
            os_api = OSApi(conf, logger)
            refresh_ip(os_api, actions.deployed_app, conf)

    def GetVmDetails(
        self,
        context: ResourceCommandContext,
        requests: str,
        cancellation_context: CancellationContext,
    ) -> str:
        """Get instance operating system, specifications and networking information."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Deploy command")
            logger.debug(f"Requests: {requests}")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            cancellation_manager = CancellationContextManager(cancellation_context)
            GetVMDetailsRequestActions.register_deployment_path(OSNovaImgDeployedApp)
            actions = GetVMDetailsRequestActions.from_request(requests, api)
            os_api = OSApi(conf, logger)
            return GetVMDetailsFlow(
                conf, cancellation_manager, os_api, logger
            ).get_vm_details(actions)

    def PowerCycle(self, context, ports, delay):
        pass

    def PowerOff(self, context: ResourceRemoteCommandContext, ports: List[str]):
        """Method shuts down (or powers off) the VM instance."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting PowerOn command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            DeployedVMActions.register_deployment_path(OSNovaImgDeployedApp)
            resource = context.remote_endpoints[0]
            actions = DeployedVMActions.from_remote_resource(resource, api)
            os_api = OSApi(conf, logger)
            return PowerFlow(os_api, actions.deployed_app, logger).power_off()

    def DeleteInstance(self, context: ResourceRemoteCommandContext, ports: List[str]):
        """Deletes the VM from the OpenStack."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting PowerOn command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            DeployedVMActions.register_deployment_path(OSNovaImgDeployedApp)
            resource = context.remote_endpoints[0]
            actions = DeployedVMActions.from_remote_resource(resource, api)
            os_api = OSApi(conf, logger)
            delete_instance(os_api, actions.deployed_app)

    def ApplyConnectivityChanges(
        self, context: ResourceCommandContext, request: str
    ) -> str:
        """Connects/disconnect VMs to VLANs based on requested actions."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting PowerOn command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            os_api = OSApi(conf, logger)

    def SetAppSecurityGroups(self, context, request):
        """
        Called via cloudshell API call

        Programmatically set which ports will be open on each of the apps in the sandbox, and from
        where they can be accessed. This is an optional command that may be implemented.
        Normally, all outbound traffic from a deployed app should be allowed.
        For inbound traffic, we may use this method to specify the allowed traffic.
        An app may have several networking interfaces in the sandbox. For each such interface, this command allows to set
        which ports may be opened, the protocol and the source CIDR

        If operation fails, return a "success false" action result.

        :param ResourceCommandContext context:
        :param str request:
        :return:
        :rtype: str
        """
        pass

    def cleanup(self):
        pass

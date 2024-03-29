from typing import List

from cloudshell.cp.core.cancellation_manager import CancellationContextManager
from cloudshell.cp.core.request_actions import (
    DeployedVMActions,
    DeployVMRequestActions,
    GetVMDetailsRequestActions,
)
from cloudshell.cp.core.request_actions.save_restore_app import (
    SaveRestoreRequestActions,
)
from cloudshell.shell.core.driver_context import (
    AutoLoadCommandContext,
    AutoLoadDetails,
    CancellationContext,
    InitCommandContext,
    ResourceCommandContext,
    ResourceRemoteCommandContext,
    UnreservedResourceCommandContext,
)
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.shell.flows.connectivity.parse_request_service import (
    ParseConnectivityRequestService,
)

from cloudshell.cp.openstack import constants
from cloudshell.cp.openstack.flows import (
    ConnectivityFlow,
    DeployAppFromNovaImgFlow,
    GetVMDetailsFlow,
    PowerFlow,
    delete_instance,
    get_console,
    refresh_ip,
    validate_console_type,
)
from cloudshell.cp.openstack.flows.save_restore_app import SaveRestoreAppFlow
from cloudshell.cp.openstack.models import OSNovaImgDeployApp, OSNovaImgDeployedApp
from cloudshell.cp.openstack.models.connectivity_models import OsConnectivityActionModel
from cloudshell.cp.openstack.os_api.api import OsApi
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
            os_api = OsApi.from_config(conf, logger)
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
            os_api = OsApi.from_config(conf, logger)
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
            os_api = OsApi.from_config(conf, logger)
            return PowerFlow(os_api, actions.deployed_app, logger).power_on()

    def remote_refresh_ip(
        self,
        context: ResourceRemoteCommandContext,
        ports: List[str],
        cancellation_context: CancellationContext,
    ):
        """Retrieves the VM's updated IP address from the OpenStack."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Refresh IP command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            DeployedVMActions.register_deployment_path(OSNovaImgDeployedApp)
            resource = context.remote_endpoints[0]
            actions = DeployedVMActions.from_remote_resource(resource, api)
            os_api = OsApi.from_config(conf, logger)
            refresh_ip(os_api, actions.deployed_app, conf)

    def GetVmDetails(
        self,
        context: ResourceCommandContext,
        requests: str,
        cancellation_context: CancellationContext,
    ) -> str:
        """Get instance operating system, specifications and networking information."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Get VM Details command")
            logger.debug(f"Requests: {requests}")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            cancellation_manager = CancellationContextManager(cancellation_context)
            GetVMDetailsRequestActions.register_deployment_path(OSNovaImgDeployedApp)
            actions = GetVMDetailsRequestActions.from_request(requests, api)
            os_api = OsApi.from_config(conf, logger)
            return GetVMDetailsFlow(
                conf, cancellation_manager, os_api, logger
            ).get_vm_details(actions)

    def PowerCycle(self, context, ports, delay):
        pass

    def PowerOff(self, context: ResourceRemoteCommandContext, ports: List[str]):
        """Method shuts down (or powers off) the VM instance."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting PowerOff command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            DeployedVMActions.register_deployment_path(OSNovaImgDeployedApp)
            resource = context.remote_endpoints[0]
            actions = DeployedVMActions.from_remote_resource(resource, api)
            os_api = OsApi.from_config(conf, logger)
            return PowerFlow(os_api, actions.deployed_app, logger).power_off()

    def DeleteInstance(self, context: ResourceRemoteCommandContext, ports: List[str]):
        """Deletes the VM from the OpenStack."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Delete Instance command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            DeployedVMActions.register_deployment_path(OSNovaImgDeployedApp)
            resource = context.remote_endpoints[0]
            actions = DeployedVMActions.from_remote_resource(resource, api)
            os_api = OsApi.from_config(conf, logger)
            delete_instance(os_api, actions.deployed_app)

    def ApplyConnectivityChanges(
        self, context: ResourceCommandContext, request: str
    ) -> str:
        """Connects/disconnect VMs to VLANs based on requested actions."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Connectivity command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            parse_connectivity_req_service = ParseConnectivityRequestService(
                is_vlan_range_supported=False,
                is_multi_vlan_supported=False,
                connectivity_model_cls=OsConnectivityActionModel,
            )
            return ConnectivityFlow(
                conf, parse_connectivity_req_service, logger
            ).apply_connectivity(request)

    def SetAppSecurityGroups(
        self, context: ResourceCommandContext, request: str
    ) -> str:
        """Set application security groups.

        Programmatically set which ports will be open on each of the apps in the sandbox
        and from where they can be accessed.
        This is an optional command that may be implemented.
        Normally, all outbound traffic from a deployed app should be allowed.
        For inbound traffic, we may use this method to specify the allowed traffic.
        An app may have several networking interfaces in the sandbox. For each such
        interface, this command allows to set which ports may be opened, the protocol
        and the source CIDR
        """
        pass

    def cleanup(self):
        pass

    def console(
        self,
        context: ResourceRemoteCommandContext,
        console_type: str,
        ports: List[str],
    ) -> str:
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Get Console command")
            validate_console_type(console_type)
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api)
            DeployedVMActions.register_deployment_path(OSNovaImgDeployedApp)
            resource = context.remote_endpoints[0]
            actions = DeployedVMActions.from_remote_resource(resource, api)
            os_api = OsApi.from_config(conf, logger)
            return get_console(os_api, actions.deployed_app, console_type)

    def SaveApp(
        self,
        context: ResourceCommandContext,
        request: str,
        cancellation_context: CancellationContext,
    ) -> str:
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Save App command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api=api)
            cancellation_manager = CancellationContextManager(cancellation_context)
            actions = SaveRestoreRequestActions.from_request(request)
            return SaveRestoreAppFlow(conf, logger, cancellation_manager).save_apps(
                actions.save_app_actions
            )

    def DeleteSavedApps(
        self,
        context: UnreservedResourceCommandContext,
        request: str,
        cancellation_context: CancellationContext,
    ) -> str:
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Delete Saved App command")
            api = CloudShellSessionContext(context).get_api()
            conf = OSResourceConfig.from_context(self.SHELL_NAME, context, api=api)
            cancellation_manager = CancellationContextManager(cancellation_context)
            actions = SaveRestoreRequestActions.from_request(request)
            return SaveRestoreAppFlow(
                conf, logger, cancellation_manager
            ).delete_saved_apps(actions.delete_saved_app_actions)

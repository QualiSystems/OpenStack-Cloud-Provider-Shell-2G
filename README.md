[![Build status](https://github.com/QualiSystems/OpenStack-Shell-2G/workflows/CI/badge.svg?branch=master)](https://github.com/QualiSystems/OpenStack-Shell-2G/actions?query=branch%3Amaster)

# OpenStack Cloud Provider Shell 2G
A CloudShell 'Shell' that allows integrating OpenStack as an App's deployment option in CloudShell
![Image][1]

Release date: July 2021

`Shell version: 1.0.0`

`Document version: 1.0`

# In This Guide

* [Overview](#overview)
* [Downloading the Shell](#downloading-the-shell)
* [Importing and Configuring the Shell](#importing-and-configuring-the-shell)
* [Updating Python Dependencies for Shells](#updating-python-dependencies-for-shells)
* [Typical Workflows](#typical-workflows)
* [References](#references)
* [Release Notes](#release-notes)


# Overview
A shell integrates a device model, application or other technology with CloudShell. A shell consists of a data model that defines how the device and its properties are modeled in CloudShell, along with automation that enables interaction with the device via CloudShell.

### Cloud Provider Shells
CloudShell Cloud Provider shells provide L2 or L3 connectivity between resources and/or Apps.

### OpenStack Cloud Provider Shell 2G
OpenStack Cloud Provider Shell 2G provides you with apps deployment and management capabilities. 

For more information on the device, see the vendor's official product documentation.

### Standard version
OpenStack Cloud Provider Shell 2G is based on the Cloud Provider Standard version **1.0.0**.

For detailed information about the shell’s structure and attributes, see the [Cloud Provider Standard](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md) in GitHub.

### Requirements

Release: OpenStack Cloud Provider Shell 2G

▪ CloudShell version **9.3 and above**

**Note:** If your CloudShell version does not support this shell, you should consider upgrading to a later version of CloudShell or contact customer support. 

### Data Model

The shell's data model includes all shell metadata, families, and attributes.

#### **OpenStack Cloud Provider Shell 2G Attributes**

The attribute names and types are listed in the following section of the Cloud Provider Shell Standard:

[Common Cloud Provider Attributes](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md#attributes)

The following table describes attributes that are unique to this shell and are not documented in the Shell Standard: 


|Attribute Name|Data Type|Description|
|:---|:---|:---|
|Controller URL|String|OpenStack Keystone Controller URL endpoint address. For example: http://controler:5000/v3.|
|OpenStack Domain Name|String|OpenStack domain to use.|
|OpenStack Project Name|String|OpenStack project in which CloudShell will create the instances.|
|OpenStack Management Network ID|String|UUID of the manually created CloudShell management network (for assistance identifying your management network, contact your OpenStack admin). This network will be used to configure the communication between the Sandbox instances and the CloudShell components. For example: c14241d2-376c-4fb3-8d1e-61f5c1408448. *__Note__: The UUID can be found in the Horizon user interface.*|
|Password|Password|OpenStack user's password|
|User|String|OpenStack user on the OpenStack server|
|OpenStack Reserved Networks|string|Comma separated list (,) of reserved networks. vNICs configured to these networks will not be used for instance connectivity. *__Note__: Ideally, one of the following three ranges should be free: 10.0.0.0/8, 172.16.0.0/16, 192.168.0.0/16*|
|VLAN Type|String|The VLAN technology to use for connectivity to/from this cloud provider. Options are __VLAN__ and __VXLAN__.|
|Floating IP Subnet ID|String|UUID of the external network subnet that will allocate floating IDs to the OpenStack instances, to allow external connectivity into those instances. For assistance identifying your Floating IP network, contact your OpenStack admin. For additional details, see [OpenStack Configuration Requirements](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/OpenStack-Cnfg-Rqrs.htm).|
|OpenStack Physical Interface Name|String|(Not required if you set the VLAN Type attribute to VXLAN) The physical interface mapping name to use when configuring OpenStack connectivity. The physical interface can be found under the connectivity provider configuration in your OpenStack plugin's agent file. For example: For Linux Bridge plugin, use _/etc/neutron/plugins/ml2/linuxbridge_agent.ini_ file > `[linux_bridge]` configuration section > `physical_interface_mappings` attribute. For example: `physical_interface_mappings = public:em1,office:p1p2,quali:em2`. And for Open vSwitch plugin, _/etc/neutron/plugins/ml2/openvswitch_agent.ini_ file > [ovs] configuration section > `bridge_mappings` attribute. For example: `bridge_mappings = public:br-vlan`.|
|Execution Server Selector|String|(Optional) This attribute points to a pre-defined group of execution servers (grouped by a common __Execution Server Selector__ value). This attribute is typically used for different sites or domains. For additional information on managing App deployments per domains, see [Managing Private Cloud Apps in Domains](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/Mng-Prvt-Cld-Apps-in-Dmns.htm).|

### Automation
This section describes the automation (driver) associated with the data model. The shell’s driver is provided as part of the shell package. There are two types of automation processes, Autoload and Resource. Autoload is executed when creating the resource in the **Inventory** dashboard.

For detailed information on each available commands, see the following section of the Cloud Provider Standard:

[Common Cloud Provider Commands](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md#commands)

# OpenStack Integration Process
In order to integrate CloudShell with OpenStack, you need to first prepare OpenStack with the required user permissions, quotas, networks etc. Then, create an OpenStack cloud provider resource and App templates which include the definition of the VMs, images and configuration management to be performed on the deployed VMs. For details, see CloudShell Help's [Azure Integration](https://help.quali.com/Online%20Help/0.0/portal/Content/Admn/OpenStack-Intgr) chapter.

# Downloading the Shell
The OpenStack Cloud Provider Shell 2G shell is available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shell comprises:

|File name|Description|
|:---|:---|
|OpenStack Cloud Provider Shell 2G.zip|Device shell package|
|cloudshell-openstack-dependencies-package-1.0.x.zip|Shell Python dependencies (for offline deployments only)|

# Importing and Configuring the Shell
This section describes how to import the OpenStack Cloud Provider Shell 2G shell and configure and modify the shell’s devices.

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page.
  
  2. In CloudShell Portal, as Global administrator, open the **Manage – Shells** page.
  
  3. Click **Import**.
  
  4. In the dialog box, navigate to the shell's zip package, select it and click **Open**. <br><br>The shell is displayed in the **Shells** page and can be used by domain administrators in all CloudShell domains to create new inventory resources, as explained in [Adding Inventory Resources](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Add-Rsrc-Tmplt.htm?Highlight=adding%20inventory%20resources). 

### Offline installation of a shell

**Note:** Offline installation instructions are relevant only if CloudShell Execution Server has no access to PyPi. You can skip this section if your execution server has access to PyPi. For additional information, see the online help topic on offline dependencies.

In offline mode, import the shell into CloudShell and place any dependencies in the appropriate dependencies folder. The dependencies folder may differ, depending on the CloudShell version you are using:

* For CloudShell version 8.3 and above, see [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository).

* For CloudShell version 8.2, perform the appropriate procedure: [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository) or [Setting the Python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

* For CloudShell versions prior to 8.2, see [Setting the Python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

### Adding shell and script packages to the local PyPi Server repository
If your Quali Server and/or execution servers work offline, you will need to copy all required Python packages, including the out-of-the-box ones, to the PyPi Server's repository on the Quali Server computer (by default *C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository*).

For more information, see [Configuring CloudShell to Execute Python Commands in Offline Mode](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=Configuring%20CloudShell%20to%20Execute%20Python%20Commands%20in%20Offline%20Mode).

**To add Python packages to the local PyPi Server repository:**
  1. If you haven't created and configured the local PyPi Server repository to work with the execution server, perform the steps in [Add Python packages to the local PyPi Server repository (offline mode)](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=offline%20dependencies#Add). 
  
  2. For each shell or script you add into CloudShell, do one of the following (from an online computer):
      * Connect to the Internet and download each dependency specified in the *requirements.txt* file with the following command: 
`pip download -r requirements.txt`. 
     The shell or script's requirements are downloaded as zip files.

      * In the [Quali Community's Integrations](https://community.quali.com/integrations) page, locate the shell and click the shell's **Download** link. In the page that is displayed, from the Downloads area, extract the dependencies package zip file.

3. Place these zip files in the local PyPi Server repository.
 
### Configuring a new resource
This section explains how to create a new resource from the shell.

In CloudShell, the component that models the device is called a resource. It is based on the shell that models the device and allows the CloudShell user and API to remotely control the device from CloudShell.

You can also modify existing resources, see [Managing Resources in the Inventory](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Mng-Rsrc-in-Invnt.htm?Highlight=managing%20resources).

**To create a resource for the device:**  
  1. In the CloudShell Portal, in the **Inventory** dashboard, click **Add New**.
     ![Image][2]
     
  3. From the list, select **OpenStack Cloud Provider Shell 2G**.
  
  4. Click **Create**.
  
  5. In the **Resource** dialog box, enter the following mandatory attributes with data from step 1:
        - **Controller URL** - OpenStack Keystone Controller URL endpoint address. For example: http://controler:5000/v3.
        - **OpenStack Domain Name** - OpenStack domain to use.
        - **OpenStack Project Name** - OpenStack project in which CloudShell will create the instances.
        - **OpenStack Management Network ID** - UUID of the manually created CloudShell management network (for assistance identifying your management network, contact your OpenStack admin). This network will be used to configure the communication between the Sandbox instances and the CloudShell components. For example: c14241d2-376c-4fb3-8d1e-61f5c1408448
<br>__Note__: The UUID can be found in the Horizon user interface.

        - **Password** - OpenStack user's password
        - **User** - OpenStack user on the OpenStack server
        - **OpenStack Reserved Networks** - Comma separated list (,) of reserved networks. vNICs configured to these networks will not be used for instance connectivity.
<br>__Note__: Ideally, one of the following three ranges should be free: 10.0.0.0/8, 172.16.0.0/16, 192.168.0.0/16
        - **VLAN Type** - The VLAN technology to use for connectivity to/from this cloud provider. Options are __VLAN__ and __VXLAN__.
        - **Floating IP Subnet ID** - UUID of the external network subnet that will allocate floating IDs to the OpenStack instances, to allow external connectivity into those instances. For assistance identifying your Floating IP network, contact your OpenStack admin. For additional details, see [OpenStack Configuration Requirements](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/OpenStack-Cnfg-Rqrs.htm).
        - **OpenStack Physical Interface Name** - (Not required if you set the VLAN Type attribute to VXLAN) The physical interface mapping name to use when configuring OpenStack connectivity. The physical interface can be found under the connectivity provider configuration in your OpenStack plugin's agent file. For example:
            - For Linux Bridge plugin: _/etc/neutron/plugins/ml2/linuxbridge_agent.ini_ file > [linux_bridge] configuration section > `physical_interface_mappings` attribute. For example: `physical_interface_mappings = public:em1,office:p1p2,quali:em2`.
            - For Open vSwitch plugin: _/etc/neutron/plugins/ml2/openvswitch_agent.ini_ file > [ovs] configuration section > `bridge_mappings` attribute. For example: `bridge_mappings = public:br-vlan`.
        - **Execution Server Selector** - (Optional) This attribute points to a pre-defined group of execution servers (grouped by a common __Execution Server Selector__ value). 
This attribute is typically used for different sites or domains. For additional information on managing App deployments per domains, see [Managing Private Cloud Apps in Domains](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/Mng-Prvt-Cld-Apps-in-Dmns.htm).
  6. Click **Continue**.

CloudShell validates provided settings and creates the new resource.

_**OpenStack Cloud Provider Shell 2G requires you to set up an OpenStack cloud provider resource and also create an appropriate App template, which would be deployed as part of the sandbox reservation. For details, see [OpenStack Integration](https://help.quali.com/Online%20Help/0.0/cloudshell/Content/Admn/OpenStack-Intgr.htm)**_

# Updating Python Dependencies for Shells
This section explains how to update your Python dependencies folder. This is required when you upgrade a shell that uses new/updated dependencies. It applies to both online and offline dependencies.
### Updating offline Python dependencies
**To update offline Python dependencies:**
1. Download the latest Python dependencies package zip file locally.

2. Extract the zip file to the suitable offline package folder(s). 

3. Terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat). 

### Updating online Python dependencies
In online mode, the execution server automatically downloads and extracts the appropriate dependencies file to the online Python dependencies repository every time a new instance of the driver or script is created.

**To update online Python dependencies:**
* If there is a live instance of the shell's driver or script, terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat). If an instance does not exist, the execution server will download the Python dependencies the next time a command of the driver or script runs.

# References
To download and share integrations, see [Quali Community's Integrations](https://community.quali.com/integrations). 

For instructional training and documentation, see [Quali University](https://www.quali.com/university/).

To suggest an idea for the product, see [Quali's Idea box](https://community.quali.com/ideabox). 

To connect with Quali users and experts from around the world, ask questions and discuss issues, see [Quali's Community forums](https://community.quali.com/forums). 

# Release Notes 

### What's New

For release updates, see the shell's [GitHub releases page](https://github.com/QualiSystems/OpenStack-Cloud-Provider-Shell-2G/releases).


[1]: https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/cloudshell_logo.png
[2]: https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/create_a_resource_device.png

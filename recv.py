#!/usr/bin/env python


import sys
import logging
from eventhubs import EventHubClient, Receiver, Offset
from config import ADDRESS, azure_context

from utilities import AzureContext
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ContainerGroup, Container, ContainerPort, Port, IpAddress, 
                                                 ResourceRequirements, ResourceRequests, ContainerGroupNetworkProtocol, OperatingSystemTypes)

resource_client = ResourceManagementClient(azure_context.credentials, azure_context.subscription_id)
client = ContainerInstanceManagementClient(azure_context.credentials, azure_context.subscription_id)

class MyReceiver(Receiver):
    def __init__(self, partition):
        super(MyReceiver, self).__init__()
        self.partition = partition
        self.total = 0
        self.last_sn = -1
        self.last_offset = "-1"

    def on_event_data(self, event_data):
        self.last_offset = event_data.offset
        self.last_sn = event_data.sequence_number
        self.total += 1
        print("Partition", self.partition, "Received ", self.total," sn=",self.last_sn," offset=",self.last_offset)

# try:
#     CONSUMER_GROUP = "$default"
#     OFFSET = Offset("-1")

#     EventHubClient(ADDRESS if len(sys.argv) == 1 else sys.argv[1]) \
#         .subscribe(MyReceiver("0"), CONSUMER_GROUP, "0", OFFSET) \
#         .run()

# except KeyboardInterrupt:
#     pass

def create_container_group(resource_group_name, name, location, image, memory, cpu):

   # setup default values
   port = 80
   container_resource_requirements = None
   command = None
   environment_variables = None

   # set memory and cpu
   container_resource_requests = ResourceRequests(memory_in_gb = memory, cpu = cpu)
   container_resource_requirements = ResourceRequirements(requests = container_resource_requests)
   
   container = Container(name = name,
                         image = image,
                         resources = container_resource_requirements,
                         command = command,
                         ports = [ContainerPort(port=port)],
                         environment_variables = environment_variables)

   # defaults for container group
   cgroup_os_type = OperatingSystemTypes.linux
   cgroup_ip_address = IpAddress(ports = [Port(protocol=ContainerGroupNetworkProtocol.tcp, port = port)])
   image_registry_credentials = None

   cgroup = ContainerGroup(location = location,
                           containers = [container],
                           os_type = cgroup_os_type,
                           ip_address = cgroup_ip_address,
                           image_registry_credentials = image_registry_credentials)

   client.container_groups.create_or_update(resource_group_name, name, cgroup)


create_container_group("aciherodemo", "test1", "West US", "nginx", 1, 1)

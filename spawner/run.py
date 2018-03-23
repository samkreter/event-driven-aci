#!/usr/bin/env python

from config import ADDRESS, queueConf, azure_context, AzureContext
from azure.servicebus import ServiceBusService, Message, Queue
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ContainerGroup, Container, ContainerPort, Port, IpAddress, 
                                                 ResourceRequirements, ResourceRequests, ContainerGroupNetworkProtocol, OperatingSystemTypes)

resource_client = ResourceManagementClient(azure_context.credentials, azure_context.subscription_id)
client = ContainerInstanceManagementClient(azure_context.credentials, azure_context.subscription_id)

bus_service = ServiceBusService(
    service_namespace = queueConf['service_namespace'],
    shared_access_key_name = queueConf['saskey_name'],
    shared_access_key_value = queueConf['saskey_value'])



RESOURCE_GROUP = "Test"
LOCATION = "westus"
BASE_NAME = "worker-"
IMAGE = "nginx"



#create_container_group(RESOURCE_GROUP, BASE_NAME + str(self.worker_count), LOCATION, IMAGE, )

def main():
    print("Starting Work Cycle...")
    try:
        msg = bus_service.receive_queue_message(queueConf['queue_name'], peek_lock=False)
        print(msg.body)
    except KeyboardInterrupt:
        pass


def create_container_group(resource_group_name, name, location, image, msg):

   # setup default values
   port = 80
   container_resource_requirements = None
   command = None
   environment_variables = None

   # set memory and cpu
   container_resource_requests = ResourceRequests(memory_in_gb = 3.5, cpu = 2)
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


if __name__ == '__main__':
    main()

"""
The service lists the status of all the Google Cloud compute instances connected to a particular account on a per-project,
per-zone basis. First it prints the information of network interfaces of certain machines if user wants. Then it also
prints the machine type of the instance so the user can get host machine details about the instances.

Sample usage: python3 listInstancesAndHosts.py

Sample output:

For project My Project 40050, the instances are:
+-----------------------+---------+------------+--------------+
|     Instance Name     |  Status |    Zone    | Machine Type |
+-----------------------+---------+------------+--------------+
| instance-group-1-8m82 | RUNNING | us-east1-b |   f1-micro   |
| instance-group-1-w28d | RUNNING | us-east1-b |   f1-micro   |
| instance-group-1-fknk | RUNNING | us-east1-c |   f1-micro   |
| instance-group-1-z7xs | RUNNING | us-east1-d |   f1-micro   |
+-----------------------+---------+------------+--------------+

Enter a instance name to get info about its network interfaces or c to continue: instance-group-1-8m82
Enter the zone name for the instance: us-east1-b
Network Interfaces:
[{'accessConfigs': [{'kind': 'compute#accessConfig',
                     'name': 'External NAT',
                     'natIP': '104.196.134.106',
                     'type': 'ONE_TO_ONE_NAT'}],
  'kind': 'compute#networkInterface',
  'name': 'nic0',
  'network': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/global/networks/default',
  'networkIP': '10.142.0.3',
  'subnetwork': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1/subnetworks/default'}]
Enter a instance name to get more detailed info about its network interfaces or c to continue: c

Enter a machine type to get more detailed info(host information) or c to continue: f1-micro
Enter the zone name for machine type: us-east1-b
{'creationTimestamp': '1969-12-31T16:00:00.000-08:00',
 'description': '1 vCPU (shared physical core) and 0.6 GB RAM',
 'guestCpus': 1,
 'id': '1000',
 'imageSpaceGb': 0,
 'isSharedCpu': True,
 'kind': 'compute#machineType',
 'maximumPersistentDisks': 16,
 'maximumPersistentDisksSizeGb': '3072',
 'memoryMb': 614,
 'name': 'f1-micro',
 'selfLink': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/zones/us-east1-b/machineTypes/f1-micro',
 'zone': 'us-east1-b'}
Enter a machine type to get more detailed info or c to continue: c
"""
import googleapiclient.discovery
from google.cloud import resource_manager
from prettytable import PrettyTable
from pprint import pprint

t = PrettyTable(["Instance Name", "Status", "Zone", "Machine Type"])
client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    print ("For project " + projName + ", the instances are: ")
    request = compute.zones().list(project=projId)
    while request is not None:
        response = request.execute()
        for zone in response['items']:
            zoneName = zone['name']
            instanceRequest = compute.instances().list(project=projId, zone=zoneName)
            while instanceRequest is not None:
                instanceResponse = instanceRequest.execute()
                if 'items' in instanceResponse:
                    for instance in instanceResponse['items']:
                        machineTypeUrl = instance['machineType']
                        machineTypeName = machineTypeUrl.split("/")[-1]
                        t.add_row([instance['name'], instance['status'], zoneName, machineTypeName])
                instanceRequest = compute.instances().list_next(previous_request=instanceRequest, previous_response=instanceResponse)
        request = compute.zones().list_next(previous_request=request, previous_response=response)
    print (t)
    t.clear_rows()
    user_choice = input("Enter a instance name to get info about its network interfaces or c to continue: ")
    while user_choice != "c":
        zoneName = input("Enter the zone name for the instance: ")
        request = compute.instances().get(project=projId, zone=zoneName, instance=user_choice)
        response = request.execute()
        print ("Network Interfaces: ")
        pprint(response['networkInterfaces'])
        user_choice = input("Enter a instance name to get more detailed info about its network interfaces or c to continue: ")
    user_choice = input("Enter a machine type to get more detailed info(host information) or c to continue: ")
    while user_choice != "c":
        zoneName = input("Enter the zone name for machine type: ")
        request = compute.machineTypes().get(project=projId, zone=zoneName, machineType=user_choice)
        response = request.execute()
        pprint(response)
        user_choice = input("Enter a machine type to get more detailed info(host information) or c to continue: ")

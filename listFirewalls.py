"""
The service lists all the firewall rules of Google Cloud compute projects linked to a particular account.

Sample usage: python3 listFirewalls.py

Sample output:

For project My Project 40050, the firewall rules are:
+------------------------+-------------+-----------------------------------------------+
|          Name          | Network/VPC |                  Description                  |
+------------------------+-------------+-----------------------------------------------+
|   default-allow-icmp   |   default   |            Allow ICMP from anywhere           |
| default-allow-internal |   default   | Allow internal traffic on the default network |
|   default-allow-rdp    |   default   |            Allow RDP from anywhere            |
|   default-allow-ssh    |   default   |            Allow SSH from anywhere            |
+------------------------+-------------+-----------------------------------------------+
Enter a firewall rule name to get more detailed info or c to continue: default-allow-icmp
{'allowed': [{'IPProtocol': 'icmp'}],
 'creationTimestamp': '2018-01-17T07:09:49.421-08:00',
 'description': 'Allow ICMP from anywhere',
 'direction': 'INGRESS',
 'id': '4500073023364323794',
 'kind': 'compute#firewall',
 'name': 'default-allow-icmp',
 'network': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/global/networks/default',
 'priority': 65534,
 'selfLink': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/global/firewalls/default-allow-icmp',
 'sourceRanges': ['0.0.0.0/0']}
Enter a firewall rule name to get more detailed info or c to continue: c
"""

import googleapiclient.discovery
from google.cloud import resource_manager
from pprint import pprint
from prettytable import PrettyTable

t = PrettyTable(["Name", "Network/VPC", "Description"])
client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = compute.firewalls().list(project=projId)
    print ("For project " + projName + ", the firewall rules are:")
    while request is not None:
        response = request.execute()
        for firewall in response['items']:
            networkUrl = firewall['network']
            networkName = (networkUrl.split("/"))[-1]
            t.add_row([firewall['name'], networkName, firewall['description']])
        request = compute.firewalls().list_next(previous_request=request, previous_response=response)
    print (t)
    t.clear_rows()
    user_choice = input("Enter a firewall rule name to get more detailed info or c to continue: ")
    while user_choice != "c":
        request = compute.firewalls().get(project=projId, firewall=user_choice)
        response = request.execute()
        pprint(response)
        user_choice = input("Enter a firewall rule name to get more detailed info or c to continue: ")

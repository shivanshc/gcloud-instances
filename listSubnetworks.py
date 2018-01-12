"""
The service lists all the subnets in Google cloud compute projects to a particular account on a per-project basis.
It also has the option to get detailed information about a particular subnet in a certain region.

Sample usage: python3 listSubnetworks.py

Sample output:

For project My First Project, the subnetworks are:
+---------+-------------------------+-------------+
|   Name  |       Region Name       | Network/VPC |
+---------+-------------------------+-------------+
| default |        asia-east1       |   default   |
| default |     asia-northeast1     |   default   |
| default |       asia-south1       |   default   |
| default |     asia-southeast1     |   default   |
| default |   australia-southeast1  |   default   |
| default |       europe-west1      |   default   |
| default |       europe-west2      |   default   |
| default |       europe-west3      |   default   |
| default | northamerica-northeast1 |   default   |
| default |    southamerica-east1   |   default   |
| default |       us-central1       |   default   |
| default |         us-east1        |   default   |
| default |         us-east4        |   default   |
| default |         us-west1        |   default   |
+---------+-------------------------+-------------+
Enter a subnetwork name to get more detailed info or c to continue: Enter the region name for the chosen subnetwork: {'creationTimestamp': '2017-12-21T15:31:25.355-08:00',
 'gatewayAddress': '10.142.0.1',
 'id': '896079670801463970',
 'ipCidrRange': '10.142.0.0/20',
 'kind': 'compute#subnetwork',
 'name': 'default',
 'network': 'https://www.googleapis.com/compute/v1/projects/graceful-tenure-189823/global/networks/default',
 'privateIpGoogleAccess': False,
 'region': 'https://www.googleapis.com/compute/v1/projects/graceful-tenure-189823/regions/us-east1',
 'selfLink': 'https://www.googleapis.com/compute/v1/projects/graceful-tenure-189823/regions/us-east1/subnetworks/default'}
Enter a subnetwork name to get more detailed info or c to continue:c
"""

import googleapiclient.discovery
from google.cloud import resource_manager
from pprint import pprint
from prettytable import PrettyTable

t = PrettyTable(["Name", "Region Name", "Network/VPC"])
client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = compute.regions().list(project=projId)
    print ("For project " + projName + ", the subnetworks are:")
    while request is not None:
        response = request.execute()
        for regionItem in response['items']:
            regionName = regionItem['name']
            subnetRequest = compute.subnetworks().list(project=projId, region=regionName)
            while subnetRequest is not None:
                subnetResponse = subnetRequest.execute()
                if 'items' in subnetResponse:
                    for subnet in subnetResponse['items']:
                        networkUrl = subnet['network']
                        networkName = (networkUrl.split("/"))[-1]
                        t.add_row([subnet['name'], regionName, networkName])
                subnetRequest = compute.routes().list_next(previous_request=subnetRequest, previous_response=subnetResponse)
        request = compute.routes().list_next(previous_request=request, previous_response=response)
    print (t)
    t.clear_rows()
    user_choice = input("Enter a subnetwork name to get more detailed info or c to continue: ")
    while user_choice != "c":
        regionName = input("Enter the region name for the chosen subnetwork: ")
        request = compute.subnetworks().get(project=projId, region=regionName, subnetwork=user_choice)
        response = request.execute()
        pprint(response)
        user_choice = input("Enter a subnetwork name to get more detailed info or c to continue: ")

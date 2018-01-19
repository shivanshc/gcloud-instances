"""
Target pools are used for load balancing in a google cloud project.
This service lists all the target pools in a Google Cloud project on a per-region basis for all the projects
associated with an account. It also allows you to get detailed info about a target pool if required.

Sample usage: python3 listPools.py

Sample output:

For project My Project 40050, the target pools are:
+------------------+-------------+-------------+
| Target Pool Name | Region Name | Description |
+------------------+-------------+-------------+
|   sample-pool    |   us-east1  |             |
+------------------+-------------+-------------+
Enter a target pool name to get more detailed info or c to continue: sample-pool
Enter the region name for the chosen pool: us-east1
{'creationTimestamp': '2018-01-18T18:04:18.975-08:00',
 'description': '',
 'id': '5466791649689267405',
 'instances': ['https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/zones/us-east1-b/instances/instance-group-1-9vds',
               'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/zones/us-east1-b/instances/instance-group-1-h3cq'],
 'kind': 'compute#targetPool',
 'name': 'sample-pool',
 'region': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1',
 'selfLink': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1/targetPools/sample-pool',
 'sessionAffinity': 'NONE'}
Enter a target pool name to get more detailed info or c to continue:c
"""

import googleapiclient.discovery
from google.cloud import resource_manager
from pprint import pprint
from prettytable import PrettyTable

t = PrettyTable(["Target Pool Name", "Region Name", "Description"])
client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = compute.regions().list(project=projId)
    print ("For project " + projName + ", the target pools are:")
    while request is not None:
        response = request.execute()
        for regionItem in response['items']:
            regionName = regionItem['name']
            poolRequest = compute.targetPools().list(project=projId, region=regionName)
            while poolRequest is not None:
                poolResponse = poolRequest.execute()
                if 'items' in poolResponse:
                    for pool in poolResponse['items']:
                        name = pool['name']
                        description = pool['description']
                        t.add_row([name, regionName, description])
                poolRequest = compute.targetPools().list_next(previous_request=poolRequest, previous_response=poolResponse)
        request = compute.regions().list_next(previous_request=request, previous_response=response)
    print (t)
    t.clear_rows()
    user_choice = input("Enter a target pool name to get more detailed info or c to continue: ")
    while user_choice != "c":
        regionName = input("Enter the region name for the chosen pool: ")
        request = compute.targetPools().get(project=projId, region=regionName, targetPool=user_choice)
        response = request.execute()
        pprint(response)
        user_choice = input("Enter a target pool name to get more detailed info or c to continue: ")

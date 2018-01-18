"""
The service lists all the VPCs/Networks present in a single project for all the projects associated with the
GCloud account in user. It also has the option of printing detailed info about a VPC if required.

Sample usage: python3 listVPCs.py

Sample output:

"""

import googleapiclient.discovery
from google.cloud import resource_manager
from pprint import pprint
from prettytable import PrettyTable

t = PrettyTable(["Name", "Description"])
client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = compute.networks().list(project=projId)
    print ("For project " + projName + ", the Networks are:")
    while request is not None:
        response = request.execute()
        for network in response['items']:
            t.add_row([network['name'], network['description']])
        request = compute.routes().list_next(previous_request=request, previous_response=response)
    print (t)
    t.clear_rows()
    user_choice = input("Enter a VPC/Network name to get more detailed info or c to continue: ")
    while user_choice != "c":
        request = compute.networks().get(project=projId, network=user_choice)
        response = request.execute()
        pprint(response)
        user_choice = input("Enter a VPC/Network name to get more detailed info or c to continue: ")

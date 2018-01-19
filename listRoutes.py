"""
The service lists all the route instances Google Cloud compute projects connected to a particular account on a per-project
basis. It also has the option to get detailed information for a particular route.

Sample usage: python3 listRoutes.py

Sample output:

For project My First Project, the routes are:
+--------------------------------+-------------+------------------------------------------------------+
|              Name              | Network/VPC |                     Description                      |
+--------------------------------+-------------+------------------------------------------------------+
| default-route-000c2ffea1a3b74f |   default   | Default local route to the subnetwork 10.156.0.0/20. |
| default-route-27c98bdc1308646b |   default   | Default local route to the subnetwork 10.148.0.0/20. |
| default-route-2ba5a867e231163c |   default   |            Default route to the Internet.            |
| default-route-38f127b3e5fcef31 |   default   | Default local route to the subnetwork 10.132.0.0/20. |
| default-route-43187929aa046623 |   default   | Default local route to the subnetwork 10.162.0.0/20. |
| default-route-55b6f03e71e44fe8 |   default   | Default local route to the subnetwork 10.158.0.0/20. |
| default-route-5924db1d8a1b1a70 |   default   | Default local route to the subnetwork 10.142.0.0/20. |
| default-route-64e9fe257d64b894 |   default   | Default local route to the subnetwork 10.150.0.0/20. |
| default-route-73e360764ec1b366 |   default   | Default local route to the subnetwork 10.138.0.0/20. |
| default-route-aca1086e52c7897b |   default   | Default local route to the subnetwork 10.152.0.0/20. |
| default-route-bbf7cc6922b47f7a |   default   | Default local route to the subnetwork 10.154.0.0/20. |
| default-route-c269f41ef99eed87 |   default   | Default local route to the subnetwork 10.146.0.0/20. |
| default-route-cdc74b41a989596e |   default   | Default local route to the subnetwork 10.140.0.0/20. |
| default-route-f7ce6e8de1086133 |   default   | Default local route to the subnetwork 10.160.0.0/20. |
| default-route-f9c9db6ca9465e9e |   default   | Default local route to the subnetwork 10.128.0.0/20. |
+--------------------------------+-------------+------------------------------------------------------+
Enter a route name to get more detailed info or c to continue: default-route-64e9fe257d64b894
{'creationTimestamp': '2017-12-21T15:31:29.860-08:00',
 'description': 'Default local route to the subnetwork 10.150.0.0/20.',
 'destRange': '10.150.0.0/20',
 'id': '774197814725049022',
 'kind': 'compute#route',
 'name': 'default-route-64e9fe257d64b894',
 'network': 'https://www.googleapis.com/compute/v1/projects/graceful-tenure-189823/global/networks/default',
 'nextHopNetwork': 'https://www.googleapis.com/compute/v1/projects/graceful-tenure-189823/global/networks/default',
 'priority': 1000,
 'selfLink': 'https://www.googleapis.com/compute/v1/projects/graceful-tenure-189823/global/routes/default-route-64e9fe257d64b894'}
Enter a route name to get more detailed info or c to continue:c
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
    request = compute.routes().list(project=projId)
    print ("For project " + projName + ", the routes are:")
    while request is not None:
        response = request.execute()
        for route in response['items']:
            networkUrl = route['network']
            networkName = (networkUrl.split("/"))[-1]
            t.add_row([route['name'], networkName, route['description']])
        request = compute.routes().list_next(previous_request=request, previous_response=response)
    print (t)
    t.clear_rows()
    user_choice = input("Enter a route name to get more detailed info or c to continue: ")
    while user_choice != "c":
        request = compute.routes().get(project=projId, route=user_choice)
        response = request.execute()
        pprint(response)
        user_choice = input("Enter a route name to get more detailed info or c to continue: ")

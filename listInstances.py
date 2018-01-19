"""
The service lists the status of all the Google Cloud compute instances connected to a particular account on a per-project,
per-zone basis.

Sample usage: python3 listInstances.py

Sample output:

For project My First Project, the instances in zone us-east1-b are:
+---------------------+------------+
|    Instance Name    |   Status   |
+---------------------+------------+
| instance-template-1 | TERMINATED |
| instance-template-2 | TERMINATED |
| instance-template-3 | TERMINATED |
+---------------------+------------+
"""
import googleapiclient.discovery
from google.cloud import resource_manager
from prettytable import PrettyTable

t = PrettyTable(["Instance Name", "Status"])
client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = compute.zones().list(project=projId)
    while request is not None:
        response = request.execute()
        for zone in response['items']:
            zoneName = zone['name']
            instanceRequest = compute.instances().list(project=projId, zone=zoneName)
            while instanceRequest is not None:
                instanceResponse = instanceRequest.execute()
                if 'items' in instanceResponse:
                    print ("For project " + projName + ", the instances in zone " + zoneName + " are: ")
                    for instance in instanceResponse['items']:
                        t.add_row([instance['name'], instance['status']])
                    print (t)
                    t.clear_rows()
                instanceRequest = compute.instances().list_next(previous_request=instanceRequest, previous_response=instanceResponse)
        request = compute.zones().list_next(previous_request=request, previous_response=response)

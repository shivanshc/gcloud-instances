"""
The service lists all the regions and zones available to each project connected to a google cloud platform
account.

Sample usage: python3 listRegionsAndZones.py

Sample output:

For project, My Project 40050 the availability zones and their corresponding regions are:
+---------------------------+-------------------------+
|            Zone           |          Region         |
+---------------------------+-------------------------+
|         us-east1-b        |         us-east1        |
|         us-east1-c        |         us-east1        |
|         us-east1-d        |         us-east1        |
|         us-east4-c        |         us-east4        |
|         us-east4-b        |         us-east4        |
|         us-east4-a        |         us-east4        |
|       us-central1-c       |       us-central1       |
|       us-central1-a       |       us-central1       |
|       us-central1-f       |       us-central1       |
|       us-central1-b       |       us-central1       |
|         us-west1-b        |         us-west1        |
|         us-west1-c        |         us-west1        |
|         us-west1-a        |         us-west1        |
|       europe-west4-b      |       europe-west4      |
|       europe-west4-c      |       europe-west4      |
|       europe-west1-b      |       europe-west1      |
|       europe-west1-d      |       europe-west1      |
|       europe-west1-c      |       europe-west1      |
|       europe-west3-b      |       europe-west3      |
|       europe-west3-c      |       europe-west3      |
|       europe-west3-a      |       europe-west3      |
|       europe-west2-c      |       europe-west2      |
|       europe-west2-b      |       europe-west2      |
|       europe-west2-a      |       europe-west2      |
|        asia-east1-b       |        asia-east1       |
|        asia-east1-a       |        asia-east1       |
|        asia-east1-c       |        asia-east1       |
|     asia-southeast1-b     |     asia-southeast1     |
|     asia-southeast1-a     |     asia-southeast1     |
|     asia-northeast1-b     |     asia-northeast1     |
|     asia-northeast1-c     |     asia-northeast1     |
|     asia-northeast1-a     |     asia-northeast1     |
|       asia-south1-c       |       asia-south1       |
|       asia-south1-b       |       asia-south1       |
|       asia-south1-a       |       asia-south1       |
|   australia-southeast1-b  |   australia-southeast1  |
|   australia-southeast1-c  |   australia-southeast1  |
|   australia-southeast1-a  |   australia-southeast1  |
|    southamerica-east1-b   |    southamerica-east1   |
|    southamerica-east1-c   |    southamerica-east1   |
|    southamerica-east1-a   |    southamerica-east1   |
| northamerica-northeast1-a | northamerica-northeast1 |
| northamerica-northeast1-b | northamerica-northeast1 |
| northamerica-northeast1-c | northamerica-northeast1 |
+---------------------------+-------------------------+
"""
import googleapiclient.discovery
from google.cloud import resource_manager
from prettytable import PrettyTable

t = PrettyTable(["Zone", "Region"])
client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = compute.zones().list(project=projId)
    print ("For project, " + projName + " the availability zones and their corresponding regions are:")
    while request is not None:
        response = request.execute()
        for zone in response['items']:
            zoneName = zone['name']
            regionUrl = zone['region']
            regionName = regionUrl.split('/')[-1]
            t.add_row([zoneName, regionName])
        request = compute.zones().list_next(previous_request=request, previous_response=response)
    print (t)
    t.clear_rows()

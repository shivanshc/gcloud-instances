import googleapiclient.discovery
from google.cloud import resource_manager
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
                    print ("\t"+"instanceName"+"\t"+"Status")
                    for instance in instanceResponse['items']:
                        print("\t"+instance['name'], instance['status'])
                instanceRequest = compute.instances().list_next(previous_request=instanceRequest, previous_response=instanceResponse)
        request = compute.zones().list_next(previous_request=request, previous_response=response)

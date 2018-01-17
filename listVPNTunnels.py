"""
The service lists all the VPN tunnels created or connected to a Google Cloud project for all the projects associated 
with an account.

Sample usage: python3 listVPNTunnels.py

Sample output:

For project My Project 40050, the VPN tunnels in regionus-east1 are:
{'creationTimestamp': '2018-01-17T07:40:10.744-08:00',
 'description': '',
 'detailedStatus': 'No incoming packets from peer',
 'id': '12345',
 'ikeVersion': 2,
 'kind': 'compute#vpnTunnel',
 'localTrafficSelector': ['0.0.0.0/0'],
 'name': 'vpn-2-tunnel-1',
 'peerIp': '127.0.0.1',
 'region': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1',
 'selfLink': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1/vpnTunnels/vpn-2-tunnel-1',
 'sharedSecret': '*************',
 'sharedSecretHash': 'HelloWorld',
 'status': 'NO_INCOMING_PACKETS',
 'targetVpnGateway': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1/targetVpnGateways/vpn-2'}

"""
import googleapiclient.discovery
from google.cloud import resource_manager
from prettytable import PrettyTable
from pprint import pprint

client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = compute.regions().list(project=projId)
    while request is not None:
        response = request.execute()
        for region in response['items']:
            regionName = region['name']
            vpnRequest = compute.vpnTunnels().list(project=projId, region=regionName)
            while vpnRequest is not None:
                vpnResponse = vpnRequest.execute()
                if 'items' in vpnResponse:
                    print ("For project " + projName + ", the VPN tunnels in region " + regionName + " are: ")
                    for vpnTunnel in vpnResponse['items']:
                        pprint(vpnTunnel)
                vpnRequest = compute.vpnTunnels().list_next(previous_request=vpnRequest, previous_response=vpnResponse)
        request = compute.regions().list_next(previous_request=request, previous_response=response)

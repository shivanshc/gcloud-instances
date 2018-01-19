"""
The service lists all the VPN tunnels created or connected to a Google Cloud project for all the projects associated with the account.

Sample usage: python3 listVPNTunnels.py

Sample output:

For project My Project 40050, the VPN tunnels are:
+-----------------+-------------+-------------+
| VPN Tunnel Name | Region Name | Description |
+-----------------+-------------+-------------+
|  vpn-2-tunnel-1 |   us-east1  |             |
+-----------------+-------------+-------------+
Enter a VPN tunnel name to get more detailed info or c to continue: vpn-2-tunnel-1
Enter the region name for the chosen pool: us-east1
{'creationTimestamp': '2018-01-17T07:40:10.744-08:00',
 'description': '',
 'detailedStatus': 'No incoming packets from peer',
 'id': '3979416647993839797',
 'ikeVersion': 2,
 'kind': 'compute#vpnTunnel',
 'localTrafficSelector': ['0.0.0.0/0'],
 'name': 'vpn-2-tunnel-1',
 'peerIp': '35.194.137.221',
 'region': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1',
 'selfLink': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1/vpnTunnels/vpn-2-tunnel-1',
 'sharedSecret': '*************',
 'sharedSecretHash': 'AH2iNNV7JY3AnmLMl6HSGe-H0dEz',
 'status': 'NO_INCOMING_PACKETS',
 'targetVpnGateway': 'https://www.googleapis.com/compute/v1/projects/lyrical-diagram-192415/regions/us-east1/targetVpnGateways/vpn-2'}
Enter a VPN tunnel name to get more detailed info or c to continue:c
"""

import googleapiclient.discovery
from google.cloud import resource_manager
from prettytable import PrettyTable
from pprint import pprint
t = PrettyTable(["VPN Tunnel Name", "Region Name", "Description"])
client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = compute.regions().list(project=projId)
    print ("For project " + projName + ", the VPN tunnels are:")
    while request is not None:
        response = request.execute()
        for regionItem in response['items']:
            regionName = regionItem['name']
            vpnRequest = compute.vpnTunnels().list(project=projId, region=regionName)
            while vpnRequest is not None:
                vpnResponse = vpnRequest.execute()
                if 'items' in vpnResponse:
                    for vpnTunnel in vpnResponse['items']:
                        name = vpnTunnel['name']
                        description = vpnTunnel['description']
                        t.add_row([name, regionName, description])
                vpnRequest = compute.vpnTunnels().list_next(previous_request=vpnRequest, previous_response=vpnResponse)
        request = compute.regions().list_next(previous_request=request, previous_response=response)
    print (t)
    t.clear_rows()
    user_choice = input("Enter a VPN tunnel name to get more detailed info or c to continue: ")
    while user_choice != "c":
        regionName = input("Enter the region name for the chosen pool: ")
        request = compute.vpnTunnels().get(project=projId, region=regionName, vpnTunnel=user_choice)
        response = request.execute()
        pprint(response)
        user_choice = input("Enter a VPN tunnel name to get more detailed info or c to continue: ")

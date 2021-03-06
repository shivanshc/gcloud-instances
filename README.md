# gcloud-helper

The different gcloud utilities simplify access to some important information for a particular google cloud account on a per-project basis. All the .py files have a description, sample usage and sample output at the top of the file. The different utilities are summarised below too:

listInstancesAndHosts.py : It can be used to list all the instances connected to a gcloud account along with their status on a per-project, per-zone basis. It also prints the machine type of the instances so users can get more detailed host information about any machine type. Finally, it also has the option to print network interfaces of any given instance name.

listRoutes.py: It can be used to list all the route (routing table entries) for all the projects connected to a gcloud account on a per-project basis. It also has the option of getting extensive details of a route if required.

listSubnetworks.py: It can be used to list all the subnetworks(subnets) for all the projects connected to a gcloud account on a per-project, per-region basis. It also has the option of getting extensive details of a subnet if required.

listRoles.py: It can be used to list all the security roles of all the google cloud projects tied to a certain account. It also prints the info about who is assigned to what role and has the option to get more detailed info about any role if required.

listVPNTunnels.py: It can be used to list all the VPN tunnels which are connected to a project for all the projects associated with the google cloud account being used. It prints all the relevant info for a VPN tunnel.

listVPCs.py: It can be used to list all the VPCs/Networks belonging to a certain project for all projects linked to an account. We can also use it to print detailed info about a certain VPC.

listPools.py: It can be used to list all the target pools belonging for all the projects linked to an account. It can also be used to get detailed info regarding a target pool if required. Note: Target pools are used for network load balancing and thus, this essentially gives information about load balancing.

listRegionsAndZones.py: This service lists all the available regions and zones to a particular project.

listFirewalls.py: It prints a table with all the firewall rules associated with google cloud projects connected to a certain account.

### Setup Instructions
1. Clone this git repositroy.
2. Install the python dependencies using (Could be done in a virtualenv if you wish)
     ```  python
     pip install -r requirements.txt
     ```
3. Setup google authentication credentials by following the setup steps of condition 1 under "How the Application Default Credentials work" from [here](https://developers.google.com/identity/protocols/application-default-credentials)
4. Then simply run one of the applications, for example listInstances.py, using
     ```  python
     python3 listInstances.py
     ```
5. The first time you run the application it might give you an error saying your project does not have the API enabled and would give you a link where you can set up the API access. After doing that, run the application again.

# gcloud-helper

The different gcloud utilities simplify access to some important information for a particular google cloud account on a per-project basis. All the .py files have a description, sample usage and sample output at the top of the file. The different utilities are summarised below too:

listInstances.py : It can be used to list all the instances connected to a gcloud account along with their status on a per-project, per-zone basis.

listRoutes.py: It can be used to list all the route (routing table entries) for all the projects connected to a gcloud account on a per-project basis. It also has the option of getting extensive details of a route if required.

listSubnetworks.py: It can be used to list all the subnetworks(subnets) for all the projects connected to a gcloud account on a per-project, per-region basis. It also has the option of getting extensive details of a subnet if required.

listRoles.py: It can be used to list all the security roles of all the google cloud projects tied to a certain account. It also prints the info about who is assigned to what role and has the option to get more detailed info about any role if required.

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

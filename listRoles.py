"""
The service lists the IAM policy of every Google cloud project associated with an account. IAM policy refers to Identity and Access Management policy which is used to check who has access to what in a project. It also has the option to get a detailed information about a certain role.

Sample usage: python3 listRoles.py

Sample output:
For project My First Project, the IAM policy is:
{'bindings': [{'members': ['serviceAccount:912024285956-compute@developer.gserviceaccount.com',
                           'serviceAccount:912024285956@cloudservices.gserviceaccount.com'],
               'role': 'roles/editor'},
              {'members': ['user:schandnani@outlook.com'],
               'role': 'roles/owner'}],
 'etag': 'BwVg4hcfVKk=',
 'version': 1}
Enter a role name to get more detailed info or c to continue: roles/editor
{'description': 'Edit access to all resources.',
 'etag': 'AA==',
 'includedPermissions': ['appengine.applications.get',
                         'appengine.applications.list',
                         'appengine.applications.update',
                         'appengine.instances.delete',
                         'appengine.instances.get',
                         'appengine.instances.list',
                         'appengine.instances.update',
                         .
                         .
                         .
                         .
                         .
                         'bigtable.clusters.update',
                         'bigtable.instances.create',
                         'bigtable.instances.delete',
                         'storage.buckets.delete',
                         'storage.buckets.list'],
 'name': 'roles/editor',
 'stage': 'GA',
 'title': 'Editor'}
Enter a role name to get more detailed info or c to continue:c

"""

import googleapiclient.discovery
from google.cloud import resource_manager
from pprint import pprint
from prettytable import PrettyTable

client = resource_manager.Client()
compute = googleapiclient.discovery.build('compute', 'v1')
rm = googleapiclient.discovery.build('cloudresourcemanager', 'v1')
iam = googleapiclient.discovery.build('iam', 'v1')

for project in client.list_projects():
    projId = project.project_id
    projName = project.name
    request = rm.projects().getIamPolicy(resource=projId, body={})
    response = request.execute()
    print ("For project " + projName + ", the IAM policy is:")
    pprint(response)
    user_choice = input("Enter a role name to get more detailed info or c to continue: ")
    while user_choice != "c":
        request = iam.roles().get(name=user_choice)
        response = request.execute()
        pprint(response)
        user_choice = input("Enter a role name to get more detailed info or c to continue: ")

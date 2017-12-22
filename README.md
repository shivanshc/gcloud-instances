# gcloud-instances
The service lists the status of all the Google Cloud compute instances connected to a particular account on a per-project, per-zone basis.

### Setup Instructions
1. Clone this git repositroy.
2. Install the python dependencies using (Could be done in a virtualenv if you wish)
     ```  python
     pip install -r requirements.txt
     ```
3. Setup google authentication credentials by following the setup steps of condition 1 under "How the Application Default Credentials work" from [here](https://developers.google.com/identity/protocols/application-default-credentials)
4. Then simply run the application using
 ```  python
     python3 listInstances.py
 ```
5. The first time you run the application it might give you an error saying your project does not have the API enabled and would give you a link where you can set up the API access. After doing that, run the application again.

Sample output:
```
For project My First Project, the instances in zone us-east1-b are:
	instanceName	Status
	instance-template-1 TERMINATED
	instance-template-2 RUNNING
	instance-template-3 TERMINATED
```

import requests


# Define your tenant , Service Principal Creds , preferably import this from a HSM
tenant_id = "<Enter your tenant ID here>"
client_id = "<Enter your client ID here>"
client_secret = "<Enter your client secret here>"


# This piece fetches your Service Principal Token 
url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

headers = {
             'Content-Type': 'application/x-www-form-urlencoded'
        }

body = {
         'grant_type': 'client_credentials',
         'client_id': client_id,
         'client_secret': client_secret,
         'scope': 'https://api.fabric.microsoft.com/.default'
        }
        
response = requests.post(url, headers=headers, data=body)

# token for your SPN
spn_token = response.json()['access_token']


# This part , triggers the notebook using SPN
workspace_id = "<Enter your workspace ID here>"
notebook_id = "<Enter your notebook ID here>"
default_lakehouse_name = "<Enter your default lakehouse name here>"
lakehouse_id = "<Enter your lakehouse ID here>"

headers = {

            "Authorization": f"Bearer {spn_token}",
            "Content-Type": "application/json"
        }

body = {
    "executionData": {
            
            "defaultLakehouse": {
                "name": default_lakehouse_name,
                "id": lakehouse_id,
                "workspaceId": workspace_id
            },
            "useStarterPool": False
        }
    }


url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{notebook_id}/jobs/instances?jobType=RunNotebook"
response = requests.post(url,headers=headers,json=body)

# 202 indicates a succesful trigger	
print(response.raw.status)
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


# This part , triggers the pipeline using SPN 

workspace_id = "<enter your workspace ID here>"
pipeline_id = "<enter your pipeline ID here>" 

headers = {
        "Authorization": f"Bearer {spn_token}",
        "Content-Type": "application/json"
    }

# This is the body of the request, you can add parameters as per your pipeline requirements
body = {
        "executionData": { 
            "parameters": {
                "param_waitsec": "10"  # Example parameter
            } 
        } 
    }

# Define the URL for the API endpoint
url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items/{pipeline_id}/jobs/instances?jobType=Pipeline"

    # Make the POST request to trigger the pipeline
response = requests.post(url, headers=headers, json=body)

# 202 indicates a succesful trigger
print(response.raw.status)    
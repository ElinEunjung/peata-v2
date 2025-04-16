import requests

"""Delete this file in Production"""

    #Obtain a client access token, add this to the authorization header
     #TODO use user parameters instead
     
def obtain_access_token(client_key, client_secret):
    url = "https://open.tiktokapis.com/v2/oauth/token/"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_key': client_key,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get("access_token")
    return None
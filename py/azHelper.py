#region
'''
=============================================================================
THIS CODE-SAMPLE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER
EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.

This sample is not supported under any Microsoft standard support program or
service. The code sample is provided AS IS without warranty of any kind.
Microsoft further disclaims all implied warranties including, without
limitation, any implied warranties of merchantability or of fitness for a
particular purpose. The entire risk arising out of the use or performance of
the sample and documentation remains with you. In no event shall Microsoft,
its authors, or anyone else involved in the creation, production, or delivery
of the script be liable for any damages whatsoever (including, without
limitation, damages for loss of business profits, business interruption, loss
of business information, or other pecuniary loss) arising out of  the use of
or inability to use the sample or documentation, even if Microsoft has been
advised of the possibility of such damages.
=============================================================================
'''
#endregion

import requests
import adal
from msrestazure.azure_active_directory import AADTokenCredentials

'''
Get SPN token using tenant id, client id and client secret,
we need two types of audience, one for graph and one for https://management.azure.com/
'''

def get_sp_token(tenant, client_id, client_secret, auidience):

    grant_type = 'client_credentials'
    headers =   {"ContentType":'application/x-www-form-urlencoded',
                "cache-control": 'no-cache'}

    body = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&resource={auidience}"

    uri = f'https://login.windows.net/{tenant}/oauth2/token'

    return (requests.post(uri, data=body, headers=headers).json())["access_token"]

'''
Resolve owner id from upn, we need token with graph audience
to resolve id SPN needs read access to Azure AD
'''
def get_id_from_upn(token, tenant, owner_mail):
    headers = {"Authorization": 'Bearer ' + token,
                "ContentType": 'application/json'}

    uri = f'https://graph.microsoft.com/v1.0/users/{owner_mail}'

    return requests.get(uri, headers=headers).json()["id"]

'''
Execute REST Request
'''
def exec_REST(token, method_name, exec_URI, body = None):
    headers = {"Authorization": 'Bearer ' + token,
               "ContentType": 'application/json'}
    response = getattr(requests, method_name)(exec_URI, headers=headers, json=body)#.json()
    if response.status_code == 204: #no content
        ret_val = None
    else:
        ret_val = response.json()

    return ret_val

'''
Get principal id from object id
'''
def get_principalId(token, tenant, client_id):
    base_URI = "https://graph.windows.net/"
    filter_URI = f"filter=appID eq '{client_id}'"
    apiVer_URI = "&api-version=1.6"
    def_URI = f"{base_URI}{tenant}/servicePrincipals?${filter_URI}{apiVer_URI}"
    method_name = "get"
    output = exec_REST(token, method_name, def_URI)
    return output["value"][0]["objectId"]

'''
Authenticate the end-user using device auth.
'''
def authenticate_device_code(tenant):
    authority_host_uri = 'https://login.microsoftonline.com'
    authority_uri = f"{authority_host_uri}/{tenant}"
    resource_uri = 'https://management.core.windows.net/'
    client_id = '04b07795-8ddb-461a-bbee-02f9e1bf7b46' #azure cli app id

    context = adal.AuthenticationContext(authority_uri)
    code = context.acquire_user_code(resource_uri, client_id)
    print(code['message'])
    token = context.acquire_token_with_device_code(resource_uri, code, client_id)
    return token["accessToken"]

'''
Get all user props using Graph
'''
def get_user_props(token, tenant, upn, props):
    base_url = "https://graph.microsoft.com/v1.0/users/"
    url_str = f"{base_url}{upn}?$select={props}"
    return exec_REST(token, "get", url_str)

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

import azHelper
import os

'''
Get Role Definition ID
'''
def get_roleDefinitionId(token, role_name, subscription_id):
    base_URI = "https://management.azure.com//subscriptions"
    filter_URI = f"filter=roleName eq '{role_name}'"
    def_URI = f"{base_URI}/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions?${filter_URI}&api-version=2018-01-01-preview"
    method_name = "get"
    print(def_URI)
    output = azHelper.exec_REST(token, method_name, def_URI)
    return output["value"][0]["id"], output["value"][0]["name"]


'''
Grant RBAC Access
'''
def grant_access(token, sub_id, name, role_definition_id, owner_id):
    base_URI = f"https://management.azure.com//subscriptions/{sub_id}"
    suffix_URI =f"/providers/Microsoft.Authorization/roleAssignments/{name}?api-version=2018-01-01-preview"
    acc_URI = base_URI + suffix_URI
    body = {"properties": {"roleDefinitionId":role_definition_id, "principalId":owner_id}}
    method_name = "put"
    return azHelper.exec_REST(token, method_name, acc_URI, body=body)


'''
List RBAC Access
'''
def list_access(token, sub_id, owner_id):
    base_URI = f"https://management.azure.com//subscriptions/{sub_id}/providers/Microsoft.Authorization/roleAssignments?$"
    filter_URI = f"filter=principalId eq '{owner_id}'"
    api_URI = "&api-version=2018-01-01-preview"
    list_URI = base_URI + filter_URI + api_URI
    method_name = "get"
    return azHelper.exec_REST(token, method_name, list_URI)["value"]


'''
Remove RBAC Access
'''
def remove_access(token, role_definition_id):
    base_URI = "https://management.azure.com/"
    apiVer_URI = "?api-version=2018-01-01-preview"
    remove_URI = f"{base_URI}{role_definition_id}{apiVer_URI}"
    method_name = "delete"
    return azHelper.exec_REST(token, method_name, remove_URI)


#region main
if __name__ == '__main__':
    tenant = os.environ["D_AZURE_TENANT_ID"]
    client_id = os.environ["D_AZURE_CLIENT_ID"]
    client_secret =  os.environ["D_AZURE_CLIENT_SECRET"]
    #print(client_secret)
    sub_id = os.environ["SINERGIJA_SUB_ID"]
    azure_audience = "https://management.azure.com/"
    graph_audience = "https://graph.microsoft.com/"
    owner_mail = "test@dzelenicwindowslive.onmicrosoft.com"

    azure_token = azHelper.get_sp_token(tenant, client_id, client_secret, azure_audience)
    #print(azure_token)
    graph_token = azHelper.get_sp_token(tenant, client_id, client_secret, graph_audience)
    #print(graph_token)
    owner_id = azHelper.get_id_from_upn(graph_token, tenant, owner_mail)
    print(f"Object ID za {owner_mail}: {owner_id}")

    role_name = input("Role Name:")
    role_definition_id, name = get_roleDefinitionId(azure_token, role_name, sub_id)
    print(f"Role definition za {role_name}: {role_definition_id}")

    response = grant_access(azure_token, sub_id, name, role_definition_id, owner_id)
    print(response)
#endregion
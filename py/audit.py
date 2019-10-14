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

#import json
import azHelper
import os

'''
Call the Tenant Activity Log API to see activities
'''

def audit_mg(token, greater_ThanTimeStamp, less_ThanTimestamp):

    base_URI = "https://management.azure.com/providers/Microsoft.Insights/eventtypes/management/values?api-version=2015-04-01&$"
    filter_URI = f"filter=eventTimestamp ge '{greater_ThanTimeStamp}' and eventTimestamp le '{less_ThanTimestamp}' and eventChannels eq 'Operation' and resourceProvider eq 'Microsoft.Management'"
    rest_URI = f'{base_URI}{filter_URI}'
    method_name = "get"
    return azHelper.exec_REST(token, method_name, rest_URI)

# region main
if __name__ == '__main__':
    tenant = os.environ["D_AZURE_TENANT_ID"]
    client_id = os.environ["D_AZURE_CLIENT_ID"]
    client_secret =  os.environ["D_AZURE_CLIENT_SECRET"]
    azure_audience = "https://management.azure.com/"
    ret_val = []

    greater_ThanTimeStamp = input("From (yyyy-MM-ddThh:mm:ss.ssssZ):") #"2018-08-06T09:03:48.1015011Z
    less_ThanTimeStamp = input("To(yyyy-MM-ddThh:mm:ss.ssssZ):")

    azure_token = azHelper.get_sp_token(tenant, client_id, client_secret, azure_audience)
    response = audit_mg(azure_token, greater_ThanTimeStamp = greater_ThanTimeStamp, less_ThanTimestamp = less_ThanTimeStamp)
    #print(response)
    ret_val.append(response)
    while 'nextLink' in response:
        response = azHelper.exec_REST(azure_token, "get", response['nextLink'])
        ret_val.append(response)
    with open('azSubLog.txt', 'w') as f:
        for val in range(len(ret_val)):
            if 'value'in ret_val[val]:
                for values in ret_val[val]['value']:
                    mg_action = "Microsoft.Management/managementGroups"
                    if mg_action in values['authorization']['action']:
                        out_str = f"{values['authorization']['scope']} | {values['eventTimestamp']} | {values['caller']} | {values['operationName']['localizedValue']} | {values['status']['value']}" #| {values['httpRequest']['method']}"
                        print(out_str)
                        f.write(f"{out_str}\n")
#endregion


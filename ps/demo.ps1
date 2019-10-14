Invoke-RestMethod -Uri http://localhost:8000/osobe

Invoke-RestMethod -Uri http://localhost:8000/osobe | Get-Member

(Invoke-RestMethod -Uri http://localhost:8000/osobe).Osobe

Invoke-WebRequest -Uri http://localhost:8000/osobe/123

#Login with:
Connect-AzAccount -Subscription $env:SMS_SUB_ID #console 1

Get-AzVM -ResourceGroupName ubuntu1804

Get-AzVM -ResourceGroupName ubuntu1804 -Status | Format-Table name, powerstate

Get-AzVM -ResourceGroupName ubuntu1804 -Debug

Stop-AzVM -ResourceGroupName ubuntu1804 -Name ubuntu1804 -StayProvisioned -Debug

# POSTMAN

# show Azure-AsyncOperation

Get-AzStorageAccount -ResourceGroupName siner19demo

#az ad sp create-for-rbac --name ServicePrincipalName --password mySuperStrongPwd

#prebaci na privatni subscription

#Connect-AzAccount -Credential $cred -TenantId $env:D_AZURE_TENANT_ID  -ServicePrincipal #console2

New-AzRoleAssignment -ResourceGroupName sinergija19 -SignInName "test@dzelenicwindowslive.onmicrosoft.com" -RoleDefinitionName reader

New-AzRoleAssignment -ResourceGroupName sinergija19 -SignInName "test@dzelenicwindowslive.onmicrosoft.com" -RoleDefinitionName reader -Debug

# https://graph.microsoft.com/v1.0/users/test@dzelenicwindowslive.onmicrosoft.com

Get-AzureADDirectoryRoleMember -ObjectId (Get-AzureADDirectoryRole | where-object {$_.DisplayName -eq "Directory Readers"}).Objectid
Get-AzureADDirectoryRole | where-object {$_.DisplayName -eq "Directory Readers"}

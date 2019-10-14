#
#Easily obtain AccessToken (Bearer) from an existing AzureRM PowerShell session
#
#https://gallery.technet.microsoft.com/scriptcenter/Easily-obtain-AccessToken-3ba6e593
#
#Author: s_lapointe


function Get-AzCachedAccessToken()
{
    $ErrorActionPreference = 'Stop'

    $azureRmProfile = [Microsoft.Azure.Commands.Common.Authentication.Abstractions.AzureRmProfileProvider]::Instance.Profile
    if(-not $azureRmProfile.Accounts.Count) {
        Write-Error "Ensure you have logged in before calling this function."
    }
    $currentAzureContext = Get-AzContext
    $profileClient = New-Object Microsoft.Azure.Commands.ResourceManager.Common.RMProfileClient($azureRmProfile)
    Write-Debug "Getting access token for tenant $($currentAzureContext.Tenant.TenantId)"
    $token = $profileClient.AcquireAccessToken($currentAzureContext.Tenant.TenantId)
    $token.AccessToken
}

Get-AzCachedAccessToken

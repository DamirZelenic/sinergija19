#used samples from https://github.com/igorpag/PSasRESTclientAzure and
#https://gallery.technet.microsoft.com/scriptcenter/Easily-obtain-AccessToken-3ba6e593

function Get-Token
{
    $azureRmProfile = [Microsoft.Azure.Commands.Common.Authentication.Abstractions.AzureRmProfileProvider]::Instance.Profile
    $currentAzureContext = Get-AzContext
    $profileClient = New-Object Microsoft.Azure.Commands.ResourceManager.Common.RMProfileClient($azureRmProfile)
    $token = $profileClient.AcquireAccessToken($currentAzureContext.Tenant.TenantId)
    return $token.AccessToken
}

function New-StorageAccountFromREST ($token, $storageAcccountName)
{
    $storagetype = "Standard_LRS"
    $rgname = "siner19demo"
    $location = "westeurope"

    $suffixURI = "?api-version=2016-12-01"
    $baseURI = "https://management.azure.com"
    $uri = $baseURI + ((Get-AzResourceGroup -Name $rgname).ResourceId) + "/providers/Microsoft.Storage/storageAccounts/" `
        + "$storageacccountname" + $suffixURI

    Write-Debug "Uri za kreiranje: $uri"

    $bodyCont = @{"name" = $storagetype}

    $body = @{"sku"= $bodyCont;"location" = $location}

    $params = @{
        ContentType = 'application/json'
        Headers     = @{
            'authorization' = "Bearer $token"
        }
        Body        = $body | ConvertTo-Json
        Method      = 'Put'
        URI         = $uri
    }

    Write-Output $params

    try
    {
        $response2 = Invoke-WebRequest @params
    }
    catch
    {
        Write-Output ("Error in the HTTP request...")
        Write-Output $Error[0]
        break
    }

    # Now let's check for the completion of the above operation: #

    if ($URIAsyncCheck = $response2.Headers["Location"])
    {
        Write-Output ("Response URL returned inside [Location] attribute")
    }
    else
    {
        $URIAsyncCheck = $response2.Headers["Azure-AsyncOperation"]
        Write-Output ("Response URL returned inside [Azure-AsyncOperation] attribute")
    }

    if ($URIAsyncCheck -is "System.String[]")
    {
        $URIAsyncCheck = ($URIAsyncCheck)[0]
    }

    # Now let's use value of $URIAsyncCheck to check the async operation status:
    $params = @{
        ContentType = 'application/json'
        Headers     = @{
            'authorization' = "Bearer $token"
        }
        Method      = 'Get'
        URI         = $URIAsyncCheck
    }
    try
    {
        $response3 = Invoke-WebRequest @params
    }
    catch
    {
        Write-Output ("Error in the HTTP request status check. Name may be already in use.")
        break
    }

    While ($response3.StatusCode -ne 200)
    {
        Start-Sleep -s 1;
        $response3 = Invoke-WebRequest @params
        Write-Output ("Radim ...Response Code = $($response3.StatusCode)")
    }

    # Search for the "ProvisioningState" attribute in the text blob: #
    if ($response3.Content.Contains('"provisioningState":"Succeeded"'))
    {
        Write-Output '["provisioningState":"Succeeded"] found in the Response Content payload....'
    }
    elseif ($response3.Content.Contains('"provisioningState":"Failed"'))
    {
        Write-Output '["provisioningState":"Failed"] found in the Response Content payload....'
    }
    elseif ($response3.Content.Contains('"provisioningState":"Canceled"'))
    {
        Write-Output '["provisioningState":"Failed"] found in the Response Content payload....'
    }
}

$storageAcccountName = Read-Host "Storage Account Name"
$token = Get-Token
# Write-Output $token
New-StorageAccountFromREST -token $token -storageAcccountName $storageAcccountName
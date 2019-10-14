$body = @{"id"="316";"ime"="Deda";"prezime"="Vlado"} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/osobe/dodaj -Method Post -Body $body
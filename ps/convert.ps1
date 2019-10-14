$final = ""
$letter = $null
$char = $null

foreach ($char in Get-content C:\users\dazeleni\Desktop\body1.txt)
{

    $char = [int[]]$char
    $letter += [char[]]$char
}
$final = ("$letter").Replace(" ","")
$final
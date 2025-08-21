Write-Host "$PSScriptRoot"
Set-Location "$PSScriptRoot"
Invoke-Expression .\env\Scripts\activate.ps1
python .\src\manage.py runserver
Write-Host "$PSScriptRoot"

Set-Location "$PSScriptRoot"

python -m virtualenv .\env
Invoke-Expression .\env\Scripts\activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\prerequisites.txt

python .\src\manage.py migrate
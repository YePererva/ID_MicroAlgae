# CS 5600 Final Project : ID Microalgae

Project for visual identification of microalgal cells by submitted picture from microscope camera.

## Update from 2025

### Deploy on Fedora 42 Server

```bash
sudo dnf up --refresh
sudo dnf install git python3-pip python3-virtualenv

cd ~
git clone https://github.com/YePererva/ID_MicroAlgae.git
cd ./ID_MicroAlgae

python -m virtualenv ./venv
source ./venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ./prerequisites.txt

python ./src/manage.py runserver
```

### Deploy on Windows 11

```PowerShell
cd ~
git clone https://github.com/YePererva/ID_MicroAlgae.git
cd ./ID_MicroAlgae
python -m virtualenv .\venv
. .\venv\Scripts\activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\prerequisites.txt

python .\src\manage.py runserver
```



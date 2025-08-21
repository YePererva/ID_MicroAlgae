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

python -m virtualenv ./env
source ./env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ./prerequisites.txt

python ./src/manage.py migrate

sudo firewall-cmd --zone=public --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --runtime-to-permanent

python ./src/manage.py runserver
```

### Deploy on Windows 11

```PowerShell
git clone https://github.com/YePererva/ID_MicroAlgae.git
cd .\ID_MicroAlgae
python -m virtualenv .\env
. .\env\Scripts\activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\prerequisites.txt

python .\src\manage.py migrate

python .\src\manage.py runserver
```
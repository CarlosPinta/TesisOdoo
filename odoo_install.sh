#!/bin/bash
while getopts p:u: opt; do
    case $opt in
        p) passwd=$OPTARG ;;
        u) user=$OPTARG ;;
        *)
            echo 'Error in command line parsing' >&2
            exit 1
    esac
done

: ${user:?No se ha enviado el paratremo -u para ingresar el usuario de github de Tandi } ${passwd:?No se ha enviado el paratremo -p para ingresar el usuario de github de Tandi}

#Creamos el usuario y grupo de sistema 'odoo' y postgres para acceder a las bases de datos:
sudo adduser --system --quiet --shell=/bin/bash --home=/opt/odoo --gecos 'odoo' --group odoo
sudo adduser --system --quiet --shell=/bin/bash --home=/opt/postgres --gecos 'postgres' --group postgres
#Creamos en directorio en donde se almacenará el archivo de configuración y log de odoo:
sudo mkdir /var/log/odoo/
# Instalamos Postgres y librerías base del sistema:
sudo apt-get update && sudo apt-get install postgresql-client build-essential python3-pil python3-lxml python3-dev python3-pip python3-setuptools npm nodejs git libldap2-dev libsasl2-dev libxml2-dev libxslt1-dev libjpeg-dev -y
#Descargamos odoo version 12 desde git:
sudo git clone --depth 1 --branch 12.0 https://github.com/odoo/odoo /opt/odoo/odoo12
#Descargamos odoo version 12 desde git:

sudo git clone --depth 1 --branch produccion_v12 https://$user:$passwd@git-codecommit.us-east-1.amazonaws.com/v1/repos/odoo_12 /opt/odoo/custom_addons

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.6 python3.6-dev python3.6-venv -y
python3.6 -m venv /opt/odoo/python3.6_venv
source /opt/odoo/python3.6_venv/bin/activate
pip install -r /opt/odoo/odoo12/requirements.txt

#Damos permiso al directorio que contiene los archivos de OdooERP e instalamos las dependencias de python3:
sudo chown odoo:odoo /opt/odoo/ -R && sudo chown odoo:odoo /var/log/odoo/ -R && cd /opt/odoo/odoo12
#Usamos npm, que es el gestor de paquetes Node.js para instalar less:
sudo npm install -g less less-plugin-clean-css -y && sudo ln -s /usr/bin/nodejs /usr/bin/node
#Descargamos dependencias e instalar wkhtmltopdf para generar PDF en odoo
sudo apt-get install -y software-properties-common && \
sudo apt-add-repository -y "deb http://security.ubuntu.com/ubuntu bionic-security main" && \
sudo apt-get -yq update && \
sudo apt-get install -y libxrender1 libfontconfig1 libx11-dev libjpeg62 libxtst6 \
                           fontconfig xfonts-75dpi xfonts-base libpng12-0 && \
cd /tmp
wget "https://www.dropbox.com/s/79x3imq73tcqyw4/libpng12-0_1.2.54-1ubuntu1b_amd64.deb" && sudo dpkg -i libpng12-0_1.2.54-1ubuntu1b_amd64.deb
wget "https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb" && \
sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb && \
sudo apt-get -f install

#wget http://security.ubuntu.com/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1.1_amd64.deb && sudo dpkg -i libpng12-0_1.2.54-1ubuntu1.1_amd64.deb
sudo ln -s /usr/local/bin/wkhtmltopdf /usr/bin/
sudo ln -s /usr/local/bin/wkhtmltoimage /usr/bin/
#wget -N http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz && sudo gunzip GeoLiteCity.dat.gz && sudo mkdir /usr/share/GeoIP/ && sudo mv GeoLiteCity.dat /usr/share/GeoIP/
#Creamos la configuracion de Odoo:
sudo cp /opt/odoo/odoo12/debian/odoo.conf /etc/odoo.conf
#Agregamos los siguientes parámetros al archivo de configuración de odoo:
sudo echo 'logfile=/var/log/odoo/odoo-server.log' >> /etc/odoo.conf
#Creamos el archivo de inicio del servicio de Odoo:
sudo ln -s /opt/odoo/odoo12/odoo-bin /usr/bin/odoo
sudo cp /opt/odoo/odoo12/debian/odoo.service /etc/systemd/system/odoo.service && sudo chmod +x /etc/systemd/system/odoo.service
sudo sed -i 's|^ExecStart=.*|'"ExecStart=/opt/odoo/python3.6_venv/bin/python /usr/bin/odoo -c /etc/odoo.conf"'|' /etc/systemd/system/odoo.service
sudo systemctl daemon-reload
sudo systemctl enable odoo.service
sudo systemctl start odoo.service
sudo systemctl status odoo.service
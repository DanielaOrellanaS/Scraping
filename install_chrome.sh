#!/usr/bin/env bash

set -e

# Instala dependencias básicas
apt-get update && apt-get install -y wget unzip curl gnupg2 ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils

# Descarga Google Chrome estable
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb || true

# Crea carpeta local bin si no existe
mkdir -p bin

# Descarga Chromedriver (versión 135, compatible con Chrome 135)
CHROMEDRIVER_VERSION=135.0.7049.114
wget https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip
unzip -o chromedriver-linux64.zip -d bin

# Mueve chromedriver al bin principal
mv bin/chromedriver-linux64/chromedriver bin/

# Copia google-chrome al bin
cp /usr/bin/google-chrome bin/chrome

# Da permisos de ejecución
chmod +x bin/chromedriver
chmod +x bin/chrome

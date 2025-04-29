#!/usr/bin/env bash

set -e

apt-get update && apt-get install -y wget unzip curl gnupg2 ca-certificates

# Instala Google Chrome estable
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb || true

# Crea carpeta local para el driver
mkdir -p bin

# Descarga y descomprime Chromedriver 135
CHROMEDRIVER_VERSION=135.0.7049.114
wget https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip
unzip -o chromedriver-linux64.zip -d bin
chmod +x bin/chromedriver

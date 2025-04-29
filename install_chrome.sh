#!/usr/bin/env bash

set -e

# Instala dependencias necesarias
apt-get update && apt-get install -y wget unzip curl gnupg2 ca-certificates

# Instala Google Chrome estable (versión compatible con chromedriver 135)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb || true

# Descarga chromedriver versión 135 para Linux
CHROMEDRIVER_VERSION=135.0.7049.114
wget https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip

# Extrae y mueve a un lugar accesible
unzip -o chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver

#!/usr/bin/env bash
# exit on error
set -o errexit

apt-get update
apt-get install -y rubberband-cli

pip install -r requirements.txt
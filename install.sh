#!/bin/bash

set -e

virtualenv="$HOME/.virtualenvs/chef-$(date -I)"

mkdir -p "$virtualenv" && pushd "$virtualenv"
python -m venv .
source ./bin/activate
pip install /home/jonasbrauer/Projects/chef/dist/chef-0.1.0-py3-none-any.whl

cmd="$(which chef)"
echo
echo -e "Run CHEF as \e[32m$cmd\e[0m"
echo
echo or to enable as a systemd service:
echo
echo 1. Save the following as /etc/systemd/system/chef.service
echo 2. sudo systemctl daemon-reload
echo 3. sudo systemctl enable --now chef
echo
echo "[Unit]"
echo Description=Chef: a recipe library
echo After=network.target
echo
echo "[Service]"
echo Type=simple
echo "User=$USER"
echo "ExecStart=$cmd"
echo Restart=on-failure
echo
echo "[Install]"
echo WantedBy=multi-user.target

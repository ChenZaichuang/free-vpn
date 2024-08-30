#!/bin/bash

set -e

DIR=FREE_VPN_DIR

cd ${DIR}

${DIR}/venv/bin/python start_github_vpn.py

#!/bin/bash

set -e

DIR=FREE_VPN_DIR

cd ${DIR}

${DIR}/venv/bin/python start_gcp_vpn.py

#!/bin/bash

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sed 's|FREE_VPN_DIR|'${DIR}'|g' ${DIR}/start_gcp_vpn.sh > ~/Desktop/start_gcp_vpn.sh && chmod +x ~/Desktop/start_gcp_vpn.sh
sed 's|FREE_VPN_DIR|'${DIR}'|g' ${DIR}/start_github_vpn.sh > ~/Desktop/start_github_vpn.sh && chmod +x ~/Desktop/start_github_vpn.sh

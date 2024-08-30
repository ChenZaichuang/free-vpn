#!/bin/bash

su_prefix='sudo '
if [ $(whoami) == "root" ]; then
  su_prefix=''
fi

if ! command -v curl &> /dev/null || ! command -v screen &> /dev/null || ! command -v unzip &> /dev/null
then
    ${su_prefix}apt update -y && ${su_prefix}apt install -y curl unzip screen
fi


VPN_DIR="./vpn"

VPN_PASSWORD=$1

# 判断目录是否存在
if [ ! -d "$VPN_DIR" ]; then
  # 下载zip文件
  curl -O "https://raw.githubusercontent.com/free-vpn/main/resources/gcp/free_vpn.zip"
  # 提示用户输入密码并解压缩zip文件

  unzip -q -P "$VPN_PASSWORD" free_vpn.zip -d .

  if [ ! $? -eq 0 ]; then
    # 解压缩失败，提示用户重新输入密码
    echo "Incorrect password."
    rm -rf ${PWD}/vpn
    exit 1
  fi

  # 修改文件权限
  chmod +x ${PWD}/free_vpn/start.sh
fi

# 执行VPN脚本
bash free_vpn/start.sh

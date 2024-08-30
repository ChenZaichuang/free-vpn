#!/bin/bash

git init
git remote add origin git@github.com:ChenZaichuang/free-vpn.git || true
git branch -M main
git config --global user.email "zcchen.dev@gmail.com"
git config --global user.name "zaichuang"


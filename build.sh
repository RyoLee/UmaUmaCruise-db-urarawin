#!/usr/bin/bash
mkdir -p ./tmp
rm ./tmp/* -f
chmod +x ./build.py
wget https://raw.githubusercontent.com/wrrwrr111/pretty-derby/master/src/assert/db.json -O tmp/db.json
#wget https://raw.githubusercontent.com/RyoLee/pretty-derby/master/src/assert/cn.json -O tmp/cn.json
./build.py
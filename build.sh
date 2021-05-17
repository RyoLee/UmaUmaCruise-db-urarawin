#!/usr/bin/bash
mkdir -p ./tmp
mv ./UmaMusumeLibrary.json ./UmaMusumeLibrary.json.old
rm ./tmp/* -f
chmod +x ./build.py
wget https://raw.githubusercontents.com/wrrwrr111/pretty-derby/master/src/assert/db.json -O tmp/db.json
#wget https://raw.githubusercontent.com/RyoLee/pretty-derby/master/src/assert/cn.json -O tmp/cn.json
./build.py
count=$(diff UmaMusumeLibrary.json UmaMusumeLibrary.json.old |wc -l)
if [ "0"x != "$count"x ];then
    date +%s > version
fi
rm ./UmaMusumeLibrary.json.old
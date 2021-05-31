#!/usr/bin/bash
mkdir -p ./tmp
if [ ! -e ./UmaMusumeLibrary.json ];then
    touch ./UmaMusumeLibrary.json
fi
rm ./tmp/* -f
rm UmaMusumeLibrary.json.new -f
chmod +x ./build.py
wget https://cdn.jsdelivr.net/gh/wrrwrr111/pretty-derby@master/src/assert/db.json -O tmp/db.json
wget https://cdn.jsdelivr.net/gh/wrrwrr111/pretty-derby@master/src/assert/cn.json -O tmp/cn.json
./build.py
cat tmp/UmaMusumeLibrary.json | jq . > UmaMusumeLibrary.json.new
count=$(diff UmaMusumeLibrary.json UmaMusumeLibrary.json.new |wc -l)
if [ "0"x != "$count"x ];then
    date +%s > version
    rm ./UmaMusumeLibrary.json
    cp ./UmaMusumeLibrary.json.new UmaMusumeLibrary.json
fi
rm UmaMusumeLibrary.json.new -f

#!/usr/bin/bash
mkdir -p ./tmp
if [ ! -e ./UmaMusumeLibrary.json ]; then
    touch ./UmaMusumeLibrary.json
fi
if [ ! -e ./UmaMusumeLibrary.jp.json ]; then
    touch ./UmaMusumeLibrary.jp.json
fi
rm ./tmp/* -f
rm UmaMusumeLibrary.json.new -f
rm UmaMusumeLibrary.jp.json.new -f
chmod +x ./build.py
wget https://raw.githubusercontents.com/wrrwrr111/pretty-derby/master/src/assert/db.json -O tmp/db.json
if [[ "$?" -ne 0 ]]; then
    exit -1
fi
wget https://raw.githubusercontents.com/wrrwrr111/pretty-derby/master/src/assert/cn.json -O tmp/cn.json
if [[ "$?" -ne 0 ]]; then
    exit -1
fi
./build.py
if [[ "$?" -ne 0 ]]; then
    exit -1
fi
cat tmp/UmaMusumeLibrary.cn.json | jq . >UmaMusumeLibrary.json.new
cat tmp/UmaMusumeLibrary.jp.json | jq . >UmaMusumeLibrary.jp.json.new
count=$(diff UmaMusumeLibrary.json UmaMusumeLibrary.json.new | wc -l)
countjp=$(diff UmaMusumeLibrary.jp.json UmaMusumeLibrary.jp.json.new | wc -l)
if [ "0"x != "$count"x ]; then
    date +%s >version
    rm ./UmaMusumeLibrary.json
    cp ./UmaMusumeLibrary.json.new UmaMusumeLibrary.json
    cat UmaMusumeLibrary.json | wc -c > UmaMusumeLibrary.json.ver
fi
if [ "0"x != "$countjp"x ]; then
    rm ./UmaMusumeLibrary.jp.json
    cp ./UmaMusumeLibrary.jp.json.new UmaMusumeLibrary.jp.json
    cat UmaMusumeLibrary.jp.json | wc -c > UmaMusumeLibrary.jp.json.ver
fi
rm UmaMusumeLibrary.json.new -f
rm UmaMusumeLibrary.jp.json.new -f

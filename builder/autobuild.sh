#!/bin/bash
dbl=$(cat ./dbl)
res=$(curl -s -I -X HEAD https://raw.githubusercontent.com/wrrwrr111/pretty-derby/master/src/assert/db.json | grep content-length)
if [ "$res"x = "x" ]; then
    echo "[error]no content-length"
    exit 1
fi
odbl=$(echo "$res" | awk '{print $2}')
if [ "$dbl"x != $odbl"x" ]; then
    sh ./build.sh
    if [[ "$?" -ne 0 ]]; then
        exit -1
    fi
    echo "$odbl" >./dbl
    curl -s https://purge.jsdelivr.net/gh/RyoLee/UmaUmaCruise-db-urarawin@master/UmaMusumeLibrary.json
    curl -s https://purge.jsdelivr.net/gh/RyoLee/UmaUmaCruise-db-urarawin@master/UmaMusumeLibrary.jp.json
else
    echo "[info] no update"
fi
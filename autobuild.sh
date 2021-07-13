#!/bin/sh
sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
apk add python3 jq
git config --global user.email "516127941@qq.com"
git config --global http.proxy 'socks5://gw.lan:7891'
git config --global https.proxy 'socks5://gw.lan:7891'
git config --global user.name "RyoLee"
git pull
dbl=$(cat ./dbl)
curl -s https://purge.jsdelivr.net/gh/wrrwrr111/pretty-derby@master/src/assert/cn.json
curl -s https://purge.jsdelivr.net/gh/wrrwrr111/pretty-derby@master/src/assert/db.json
res=$(curl -s -I -X HEAD https://cdn.jsdelivr.net/gh/wrrwrr111/pretty-derby@master/src/assert/db.json | grep content-length)
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
git commit -a -m "[autobuild] version:"$(cat version)
git push

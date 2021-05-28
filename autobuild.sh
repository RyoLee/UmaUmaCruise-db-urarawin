#!/bin/sh
sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
apk add python3
git config --global user.email "516127941@qq.com"
git config --global https.proxy 'socks5://192.168.1.200:7891'
git config --global https.proxy 'socks5://192.168.1.200:7891'
git config --global user.name "RyoLee"
git pull
dbl=$(cat ./dbl)
curl -s https://purge.jsdelivr.net/gh/wrrwrr111/pretty-derby@master/src/assert/db.json
res=$(curl -s -I -X HEAD https://cdn.jsdelivr.net/gh/wrrwrr111/pretty-derby@master/src/assert/db.json|grep content-length)
if [ "$res"x = "x" ];then
    echo "[error]no content-length"
    exit 1
fi
odbl=$(echo "$res"|awk '{print $2}')
if [ "$dbl"x != $odbl"x" ];then
    sh ./build.sh
    echo "$odbl" > ./dbl
    curl -s https://purge.jsdelivr.net/gh/RyoLee/UmaUmaCruise-db-urarawin@master/UmaMusumeLibrary.json
else
    echo "[info] no update"
fi
git commit -a -m "[autobuild] version:"$(cat version)
git push

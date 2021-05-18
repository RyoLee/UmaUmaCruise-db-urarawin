#!/bin/sh
sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
apk add python3
dbl=$(cat ./dbl)
res=$(curl -s -I -X HEAD https://cdn.jsdelivr.net/gh/wrrwrr111/pretty-derby@master/src/assert/db.json|grep content-length)
if [ "$res"x = "x" ];then
    echo "[error]no content-length"
    exit 1
fi
odbl=$(echo "$res"|awk '{print $2}')
if [ "$dbl"x = $odbl"x" ];then
    echo "[info] noupdate"
    exit 0
fi
git config --global user.email "516127941@qq.com"
git config --global user.name "RyoLee"
git config --global https.proxy 'socks5://gw.lan:7891'
git config --global https.proxy 'socks5://gw.lan:7891'
git pull
sh ./build.sh
echo "$odbl" > ./dbl
git add ./*
git commit -m "[autobuild] version:"$(cat version)
git push
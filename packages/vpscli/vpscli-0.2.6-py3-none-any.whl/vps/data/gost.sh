#!/bin/bash 
# Redirect data flow

# KILL ALL PREVIOUS PROCESS 
kill $(ps aux|grep [a]md64 | awk '{print $2}')


# Demo
#./gost-linux-amd64 -L=:12345 -F=ss://aes-256-gcm:share117@ru.140714.xyz:8633 &> /dev/null 
# ./gost-linux-amd64 -L=ss://aes-256-gcm:share117@:51176 -F=socks5://localhost:7891 &> /dev/null &
# ./gost-linux-amd64 -L=:12345 -F=socks5://localhost:7891 &> /dev/null &
# ./gost-linux-amd64 -L=:40531 -F=socks5://localhost:7891 &> /dev/null &

GOST=$(which gost-linux-amd64)
$GOST -L=socks5://cloudiplc:passport123@:32970 &
$GOST -L=ss://aes-256-gcm:passport123@:40531 -F=socks://herizon:passport123@jp.ddot.cc:8868 

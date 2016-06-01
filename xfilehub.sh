#!/usr/bin/env bash

function clear()
{
    cd /Users/fengfei/graduation/
    for port in $(seq 8000 8009) ; do
        rm -f ./xfilehub-stroage/storages/storage\#${port}/chunks/*
        rm -f ./xfilehub-stroage/storages/storage\#${port}/*.note
    done
    rm -f ./xfilehub/storage/*.note
    tree -L 2 ./xfilehub-stroage/storages/
}

function stop()
{
    for port in $(seq 8000 8009) ; do
        kill -9 $(lsof -i:${port} | awk '{print $2}' | tail -n 2)
    done
    lsof -nPi TCP -s TCP:LISTEN | grep 127.0.0.1:80 | grep 4u | sort -k 8

    kill -9 $(lsof -i:9000 | awk '{print $2}' | tail -n 2)
    lsof -nPi TCP -s TCP:LISTEN | grep 127.0.0.1:9000 | grep 4u | sort -k 8
}

function start()
{
    echo
    cd /Users/fengfei/graduation/xfilehub-stroage/
    for port in $(seq 8000 8009) ; do
        PORT=${port} python3.5 ./server.py &
    done
    sleep 1s
    cd /Users/fengfei/graduation/xfilehub/
    python3.5 ./server.py &
}


if [ -n $1 ] ; then
    echo operation is $1
    case $1 in
    clear)
        clear ;;
    stop)
        stop ;;
    start)
        start ;;
    restart)
        stop && start ;;
    reset)
        clear && stop && start ;;
    esac
fi

exit 0
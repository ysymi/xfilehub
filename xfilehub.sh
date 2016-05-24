#!/usr/bin/env bash

function clear()
{
    for port in $(seq 8000 8009)
    do
        rm -f /Users/fengfei/graduation/xfilehub-stroage/storages/storage\#${port}/chunks/*
        rm -f /Users/fengfei/graduation/xfilehub-stroage/storages/storage\#${port}/*.note
    done
    rm -f /Users/fengfei/graduation/xfilehub/storage/*.note
    tree -L 2 /Users/fengfei/graduation/xfilehub-stroage/storages/
}

function stop()
{
    for port in $(seq 8000 8009)
    do
        kill -9 $(lsof -i:${port} | awk '{print $2}' | tail -n 2)
    done
    lsof -nPi TCP -s TCP:LISTEN | grep 127.0.0.1:80 | grep 4u | sort -k 8

    kill -9 $(lsof -i:9000 | awk '{print $2}' | tail -n 2)
    lsof -nPi TCP -s TCP:LISTEN | grep 127.0.0.1:9000 | grep 4u | sort -k 8
}

function start()
{
    echo
    for port in $(seq 8000 8009)
    do
        PORT=${port} python3.5 /Users/fengfei/graduation/xfilehub-stroage/server.py &
    done
    python3.5 /Users/fengfei/graduation/xfilehub/server.py
}


if [ -n $1 ] ; then
    echo operation is $1
    case $1 in
    clean)
        clear
        ;;
    stop)
        stop
        ;;
    start)
        start
        ;;
    restart)
        stop && start
        ;;
    reset)
        clear && stop && start
        ;;
    esac
fi

exit 0
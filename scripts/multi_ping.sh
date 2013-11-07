#!/bin/bash

function check_alive {
    ping -c 1 $1 >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo true
    else
        echo false
    fi
}

#IFS: Internal Field Separator
IFS=$'\r\n' hosts=($(cat $(dirname $0)/ping_hosts))

echo '{'

echo \"${hosts[0]}\": 
check_alive ${hosts[0]}

for host in ${hosts[@]:1}; do
    echo ,\"$host\":
    check_alive $host
done

echo '}'

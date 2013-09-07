#!/bin/bash

echo '['
for user in $(users);do
    echo "\"${user}\","
done
echo ']'

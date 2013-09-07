#!/bin/bash

output=( $(uptime) )
uptime="${output[2]:0:(-1)}"
load1="${output[7]:0:(-1)}"
load1="${load1/,/.}"
load5="${output[8]:0:(-1)}"
load5="${load5/,/.}"
load15="${output[9]:0:(-1)}"
load15="${load15/,/.}"

echo '{'
echo "  \"uptime\": \"$uptime\","
echo "  \"load1\":   $load1,"
echo "  \"load5\":   $load5,"
echo "  \"load15\":  $load15"
echo '}'

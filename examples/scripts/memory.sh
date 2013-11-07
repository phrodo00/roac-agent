#!/bin/bash
echo '{'
grep -e 'MemTotal' -e 'MemFree' -e 'Buffers' -e 'Cached' -e 'SwapCached' /proc/meminfo| tr -s ' '| cut -d ' ' -f '1 2'| sed -e '1s/^/"/' -e '2,$s/^/, "/' -e 's/:/":/'
echo '}'

#!/bin/bash

cmd="wget -nv -T60 --no-warc-compression --warc-max-size=1G --warc-cdx \
     --warc-file=$1 -i $2 -O- >/dev/null"
echo $cmd
$cmd

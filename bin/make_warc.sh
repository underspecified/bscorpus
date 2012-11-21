#!/bin/bash

warc=$1
urls=$2

cmd="( wget -nv -T60 --no-warc-compression --warc-max-size=1G --warc-cdx \
     -O- --warc-file=$warc -i $urls ) >/dev/null"
echo $cmd
eval $cmd

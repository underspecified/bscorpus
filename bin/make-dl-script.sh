#!/bin/bash

./bs-rss "$1" | 
tr -d \" | 
awk '
{
    url = $1
    file = $2

    printf "mkdir -p `dirname %s` && \\\n", file
    printf "    wget %s -O %s.html\n", url, file
    printf "    htmlfmt < %s.html > %s.txt\n\n", file, file
}'

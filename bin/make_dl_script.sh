#!/bin/bash

./MacOSX/i386/bs-rss "$1" | 
tr -d \" | 
awk '
{
    url = $1
    file = $2

    printf "mkdir -p `dirname %s` && \\\n", file
    printf "    curl -o \"%s.html\" \"%s\"\n", file, url
    printf "    htmlfmt < \"%s.html\" > \"%s.txt\"\n\n", file, file
}'

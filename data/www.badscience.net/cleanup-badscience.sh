#!/bin/bash

cleanup_bs () {
	awk '
	/^del.icio.us Digg it reddit Google StumbleUpon Slashdot It!$/ {
		article = ""
	}
	article == "true" {
		print
	}
	/^• xkcd$/ {
		article = "true"
	}'
}

case "$#*" in
	0)
		echo cleanup_bs 
	;;
	*)
		cat $* | cleanup_bs
	;;
esac

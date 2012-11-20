#!/usr/bin/awk -f

BEGIN {
	RS = ""
	FS = "\n"
	OFS = "\t"
}
{
	blog = $1
	title = $2
	url = $3
	print url
}

#!/usr/bin/awk

BEGIN {
	RS = ""
	FS = "\n"
	OFS = "\t"
}
{
	blog = $1
	post = $2
	link = $3
	print blog, post, link
}

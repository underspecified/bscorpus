#!/usr/bin/awk -f

BEGIN {
	RS = ""
	FS = "\n"
	OFS = "\t"
}
{
	blog = $1
	title = $2
	link = $3
	print blog, title, link
}

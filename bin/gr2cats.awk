#!/usr/bin/awk -f

BEGIN {
	RS = ""
	FS = "\n"
}
{
	blog = $1
	title = $2
	link = $3
	for(i=4;i<=NF;i++){
		if($i !~ /com.google/){
			print $i
		}
	}
}

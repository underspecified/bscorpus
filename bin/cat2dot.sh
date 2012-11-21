#!/bin/bash

cat2awk () {
	awk '
	BEGIN {
		FS = "\t"
	}
	{		
		freq = $1
		cat = $2
		clean = $2

		gsub(" ", "_", key)
		gsub("-", "_", key)
		gsub("/", "_", key)
		gsub(" ", "_", clean)
		gsub("-", "_", clean)
		gsub("/", "_", clean)
				
		if(clean!=key){
			printf "\t%s [label=\"%s\"];\n", clean, cat
			printf "\t%s -> %s [label=\"%s\"];\n", key, clean, freq
		}
	}' key="$1"
}

getcats () {
	awk -f gr2cats.awk gr-feeds.txt |
	tr A-Z a-z |
	grep -i "$1" |
	sed -r 's/\t$//g; s/\t/\n/g' |
	sort -t'	' |
	uniq -c |
	sort -t'	' -nr |
	sed 's/^ *//g; s/ /\t/' |
	awk '
	BEGIN {
		FS = "\t"
	}
	$1 >= 15'
}

echo "digraph G {"
#echo "	center = true;"
#echo "	ranksep = equally;"
echo "	ratio = compress;"
echo "	rank = source;"
echo '	size = "4.0,5.0";'
#echo "	page = 8.5, 5.5;"
#echo "	orientation = landscape;"

getcats "$*" | 
cut -f2 |
while read line; do
	getcats "$line" |
	cat2awk "$line"
done |
awk '
/->/ {
	a = $1 "->" $3
	b = $3 "->" $1
	if(! printed[a] && ! printed[b]){
		print
		printed[a] = "true"
		printed[b] = "true"
	}
}
$0 !~ /->/ {
	print
}' |
sort -u |
sed "s/'//g
	 s/\&/and/g
	 s#/#-#g
	 s/!//g"

echo "}"

#!/usr/bin/make

BSHOME	?= $(HOME)/bscorpus
FS      := gr-feeds
POSTS   := 1000

all:	stats

clean:	clean.txt

cleanall: clean.txt clean.xml

clean.txt:
	rm -f *.txt

clean.xml:
	rm -f *.xml

stats:	gr-cats.stats.txt gr-entries.stats.txt gr-blogs.stats.txt gr-titles.stats.txt gr-urls.stats.txt gr-links.txt

%.stats.txt:	%.txt
	tr A-Z a-z < $< | \
	sort -t'	' | \
	uniq -c | \
	sort -t'	' -nr > $@

gr-links.txt:	txt
	python $(BSHOME)/bin/gr-links.py $(FS).*.txt > $@ 2| tee gr-links.log

gr-blogs.txt:	gr-entries.txt
	cut -f1 < $< > $@

gr-titles.txt:	gr-entries.txt
	cut -f2 < $< > $@

gr-urls.txt:	gr-entries.txt
	cut -f3 < $< > $@

gr-cats.txt:	gr-feeds.txt $(BSHOME)/bin/gr2cats.awk
	awk -f $(BSHOME)/bin/gr2cats.awk < $< > $@

gr-entries.txt:	gr-feeds.txt $(BSHOME)/bin/gr2blogs.awk
	awk -f $(BSHOME)/bin/gr2blogs.awk < $< > $@

gr-feeds.txt:	txt
	cat $(FS).*.txt > $@

txt:	xml
	make $(shell echo $(FS).*.xml | sed 's/xml/txt/g')

xml: $(BSHOME)/bin/gr-rss.py
	$(BSHOME)/bin/gr-rss.py $(FS) $(POSTS)

%.txt:	%.xml $(BSHOME)/xslt/gr.xslt
	xsltproc $(BSHOME)/xslt/gr.xslt $< | \
	grep -v 'com.google' > $@

.PHONY:	all clean* stats xml

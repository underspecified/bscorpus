#!/usr/bin/make

BSHOME	?= $(HOME)/bscorpus
FS      := gr-feeds
POSTS   := 1000
stats	:= gr-cats.stats.txt gr-entries.stats.txt gr-blogs.stats.txt gr-titles.stats.txt gr-urls.stats.txt
links	:= gr-links.txt

all:	xml txt $(stats) $(links)

clean:	clean.stats clean.links clean.log

cleanall: clean.xml clean.txt clean.log clean.stats clean.links

clean.links:
	rm -f $(links)

clean.stats:
	rm -f $(stats)

clean.log:
	rm -f *.log

clean.txt:
	rm -f *.txt

clean.xml:
	rm -f *.xml

stats:	$(stats)

links:	$(links)

%.stats.txt:	%.txt
	tr A-Z a-z < $< | \
	sort -t'	' | \
	uniq -c | \
	sort -t'	' -nr > $@

gr-links.txt:	$(BSHOME)/bin/gr-rss.py
	python $(BSHOME)/bin/gr-links.py $(shell echo $(FS).*.xml) > $@ \&| tee gr-links.log

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

gr-feeds.txt:
	cat $(FS).*.txt > $@

txt:	xml
	make $(shell echo $(FS).*.xml | sed 's/xml/txt/g')

xml: $(BSHOME)/bin/gr-rss.py
	python $(BSHOME)/bin/gr-rss.py $(FS) $(POSTS)

%.txt:	%.xml $(BSHOME)/xslt/gr.xslt
	xsltproc $(BSHOME)/xslt/gr.xslt $< | \
	grep -v 'com.google' > $@

.PHONY:	all clean* stats links txt xml

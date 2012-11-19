#!/usr/bin/make

BSHOME	?= $(HOME)/bscorpus
FS      := gr_feeds
POSTS   := 1000
stats	:= gr_cats.stats.txt gr_entries.stats.txt gr_blogs.stats.txt gr_titles.stats.txt gr_urls.stats.txt
discussions	:= gr_discussions.txt

all:	stats discussions

clean:	clean.stats clean.discussions clean.log

cleanall: clean.xml clean.txt clean.log clean.stats clean.discussions

clean.discussions:
	rm -f $(discussions)

clean.stats:
	rm -f $(stats)

clean.log:
	rm -f *.log

clean.txt:
	rm -f *.txt

clean.xml:
	rm -f *.xml xml.done

stats:	$(stats)

discussions:	$(discussions)

%.stats.txt:	%.txt
	tr A-Z a-z < $< | \
	sort -t'	' | \
	uniq -c | \
	sort -t'	' -nr > $@

gr_discussions.txt:	gr_links.pkl $(BSHOME)/bin/gr_discussions.py $(BSHOME)/bin/grutils.py
	python $(BSHOME)/bin/gr_discussions.py $< | tee $@

gr_links.pkl:	$(BSHOME)/bin/gr_links.py $(BSHOME)/bin/grutils.py
	python $(BSHOME)/bin/gr_links.py $@ $(shell echo $(FS).*.xml) 2>&1 | \
	tee gr_links.log

gr_blogs.txt:	gr_entries.txt
	cut -f1 < $< > $@

gr_titles.txt:	gr_entries.txt
	cut -f2 < $< > $@

gr_urls.txt:	gr_entries.txt
	cut -f3 < $< > $@

gr_cats.txt:	gr_feeds.txt $(BSHOME)/bin/gr2cats.awk
	awk -f $(BSHOME)/bin/gr2cats.awk < $< > $@

gr_entries.txt:	gr_feeds.txt $(BSHOME)/bin/gr2blogs.awk
	awk -f $(BSHOME)/bin/gr2blogs.awk < $< > $@

gr_feeds.txt:
	cat $(FS).*.txt > $@

txt:	xml.done
	make $(shell echo $(FS).*.xml | sed 's/xml/txt/g')

xml: $(BSHOME)/bin/gr_rss.py
	python $(BSHOME)/bin/gr_rss.py $(FS) $(POSTS)
	touch xml.done

%.txt:	%.xml $(BSHOME)/xslt/gr.xslt
	-xsltproc $(BSHOME)/xslt/gr.xslt $< | \
	grep -v 'com.google' > $@

.PHONY:	all clean* stats links txt xml*

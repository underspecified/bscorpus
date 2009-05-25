BSHOME	?= $(HOME)/bscorpus
FS      := gr-feeds
POSTS   := 10000
ITERS   := 10
XITERS  := $(shell awk "END{print $(ITERS)-1}")
#TXT     := $(foreach n,$(shell seq -w 0 $(XITERS)),$(FS).$(n).txt)
XML     = $(FS).*.xml
TXT     = $(FS).*.txt

all:	xml stats

stats:	gr-cats.stats.txt gr-entries.stats.txt gr-blogs.stats.txt gr-titles.stats.txt gr-urls.stats.txt 

clean:	clean.txt

cleanall: clean.txt clean.xml

clean.txt:
	rm -f *.txt

clean.xml:
	rm -f *.xml

%.stats.txt:	%.txt
	tr A-Z a-z < $< | \
	sort -t'	' | \
	uniq -c | \
	sort -t'	' -nr > $@

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

gr-feeds.txt:	$(TXT)
	cat $^ > $@

%.txt:	%.xml $(BSHOME)/xslt/gr.xslt
	xsltproc $(BSHOME)/xslt/gr.xslt $< | \
	grep -v 'com.google' > $@

xml: $(BSHOME)/bin/gr-rss.py
	$(BSHOME)/bin/gr-rss.py $(FS) $(POSTS) $(ITERS)

.PHONY:	all clean* stats xml

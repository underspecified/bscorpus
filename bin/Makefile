FS      := gr-feeds
POSTS   := 10000
ITERS   := 10
XITERS  := $(shell awk "END{print $(ITERS)-1}")
TXT     := $(foreach n,$(shell seq -w 0 $(XITERS)),$(FS).$(n).txt)
XML     := $(TXT:.txt=.xml)

all:	stats

stats:	gr-cats.stats.txt gr-entries.stats.txt gr-blogs.stats.txt gr-titles.stats.txt gr-urls.stats.txt 

clean:
	rm -f $(FS).*

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

gr-cats.txt:	gr-feeds.txt
	awk -f gr2cats.awk < $< > $@

gr-entries.txt:	gr-feeds.txt
	awk -f gr2blogs.awk < $< > $@

gr-feeds.txt:	$(TXT)
	cat $^ > $@

%.txt:	%.xml
	xsltproc gr.xslt $< | \
	grep -v 'com.google' > $@

$(XML): gr-rss.py
	python gr-rss.py $(FS) $(POSTS) $(ITERS)

.PHONY:	all clean stats

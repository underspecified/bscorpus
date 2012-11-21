#!/usr/bin/make -f

SHELL	:= /bin/bash
BSHOME	:= $(realpath ..)
PATH	:= $(BSHOME)/bin:$(PATH)

fs	:= gr_feeds
post	:= 1000
xml	:= $(wildcard xml/$(fs).*.xml)
txt	:= $(subst xml,txt,$(xml))
urls	:= $(subst xml,urls,$(xml))
warc	:= $(subst xml,warc,$(xml))
stats	:= $(addprefix stats/,gr_cats.stats.txt gr_entries.stats.txt gr_blogs.stats.txt gr_titles.stats.txt gr_urls.stats.txt)
discussions	:= $(addprefix disc/,gr_discussions.txt gr_links.pkl)

all:	stats

clean:	clean.stats

cleanall: clean.xml clean.txt clean.stats clean.discussions

clean.discussions:
	rm -rf disc/

clean.stats:
	rm -rf stats/

clean.txt:
	rm -rf txt/

clean.warc:
	rm -rf warc/

clean.urls:
	rm -rf urls/

clean.xml:
	rm -rf xml/

discussions:	disc/done

disc/done:	$(discussions)
	touch $@

disc/gr_discussions.txt:	disc/gr_links.pkl $(BSHOME)/bin/gr_discussions.py $(BSHOME)/bin/grutils.py
	mkdir -p disc
	gr_discussions.py $< | tee $@

disc/gr_links.pkl:	xml/done $(BSHOME)/bin/gr_links.py $(BSHOME)/bin/grutils.py
	mkdir -p disc
	gr_links.py $@ $(xml) 2>&1 | tee disc/gr_links.log

stats:	stats/done

stats/done:	$(stats)
	touch $@

%.stats.txt:	%.txt $(BSHOME)/bin/calc_stats.sh
	calc_stats.sh < $< > $@

stats/gr_blogs.txt:	stats/gr_feeds.txt $(BSHOME)/bin/gr2blogs.awk
	mkdir -p stats
	gr2blogs.awk < $< > $@

stats/gr_titles.txt:	stats/gr_feeds.txt $(BSHOME)/bin/gr2titles.awk
	mkdir -p stats
	gr2titles.awk < $< > $@

stats/gr_urls.txt:	stats/gr_feeds.txt $(BSHOME)/bin/gr2urls.awk
	mkdir -p stats
	gr2urls.awk < $< > $@

stats/gr_cats.txt:	stats/gr_feeds.txt $(BSHOME)/bin/gr2cats.awk
	mkdir -p stats
	gr2cats.awk < $< > $@

stats/gr_entries.txt:	stats/gr_feeds.txt $(BSHOME)/bin/gr2entries.awk
	mkdir -p stats
	gr2entries.awk < $< > $@

stats/gr_feeds.txt:	txt/done
	mkdir -p stats
	cat $(txt) > $@

warc:	warc/done

warc/done:	urls/done
	mkdir -p warc
	+make $(warc)
	touch $@

warc/%.warc:	urls/%.urls
	mkdir -p warc
	cd warc && make_warc.sh $* ../$<

urls:	urls/done

urls/done:	txt/done
	mkdir -p urls
	+make $(urls)
	touch $@

urls/%.urls:	txt/%.txt $(BSHOME)/bin/gr2urls.awk
	mkdir -p urls
	gr2urls.awk < $< > $@

txt:	txt/done

txt/done:	xml/done
	mkdir -p txt
	+make $(txt)
	touch $@

txt/%.txt:	xml/%.xml $(BSHOME)/xslt/gr.xslt
	mkdir -p txt
	-xsltproc $(BSHOME)/xslt/gr.xslt $< | \
	grep -v 'com.google' > $@

xml:	xml/done

xml/done: $(BSHOME)/bin/gr_rss.py
	mkdir -p xml
	cd xml && gr_rss.py $(fs) $(posts)
	touch $@

.PHONY:	all clean* discussion stats txt warc xml

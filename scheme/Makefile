bin = bs-rss

all:										$(bin)

clean:
	rm -f *.c *.o

cleanall:									clean
	rm -f $(bin)

install:									$(bin)
	mkdir -p ../bin/$(OS)/$(ARCH)
	install $(bin) ../bin/$(OS)/$(ARCH)/

%.o:										%.scm
	csc -O3 -c $*.scm

%:										%.o
	csc $? -o $@

.PHONY:	all clean cleanall install

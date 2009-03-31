================================
Genron Map English Corpus v0.1.1
================================

Eric Nichols <eric-n@is.naist.jp>, 2008/10/16


This is a preliminary release of the Genron Map English corpus.
The goal is to produce a corpus of claims and their refutations 
from posts on anti-pseudoscience blogs.

Currently it consists of 57 articles downloaded from www.badscience.net
with permission from its author Dr. Ben Goldachre <ben@badscience.net>.
The original HTML for each post is downloaded and the Plan 9 utility
htmlfmt is used to convert it to plain text. Bad Science data has been
cleaned up -- front matter and comments are stripped out by the script
data/cleanup-badscience.sh.

The files are organized as follows:

data/blog-name/category/YYYYMM/title.{html,txt,txt.clean}

For example:

data/www.badscience.net/fish-oil/200809/dave-ford-from-durham-council-plays-at-being-a-scientist-again.html

is a post from www.badscience.net about fish oil published in September, 2008.

scheme/ contains the source code for an RSS feed downloader that produces
a bash script for downloading new articles and converting them to text.
bin/ contains the compiled scheme code for various platforms and some small
utility scripts.

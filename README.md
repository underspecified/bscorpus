# The Bad Science Corpus

Author: Eric Nichols <eric@ecei.tohoku.ac.jp>, Tohoku University, Japan

## Project Goal

This is a pre-release of the *Bad Science Corpus*, an automatically-constructed collection of posts on scientifically-contraversial topics gathered from blogs by scientists and skeptics. The goal of this project is to produce a self-expanding source of controversial claims and their refutations by knowledgable parties to support research on analysis rhetorical and logical argumentation structures. See reference [\[1\]][link-pacling-2009] for more details.

## Resources

* __RSS feed__: a curated collection of RSS feeds for several hundred science/skeptic blogs aggregated in a Google Reader account. Stored in `data/xml`.
* __Blog posts__: Web archives of all blog posts from July 2009 to November 2012. Stored in `data/warc`.
* __Discussions__: Blog posts that refer to the same external link are grouped into _discussions_ representing a single topic to aid extraction of controversial opinions and rebuttals. Stored in `data/disc`

## Utilities

There are Python scripts for accessing the Bad Science RSS feeds and updating the corpus as new posts are added. 

* `bin/gr_rss.py`: downloads RSS feeds as XML files
* `bin/gr_links.py`: extracts all links from RSS feed XML
* `bin/gr_discussions.py`: groups all links from feeds into discussions that have common external link

### Dependencies

See `dependencies.md` and `python_deps.txt` for dependencies.

## License
Please cite reference [\[1\]][link-pacling-2009] if you use the Bad Science Corpus. Otherwise, it may be used without restriction. All blog posts and other downloaded webpages are copyright their original authors and are being shared under the fair use. All code is copyright Eric Nichols and may be used, modified, and redistributed under the terms of the [GNU General Public License, version 2][link-gpl2].

[link-gpl2]: http://www.gnu.org/licenses/gpl-2.0.html

## References

\[1\] [Constructing a Scientific Blog Corpus for Information Credibility Analysis][link-pacling-2009]. Eric Nichols, Koji Murakami, Kentaro Inui, and Yuji Matsumoto. Proceedings of Pacling 2009. Hokkaido, Japan. 2009.

[link-pacling-2009]: http://www.cl.ecei.tohoku.ac.jp/~eric/papers/bscorpus-pacling2009-paper.pdf

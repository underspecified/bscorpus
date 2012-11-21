# The Bad Science Corpus

Author: Eric Nichols <eric@ecei.tohoku.ac.jp>, Tohoku University, Japan

## Project Goal

This is a pre-release of the *Bad Science Corpus*, an automatically-constructed collection of posts on scientifically-contraversial topics gathered from blogs by scientists and skeptics. The goal of this project is to produce a self-expanding source of contraversial claims and their refutations by knowledgable parties to support research on analysis rhetorical and logical argumentation structues. See publication [1] for more details.

## Resources

* __RSS feed__: RSS feeds for several hundred science/skeptic blogs have been archived in a Google Reader account since 2008. Stored in `data/xml`.
* __Blog posts__: downloads of the HTML for all blog posts in the blog feeds, stored in Web Archives. Stored in `data/warc`.
* __Discussions__: lists of blog posts that link to the same external article. Stored in `data/disc`

## Utilities

There are Python scripts for accessing the Bad Science RSS feeds and updating the corpus as new posts are added. 

* `bin/gr_rss.py`: downloads RSS feeds as XML files
* `bin/gr_links.py`: extracts all links from RSS feed XML
* `bin/gr_discussions.py`: groups all links from feeds into discussions that have common external link

## References

[1] Constructing a Scientific Blog Corpus for Information Credibility Analysis. Eric Nichols, Koji Murakami, Kentaro Inui, and Yuji Matsumoto. Proceedings of Pacling 2009. Hokkaido, Japan. 2009.

# academia.json

A database of RSS feeds for academic journals and conferences.

## Sources

* IEEE, for example <https://ieeexplore.ieee.org/rss/TOC32.XML> 
* ACM with, for example <http://rss.acm.org/dl/J204.xml>
* Elsevier, for example <https://rss.sciencedirect.com/publication/science/01676423>
* Springer with `journal-id`, for example <https://link.springer.com/search.rss?facet-journal-id=10515> 
* Wiley, for example <https://onlinelibrary.wiley.com/action/showFeed?jc=20477481&type=etoc>
* DBLP, for example <https://www.monperrus.net/martin/dblp-rss.py?search=venue:FASE:>
  
## Format
One entry per conference or journal, for example:

```json
"tse": {
  "dblp_code": "IEEE_Trans._Software_Eng.",
  "long_name": "IEEE Transactions on Software Engineering",
  "short_name": "TSE",
  "rss" : "https://ieeexplore.ieee.org/rss/TOC32.XML",
  "type": "journal"
}
```

Pull requests welcome.

Author: Martin Monperrus  
License: MIT

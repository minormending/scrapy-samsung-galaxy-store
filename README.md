# Samsung Galaxy Store Scrapy Spider
A scrapy spider for the [Samsung Galaxy Store](https://galaxystore.samsung.com/). The spider crawls all the category pages accumulating app info, then crawls each app page for extended app metadata and reviews. The extracted data is then stored in mongoDB.

# Usage
```
>>> scrapy crawl galaxy-store 
```

# scrapy-scrape-viewer

### Review My Scrapes

> Initially Semi-Cloned From: [kimberlythegeek/stackoverflow-denver_spider.py](https://github.com/kimberlythegeek/scrapy-project/blob/master/tutorial/spiders/stackoverflow-denver_spider.py)

* I left almost all of the GUI alone. I just applied it to work with the .json generated with my own Scrapy bots.

#### Refer to my older  [GIT-REPO-LINKs](https://github.com/mezcel/googlemaps-api-helloworld) to generate the .json this AngularJS App will use.

> * <i> I used a more efficient scrape technique than the one used in my the Google API Repo </i>

### Linux Terminal cheat:

```
    rm '/home/mezcel/github/scrapy-scrape-viewer/expresspros_Alabama_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/expresspros_Florida_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/expresspros_Georgia_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Alabama_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Florida_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Georgia_Demo.json'

    cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
    source bin/activate
    ls

    cd expresspros
    scrapy crawl expresspros -a domain='https://workforce.expresspros.com/locations/state/Alabama' -o ../../expresspros_Alabama_Demo.json -t json
    scrapy crawl expresspros -a domain='https://workforce.expresspros.com/locations/state/Florida' -o ../../expresspros_Florida_Demo.json -t json
    scrapy crawl expresspros -a domain='https://workforce.expresspros.com/locations/state/Georgia' -o ../../expresspros_Georgia_Demo.json -t json

    cd ..
    ls

    cd stackoverflow
    scrapy crawl stackoverflow -a domain='https://stackoverflow.com/jobs?sort=p&l=Alabama' -o ../../stackoverflow_Alabama_Demo.json -t json
    scrapy crawl stackoverflow -a domain='https://stackoverflow.com/jobs?sort=p&l=Florida' -o ../../stackoverflow_Florida_Demo.json -t json
    scrapy crawl stackoverflow -a domain='https://stackoverflow.com/jobs?sort=p&l=Georgia' -o ../../stackoverflow_Georgia_Demo.json -t json

```

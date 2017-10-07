# scrapy-scrape-viewer

### Viewer For My Scrapes
#### This branch will add some fairs in the area

#### atom.io tools
* [pretty-json](https://atom.io/packages/pretty-json)

> The html was initially Semi-Cloned From: [kimberlythegeek/stackoverflow-denver_spider.py](https://github.com/kimberlythegeek/scrapy-project/blob/master/tutorial/spiders/stackoverflow-denver_spider.py)

* this version is focused on modifying the jobsups spider for the document-writer template json input

* I left almost all of the GUI alone. I just applied it to work with the .json generated with my own Scrapy bots.

#### Refer to my older [GIT-REPO-Branch](https://github.com/mezcel/googlemaps-api-helloworld/tree/expanded-idea-8-stackoverflow) to generate the .json this AngularJS App will use.

> * <i> I used a more efficient scrape technique than the one used in my the Google API Repo </i>

### Linux Terminal cheat:

### Update my scrape DB
```
    rm '/home/mezcel/github/scrapy-scrape-viewer/expresspros_Alabama_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/expresspros_Florida_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/expresspros_Georgia_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Alabama_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Florida_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Georgia_Demo.json'
    rm '/home/mezcel/github/scrapy-scrape-viewer/targetedjobfairs_Fairs_Demo.json'

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

    cd ..
    ls

    cd targetedjobfairs
    scrapy crawl targetedjobfairs -o ../../targetedjobfairs_Fairs_Demo.json -t json

```

### Add a new crawler to existing Virtual Environment
```
    cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
    source bin/activate

    scrapy startproject <project_name> [project_dir]
```

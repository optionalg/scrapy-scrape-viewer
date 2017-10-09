# Remove demo json to re-write
rm '/home/mezcel/github/scrapy-scrape-viewer/targetedjobfairs_Demo.json'
# Do Scrapy
cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
source bin/activate
ls
cd targetedjobfairs
scrapy crawl targetedjobfairs -o ../../targetedjobfairs_Demo.json
# deactivate virtualenv scrapyvirtualenv
deactivate

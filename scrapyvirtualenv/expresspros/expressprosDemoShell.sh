# Remove demo json to re-write
rm '/home/mezcel/github/scrapy-scrape-viewer/expresspros_Demo.json'
# Do Scrapy
cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
source bin/activate
ls
cd expresspros
scrapy crawl expresspros -a domain='https://workforce.expresspros.com/locations/state/Alabama,https://workforce.expresspros.com/locations/state/Georgia,https://workforce.expresspros.com/locations/state/Florida' -o ../../expresspros_Demo.json
# deactivate virtualenv scrapyvirtualenv
deactivate

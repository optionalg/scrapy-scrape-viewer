# Remove demo json to re-write
rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Florida_Demo.json'
rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Georgia_Demo.json'
rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Alabama_Demo.json'
rm '/home/mezcel/github/scrapy-scrape-viewer/stackoverflow_Demo.json'
# Do Scrapy
cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
source bin/activate
ls
cd stackoverflow
scrapy crawl stackoverflow -a domain='https://stackoverflow.com/jobs?sort=p&l=Florida,https://stackoverflow.com/jobs?sort=p&l=Georgia,https://stackoverflow.com/jobs?sort=p&l=Alabama' -o ../../stackoverflow_Demo.json
# deactivate virtualenv scrapyvirtualenv
deactivate
run in firefox
firefox /home/mezcel/github/scrapy-scrape-viewer/index.html
# exit
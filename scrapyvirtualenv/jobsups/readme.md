rm '/home/mezcel/github/scrapy-scrape-viewer/jobsups_Florida_Demo.json'
cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
source bin/activate
ls
cd jobsups
scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Florida' -o ../../jobsups_Florida_Demo.json -t json

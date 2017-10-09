# Remove demo json to re-write
rm '/home/mezcel/github/scrapy-scrape-viewer/jobsups_Demo.json'
# Do Scrapy
cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
source bin/activate
ls
cd jobsups
scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Florida,https://www.jobs-ups.com/search-jobs/Georgia,https://www.jobs-ups.com/search-jobs/Alabama' -o ../../jobsups_Demo.json
# deactivate virtualenv scrapyvirtualenv
deactivate

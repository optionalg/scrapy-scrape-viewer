# Remove demo json to re-write
rm '/home/mezcel/github/scrapy-scrape-viewer/jobsups_Florida_Demo.json'
rm '/home/mezcel/github/scrapy-scrape-viewer/jobsups_Georgia_Demo.json'
rm '/home/mezcel/github/scrapy-scrape-viewer/jobsups_Alabama_Demo.json'
rm '/home/mezcel/github/scrapy-scrape-viewer/jobsups_Demo.json'
# Do Scrapy
cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
source bin/activate
ls
cd jobsups
# scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Florida' -o ../../jobsups_Florida_Demo.json -t json
# scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Georgia' -o ../../jobsups_Georgia_Demo.json -t json
# scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Alabama' -o ../../jobsups_Alabama_Demo.json -t json
scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Florida,https://www.jobs-ups.com/search-jobs/Georgia,https://www.jobs-ups.com/search-jobs/Alabama' -o ../../jobsups_Demo.json
# deactivate virtualenv scrapyvirtualenv
deactivate
# run in firefox
# firefox /home/mezcel/github/scrapy-scrape-viewer/index.html
# exit

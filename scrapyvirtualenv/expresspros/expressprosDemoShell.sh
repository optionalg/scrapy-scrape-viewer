# Remove demo json to re-write
rm '/home/mezcel/github/scrapy-scrape-viewer/expresspros_Demo.json'
# Do Scrapy
cd '/home/mezcel/github/scrapy-scrape-viewer/scrapyvirtualenv'
source bin/activate
ls
cd expresspros
# scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Florida' -o ../../jobsups_Florida_Demo.json -t json
# scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Georgia' -o ../../jobsups_Georgia_Demo.json -t json
# scrapy crawl jobsups -a domain='https://www.jobs-ups.com/search-jobs/Alabama' -o ../../jobsups_Alabama_Demo.json -t json
scrapy crawl expresspros -a domain='https://workforce.expresspros.com/locations/state/Alabama,https://workforce.expresspros.com/locations/state/Georgia,https://workforce.expresspros.com/locations/state/Florida' -o ../../expresspros_Demo.json
# deactivate virtualenv scrapyvirtualenv
deactivate
#run in firefox
#firefox /home/mezcel/github/scrapy-scrape-viewer/index.html
# exit

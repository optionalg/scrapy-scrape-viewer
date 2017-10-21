#!/bin/sh
# cd [path to virtualenv]
cd
cd github/scrapy-scrape-viewer/scrapyvirtualenv

# make a temporary placeholder for the files/dirs i want to keep
mkdir -p myTempCrawlerContainer
ls

# Recursive Copy and paste the Dir i want to keep and use
# cp -r [deisred file path] [new desired dir path]
cp -r expresspros myTempCrawlerContainer
cp -r jobsups myTempCrawlerContainer
cp -r stackoverflow myTempCrawlerContainer
cp -r targetedjobfairs myTempCrawlerContainer

ls

# Delete unwanted imported folders
rm -r bin
rm -r include
rm -r lib
rm -r local
rm -r expresspros
rm -r jobsups
rm -r stackoverflow
rm -r targetedjobfairs
# Delete unwanted imported files
rm pip-selfcheck.json
rm arena.result

# Step up to its parent directory and define child folder as a virtual environment
cd ../
virtualenv scrapyvirtualenv
ls
cd scrapyvirtualenv
source bin/activate
pip install scrapy
ls
cd myTempCrawlerContainer
cp -r expresspros ../
cp -r jobsups ../
cp -r stackoverflow ../
cp -r targetedjobfairs ../
cd ..
rm -r myTempCrawlerContainer
deactivate

## Handling Scrapy Clones Virtual Environments

#### For systems without Python, PIP, Virtualenv, or Scrapy

```
# PIP Prerequisets
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev
sudo apt-get install zlib1g-dev libffi-dev libssl-dev

# Virtualenv Prerequisets
pip install virtualenv

# made a dir a virtual environment
cd my_project_folder
virtualenv my_project

# Inside a virtualenv, you can install Scrapy with pip
pip install scrapy

# make a new crawler
scrapy startproject [crawlerfolername]

# or paste in an existing crawler folder into the virtualenv folder
[Ctrl+C] then [Ctrl+Shift+V]
```
---

If I am cloning from a remote repo, I can not just import virtual environments "as-is".
The cleanest way to do things is just to rebuild Client side virtual/scrapy specific material.

```
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
```




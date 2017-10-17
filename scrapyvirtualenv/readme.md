# scrapyvirtualenv

## Virtual Environment for my Scrapy

The virtualenv needs to be made from scratch on each Linux. This work on my machine though.


##### Migrate virtual env between computers
Guidance / Clue:
[https://stackoverflow.com/questions/34993200/copy-complete-virtualenv-to-another-pc](https://stackoverflow.com/a/34993306)

Do following steps on source machine
```
cd '[path]/[virtualenv-directory]'
source bin/activate
pip freeze > requirements.txt
```

On other PC
```
# create a virtual environment using mkvirtualenv [environment_name]
cd '[path]/[virtualenv-directory]'
source bin/activate
pip install -r requirements.txt
```

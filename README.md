# ratebeerScraper
This is a ratebeer.com scrapper written in Python3.
I wrote it to scrape Brazillian beers stats, but its probably adaptable to other needs. 

Running this version you'l have access to a .CSV with the following content:<br>

name | brewer | beer_style | score | rating_num | abv | ibu | est_cal | overall | style | about | photo_url|
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
beer name | beer producer | type of beer | ratebeer score | num of ratings | abv | ibu | estimated calories | ratebeer overall | ratebeer style | beer description | beer photo url
<br> 
Way to run it: 
  REQUIREMENT: Selenium<br>
  Go to the project directory and type:<br>
  python3 scrapper.py
<br>If you eventually get blocked by the site, just run it again with the last brewery link and it wil keep crawling:<br>
Example: python3 scrapper.py 'lastBreweryLink' 


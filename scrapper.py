from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import pandas as pd
# import time

TIMEOUT = 10
IMPLICIT_TIMEOUT = 10
LOAD_TIMEOUT = 30
options = Options()
options.add_argument("--headless")#setting to use a headless browser
driver = webdriver.Firefox(firefox_options = options) #instantiate Selenium
def new_browser(url):
    global driver
    global TIMEOUT
    global IMPLICIT_TIMEOUT
    global LOAD_TIMEOUT
    driver.implicitly_wait(IMPLICIT_TIMEOUT) #selenium max wait
    driver.set_page_load_timeout(LOAD_TIMEOUT)
    try:
        driver.get(url)
    except TimeoutException:
        LOAD_TIMEOUT += 30
        driver = new_browser(url)
    return driver

def get_beer(beer_link):
    global TIMEOUT
    global IMPLICIT_TIMEOUT
    global driver
    global name, brewer, beer_style, score, rating_num, abv, ibu, est_cal, overall, style, about, photo_url
    print('ACESSING', beer_link)
    try:#makes selenium waits until 60 seconds for element showing
        driver = new_browser(beer_link)
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="beerName"]'))
        )
        driver.find_element_by_xpath('//*[@id="beer-card-read-more"]').click()
        element2 = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[3]/div[1]/div/div[2]'))
        )
        print('getting data')
        try:
            name.append(driver.find_element_by_xpath('//*[@id="beerName"]').text)
        except NoSuchElementException:
            name.append(None)
        try:
            brewer.append(driver.find_element_by_xpath('//*[@id="brewerLink"]').text)
        except NoSuchElementException:
            brewer.append(None)
        try:
            beer_style.append(driver.find_element_by_xpath('//*[@id="styleLink"]').text)
        except NoSuchElementException:
            beer_style.append(None)
        try:
            score.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/span[1]').text)
        except NoSuchElementException:
            score.append(None)
        try:
            rating_num.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/span[3]/span[1]').text)
        except NoSuchElementException:
            rating_num.append(None)
        #alcohol p volumn
        try:
            abv.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/span[1]').text)
        except NoSuchElementException:
            abv.append(None)
        try:
            ibu.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[3]/span[1]').text)
        except NoSuchElementException:
            ibu.append(None)
        try:
            est_cal.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[4]/span[1]').text)
        except NoSuchElementException:
            est_cal.append(None)
        try:
            overall.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/span[2]').text)
        except NoSuchElementException:
            overall.append(None)
        try:
            style.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/span[1]').text)
        except NoSuchElementException:
            style.append(None)
        try:
            about.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[3]/div[1]/div/div[2]').text)
        except NoSuchElementException:
            about.append(None)
        try:
            photo_url.append(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/img').get_attribute("src"))
        except NoSuchElementException:
            photo_url.append(None)
    except TimeoutException:
        print('TIMED OUT, increasing TIMEOUT')
        IMPLICIT_TIMEOUT += 10
        get_beer(beer_link) #retry
    # finally:
            # driver.quit()
            # print('quitting driver')
name = []
brewer = []
beer_style = []
score = []
rating_num = []
abv = []
ibu = []
est_cal = []
overall = []
style = []
about = []
photo_url = []
print('DONT WORRY, ITS NOT FREEZED')
driver = new_browser('https://www.ratebeer.com/breweries/brazil/0/31/')

try:#makes selenium waits until 60 seconds for element showing
    element = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]/div/div[1]/table/tbody/tr/td/a'))
    )
finally:
    print('GETTING BREWERIES')
    breweries = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[1]/div[2]/div/div[1]/table/tbody/tr/td/a') #extract breweries
    brewerie_links = []
    for brewery in breweries[::2]: #gets links
        brewerie_links.append(brewery.get_attribute("href"))
    print('GOT ', len(brewerie_links), 'BREWERIES')
    # print(breweries)
    # driver.quit() #closes unnused browser
    for brewery_link in brewerie_links: #access links
        print("GETTING BEERS FROM ", brewery_link)
        driver = new_browser(brewery_link)
        try:#waits until page is loaded
            element = WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, '//table[@id="brewer-beer-table"]/tbody/tr/td[not(em/label[@title="Currently out of production"])][not(em)]/strong/a'))
            )
        finally:#gets beers urls
            beers = driver.find_elements_by_xpath('//table[@id="brewer-beer-table"]/tbody/tr/td[not(em/label[@title="Currently out of production"])][not(em)]/strong/a') #extract  beer links
            beer_links = []
            for beer in beers:
                beer_links.append(beer.get_attribute("href"))
            print('GOT THIS MANY BEERS', len(beer_links))
            # driver.quit() #closes unnused browser
            for beer_link in beer_links:
                get_beer(beer_link)
    print('creating CSV')
    item = {
            'name' : name,
            'brewer' : brewer,
            'beer_style' : beer_style,
            #MAXSCORE IS 5
            'score' : score,
            'rating_num' : rating_num,
            #alcohol p volumn
            'abv' : abv,
            'ibu' : ibu,
            'est_cal' : est_cal,
            'overall' : overall,
            'style' : style,
            'about' : about,
            'photo_url': photo_url,
            }
    df = pd.DataFrame(data=item)
    df.to_csv('scrappedBeers.csv')

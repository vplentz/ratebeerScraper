# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrapy import Selector
import time

class BeerSpider(scrapy.Spider):
    name = "beer"

    def start_requests(self):
        urls = ['https://www.ratebeer.com/breweries/brazil/0/31/',]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse) #calls parse

    def parse(self, response): #parses breweries links
        breweries = response.xpath('//div[@id="active"]/table[@id="brewerTable"]/tr/td/a/@href').extract()
        #for brewery in breweries[::2]: #get only the links
        url = 'https://www.ratebeer.com'+breweries[0]
        yield scrapy.Request(url = url, callback=self.parse_brewery) #calls a brewery parser

    def parse_brewery(self, response): #parse single brewery, used to get all beers
        beers = response.xpath('//table[@id="brewer-beer-table"]/tbody/tr/td/strong/a/@href').extract() #extract  beer links
        driver = webdriver.Firefox() #instantiate Selenium
        driver.implicitly_wait(100) #selenium max wait
        for beer  in beers: #go trough beers links
            beer_url = 'https://www.ratebeer.com'+beer
            driver.get(beer_url) #call selenium to run the link
            try:#makes selenium waits until 60 seconds for element showing
                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="beerName"]'))
                )
                driver.find_element_by_xpath('//*[@id="beer-card-read-more"]').click()
                element2 = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[3]/div[1]/div/div[2]'))
                )
            finally: #when selenium find element
                item = {
                    'name' : driver.find_element_by_xpath('//*[@id="beerName"]').text,
                    'brewer' : driver.find_element_by_xpath('//*[@id="brewerLink"]').text,
                    'beer_style' : driver.find_element_by_xpath('//*[@id="styleLink"]').text,
                    #MAXSCORE IS 5
                    'score' : driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/span[1]').text,
                    'rating_num' : driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[1]/span[3]/span[1]').text,
                    #alcohol p volumn
                    'abv' : driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[2]/span[1]').text,
                    'ibu' : driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[3]/span[1]').text,
                    'est_cal' : driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[4]/span[1]').text,
                    'overall' : driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[1]/span[2]').text,
                    'style' : driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/span[1]').text,
                    'about' : driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div[1]/div/div[3]/div[1]/div/div[2]').text,
                }
                yield item

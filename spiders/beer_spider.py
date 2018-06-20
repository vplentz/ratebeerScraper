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
            yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     yield scrapy.FormRequest.from_response(response=response,
    #                                            formdata={'author': 'Steve Martin', 'tag': 'humor'},
    #                                            callback=self.parse_item)
    #
    def parse(self, response): #parses breweries links
        breweries = response.xpath('//div[@id="active"]/table[@id="brewerTable"]/tr/td/a/@href').extract()
        # breweries_links = []
        for brewery in breweries[::2]: #get only the links
            url = 'https://www.ratebeer.com'+brewery
            # print('BREWERY' ,url)
            yield scrapy.Request(url = url, callback=self.parse_brewery)

    def parse_brewery(self, response): #parse single brewery, used to get all beers
        # print('oi')
        beers = response.xpath('//table[@id="brewer-beer-table"]/tbody/tr/td/strong/a/@href').extract()
        driver = webdriver.Firefox()
        driver.implicitly_wait(100)
        for beer  in beers:
            beer_url = 'https://www.ratebeer.com'+beer
            driver.get(beer_url)
            try:
                element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="beerName"]'))
                )
            finally:
                name = driver.find_element_by_xpath('//*[@id="beerName"]').text
                print('BEEEEEEER', name)
                # driver.quit()
            # selector = Selector(text=driver.page_source)
            # name = selector.xpath('//*[@id="beerName"]').extract()

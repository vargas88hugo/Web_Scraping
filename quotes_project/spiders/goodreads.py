"""
At the beginning of the proyect a logic without components was used. From this 
commit that logic is changed with Items components and ItemLoader mechanism. The
Items are explained in items.py file and the ItemLoeader is the way it connects the
scrapy core with the fields of the Item file.
"""

import scrapy
from scrapy.loader import ItemLoader # ItemLoader provides a mechanism for populating scraped items
from demo_project.items import QuoteItem # Import class from the item file

class GoodReadsSpider(scrapy.Spider):
    # identity
    name = 'goodreads'

    # request
    def start_requests(self):
        """
        This method start the spider with a request to the page or pages
        """
        url = 'https://www.goodreads.com/quotes?page=1'
        
        yield scrapy.Request(url=url, callback=self.parse)

    # response
    def parse(self, response):
        """
        This method is to extract links and return the requests
        """
        for quote in response.xpath("//div[@class='quote']"): # here starts the implementation of xpath
            loader = ItemLoader(item=QuoteItem(), selector=quote, response=response)
            loader.add_xpath('text', ".//div[@class='quoteText']/text()[1]")
            loader.add_xpath('author', ".//span[@class='authorOrTitle']/text()")
            loader.add_xpath('tags', ".//div[@class='greyText smallText left']/a/text()")
            yield loader.load_item()


        """
        Here is used the next buttom of the page to iterate until the last page
        """
        next_page = response.xpath("//a[@class='next_page']/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
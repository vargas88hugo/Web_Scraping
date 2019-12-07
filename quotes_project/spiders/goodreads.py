import scrapy

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
        for quote in response.selector.xpath("//div[@class='quote']"): # here starts the implementation of xpath
            yield {
                'text': quote.xpath(".//div[@class='quoteText']/text()[1]").extract_first(), # extract_first() method extract only the first match and can be replaced with get() 
                'author': quote.xpath(".//span[@class='authorOrTitle']/text()").extract_first(),
                'tags': quote.xpath(".//div[@class='greyText smallText left']/a/text()").extract() # extrac() method extract all the matches and can be replaced with getall() 
            }

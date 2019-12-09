"""
The extracted data are dictionaries with a lack structure 
and it is not convenient for a consistent data. For this 
reason is used the item components in the class to define
a common output data format 

See documentation in:
https://docs.scrapy.org/en/latest/topics/items.html
"""

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def remove_quatations(value):
    return value.replace(u"\u201d", '').replace(u"\u201c", '').replace(u"\u2019", "'").replace(u"\u2026", '...').replace(u"\u00ef", 'i')

class QuoteItem(scrapy.Item):
    """
    The Items are declared with the Field method and within this the data 
    is parsed. 
    """
    text = scrapy.Field(
        input_processor = MapCompose(str.strip, remove_quatations), # MapCompose processor iterates and applies the function at each value
        output_processor = TakeFirst() # TakeFirst processor returns the first Non-Null value
    )
    author = scrapy.Field(
        input_processor = MapCompose(str.strip, remove_tags),
        output_processor = TakeFirst()
    )
    tags = scrapy.Field(
        input_processor = MapCompose(remove_tags),
        output_processor = Join(',')
    )


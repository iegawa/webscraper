import scrapy


class WebscraperItem(scrapy.Item):
    title = scrapy.Field()
    stars = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    category = scrapy.Field()

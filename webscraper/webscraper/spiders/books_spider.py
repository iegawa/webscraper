import scrapy
from ..items import WebscraperItem
from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail


class BooksSpider(scrapy.Spider):
    name = 'book_exchange'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        """ Contracts - get the title, number of stars, 
            price, availability and category of the books.

        @url http://books.toscrape.com/
        @returns requests 20 
        @scrapes title stars price availability category
        """
        
        all_books = response.css('article.product_pod')

        for books in all_books:
            items = WebscraperItem()
            title = books.css('a::attr(title)').get()
            stars = books.xpath('//p/@class').get()
            price = books.css('p.price_color::text').get()
            availability = books.css(
                'p.instock.availability::text').extract()[1]

            items['title'] = title
            items['stars'] = stars
            items['price'] = price
            items['availability'] = availability

            page_request = books.xpath('//article/h3/a').attrib['href']
            book_page = response.urljoin(page_request)
            category = scrapy.Request(
                book_page, callback=self.get_category, meta={
                    'item': items}, dont_filter=True)
            yield category

        
        next_page = response.xpath(
            "//a[contains(., 'next')]").attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def get_category(self, response):
        items = response.meta['item']
        try:
            items['category'] = response.xpath(
                '//ul/li[3]/a/text()').extract_first()
        except:
            items['category'] = None
        yield items


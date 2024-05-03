
import scrapy

from pathlib import Path

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {

                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get()
                
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    # start_urls = [

    #     'https://quotes.toscrape.com/page/1/',
    #     'https://quotes.toscrape.com/page/2/'

    # ]

    # def parse(self, response):
    #     page = response.url.split('/')[-2]
    #     filename = f'quotes_{page}.html'
    #     Path(filename).write_bytes(response.body)

    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {

    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall()

    #         }

    #     next_page = response.css('li.next a::attr(href)').get()
    #     if next_page is not None:
    #         yield response.follow(next_page, callback=self.parse)
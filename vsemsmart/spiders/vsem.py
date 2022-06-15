import scrapy


class VsemSpider(scrapy.Spider):
    name = 'vsem'
    allowed_domains = ['vsemsmart.ru']
    start_urls = ['http://vsemsmart.ru/']

    def parse(self, response):
        for link in response.css('a.parent-link.dropdown-img::attr(href)').extract():
            yield response.follow(link, callback=self.parse_full)

    def parse_full(self, response):
        for link in response.css("div.product-name a::attr(href)"):
            yield response.follow(link, callback=self.parse_page)
        next_page = response.css('div.col-sm-12.text-center > ul > li > a::attr(href)').extract()[-2]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_full)

    def parse_page(self, response):
        yield {
            "title": response.css("h1::text").extract(),
            "price": response.css("div.price span::text").extract(),
            "category": response.css("body > div.container > ul > li:nth-child(2) > a > span::text").extract(),
            "link": response.url
        }
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AuthorsSpider(CrawlSpider):
    name = "authors"
    allowed_domains = ["semanticscholar.org"]
    start_urls = ["https://www.semanticscholar.org/search?fos%5B0%5D=engineering&q=morocco&sort=relevance"]

    rules = (
        Rule(LinkExtractor(allow=(r"page=",))),
        Rule(LinkExtractor(allow=(r"authors",)), callback="parse_item"),
    )

    def parse_item(self, response):
        pass

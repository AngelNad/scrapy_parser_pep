import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        rows = response.xpath('//section[@id="numerical-index"]').css(
            'tbody tr')
        all_link_pep = rows.css('td').css('a::attr(href)').getall()
        for link_pep in all_link_pep:
            yield response.follow(
                urljoin(link_pep + '/'),
                callback=self.parse_pep
            )

    def parse_pep(self, response):
        title = response.css('.page-title::text').get()
        list_title = title.split()
        data = {
            'number': list_title[1],
            'name': ' '.join(list_title[3:]),
            'status': response.css('dt:contains("Status") + dd::text').get()
        }
        yield PepParseItem(data)

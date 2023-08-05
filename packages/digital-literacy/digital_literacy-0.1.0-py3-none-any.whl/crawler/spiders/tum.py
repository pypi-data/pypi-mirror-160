"""
In this Python script, we develop a web scraper that scrapes the module
descriptions of every module publicly available on the TUM website.

For TUM, along with Scrapy, we also use Selenium as there are some JavaScript
contents in the webpage that we need to extract.
"""

import scrapy
from pathlib import Path
from selenium import webdriver
from scrapy.http import HtmlResponse
from crawler.items import CrawlerItem
from scrapy.utils.python import to_bytes
from selenium.webdriver.chrome.options import Options

driver_path: Path = Path(__file__).parents[1].joinpath('drivers/chromedriver.exe')
log_path: Path = Path(__file__).parents[3].joinpath('logs/tum.log')
log_path.touch(exist_ok=True)

chrome_options = Options()
chrome_options.add_argument('--headless')


class TUMCrawler(scrapy.Spider):
    """
    This is the main class where we define our crawler, starting URL(s) and our
    parsing methods. This class inherits from the scrapy.Spider super class.
    Therefore, the attribute 'name' and the methods 'start_requests' and
    'parse' must be implemented.
    """
    name: str = 'TUM'
    custom_settings: dict = dict(
        LOG_LEVEL='INFO',
        LOG_FILE=f'{log_path}',
        LOG_FILE_APPEND=False,
        LOG_STDOUT=True
    )

    def start_requests(self) -> scrapy.Request:
        """The starting URL of the scraping process"""
        yield scrapy.Request(
            'https://campus.tum.de/tumonline/pl/ui/$ctx/wbSuche.mhbSuche'
        )

    def parse(self, response: scrapy.http.Response, **kwargs) -> scrapy.Request:
        """Parse the page to extract the modules' links"""
        max_pages: int = int(response.css('select option::text').extract()[-1])
        with webdriver.Chrome(executable_path=f'{driver_path}',
                              options=chrome_options) as driver:
            driver.get(response.url)
            for page in range(1, max_pages + 1):
                self.logger.info(f'Scraping page {page}/{max_pages}')
                javascript: str = f'javascript:document.forms[0].pStart.value=' \
                                  f'eval(({page}-1)*30+1);GLOBALsubmit(\'document.forms[0]\');'
                driver.execute_script(javascript)
                response = HtmlResponse(
                    url=driver.current_url,
                    body=to_bytes(driver.page_source),
                    encoding='utf-8'
                )
                module_links: list = response.css('.R+ td a::attr(href)').extract()
                for module_link in module_links:
                    module_link = 'https://campus.tum.de/tumonline/pl/ui/$ctx/' + module_link
                    yield scrapy.Request(module_link, callback=self.parse_module)

    # noinspection PyMethodMayBeStatic
    def parse_module(self, response: scrapy.http.Response) -> scrapy.Item:
        """Parse the module page to extract the relevant information"""
        self.logger.debug(f'Extracting module info from {response.url}')
        item: scrapy.Item = CrawlerItem()
        response = response.replace(body=response.body.replace(
            '</br>'.encode(), '\n'.encode()
        ))
        module_details: list = response.css('.KnotenDetailsLabelSeperator '
                                            '.MaskRenderer span.Mask')
        item['uni'] = 'TUM'
        item['name'] = module_details[0].css('span.bold::text').extract_first()
        item['department'] = module_details[1].css('span::text').extract_first()
        item['department_id'] = module_details[2].css('span::text').extract_first()
        item['ects'] = module_details[4].css('span::text').extract_first()
        item['id'] = module_details[7].css('span.bold::text').extract_first()
        item['valid_from'] = module_details[10].css('span::text').extract_first()
        item['valid_to'] = module_details[11].css('span::text').extract_first()
        item['level'] = response.css(
            '#ct_tab_DE .tab_internal_content tr:nth-child(2) tr:nth-child(1) '
            '.MaskSpacing .MaskRenderer::text'
        ).extract_first()
        item['language'] = response.css(
            '#ct_tab_DE .tab_internal_content tr:nth-child(2) tr:nth-child(6) '
            '.MaskSpacing .MaskRenderer::text'
        ).extract_first()
        item['prerequisites'] = response.css(
            'tr:nth-child(5) tr:nth-child(1) .MaskSpacing .MaskRenderer::text'
        ).extract_first()
        outcomes = response.css(
            'tr:nth-child(5) tr:nth-child(2) .MaskSpacing .MaskRenderer::text'
        ).extract_first()
        contents = response.css(
            'tr:nth-child(5) tr:nth-child(3) .MaskRenderer::text'
        ).extract_first()
        item['description'] = '\n\n'.join(filter(None, [outcomes, contents]))
        item['link'] = response.url
        item['link_type'] = 'HTML'
        yield item

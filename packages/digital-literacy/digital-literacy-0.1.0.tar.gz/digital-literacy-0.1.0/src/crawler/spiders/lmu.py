"""
In this Python script, we develop a web scraper that scrapes the module
descriptions of every module publicly available on the LMU website.

For LMU, along with Scrapy, we also use Selenium as there are some JavaScript
buttons in the webpage that we need to click on in order to change pages.

Since LMU displays its module descriptions as a PDF file, we use the PyMuPDF
module (fitz) to extract the PDF text and then crawl the text to extract the
information that we need. We implement an LMUParser for that purpose.
"""

import io
import fitz
import scrapy
import urllib.request

from pathlib import Path
from selenium import webdriver
from parsers import LMUParser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrapy.http import HtmlResponse
from crawler.items import CrawlerItem
from scrapy.utils.python import to_bytes
from selenium.webdriver.chrome.options import Options

driver_path: Path = Path(__file__).parents[1].joinpath('drivers/chromedriver.exe')
log_path: Path = Path(__file__).parents[3].joinpath('logs/lmu.log')
log_path.touch(exist_ok=True)

chrome_options = Options()
chrome_options.add_argument('--headless')


# noinspection PyMethodMayBeStatic, PyUnresolvedReferences
class LMUCrawler(scrapy.Spider):
    """
    This is the main class where we define our crawler, starting URL(s) and our
    parsing methods. This class inherits from the scrapy.Spider super class.
    Therefore, the attribute 'name' and the methods 'start_requests' and
    'parse' must be implemented.
    """
    name: str = 'LMU'
    custom_settings: dict = dict(
        LOG_LEVEL='INFO',
        LOG_FILE=f'{log_path}',
        LOG_FILE_APPEND=False,
        LOG_STDOUT=True
    )

    def start_requests(self) -> scrapy.Request:
        """The starting URL of the scraping process"""
        yield scrapy.Request(
            'https://www.lmu.de/de/studium/studienangebot/'
            'alle-studienfaecher-und-studiengaenge/index.html?'
        )

    def parse(self, response: scrapy.http.Response, **kwargs) -> scrapy.Request:
        """Parse the page to extract the modules' links"""
        self.logger.info('Starting the scraping process')
        page_num: int = 2
        with webdriver.Chrome(executable_path=f'{driver_path}',
                              options=chrome_options) as driver:
            driver.get(response.url)
            driver.find_element_by_css_selector('.form__input-group-button').click()
            # Wait until the page is completely loaded
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, f'#pagination__item-{page_num}')
                )
            )
            # Extract the response from Selenium to pass it on to Scrapy
            response = HtmlResponse(
                url=driver.current_url,
                body=to_bytes(driver.page_source),
                encoding='utf-8'
            )
            # Start Pagination
            while True:
                self.logger.info(f'Scraping page {page_num-1}')
                module_links: list = response.css('.filter-course-finder__result-title-link '
                                                  '::attr(href)').extract()
                for module_link in module_links:
                    if 'http' in module_link:
                        yield scrapy.Request(module_link, callback=self.parse_url)

                driver.find_element_by_css_selector(f'#pagination__item-{page_num}').click()
                try:
                    WebDriverWait(driver, 10).until(
                        expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, f'#pagination__item-{page_num+1}')
                        )
                    )
                except TimeoutException:
                    break
                response = HtmlResponse(
                    url=driver.current_url,
                    body=to_bytes(driver.page_source),
                    encoding='utf-8'
                )
                page_num += 1

    def parse_url(self, response: scrapy.http.Response) -> scrapy.Request:
        """Parse the modules' links to extract the links to PDFs"""
        list_1: list = response.css('.accordion__item+ .accordion__item '
                                    '.is-external::attr(href)').extract()
        list_2: list = response.css('#accordionItem-100082-0 '
                                    '.is-download::attr(href)').extract()
        list_3: list = response.css('#accordionItem-100082-1 '
                                    '.is-download::attr(href)').extract()

        module_pdf: bool = False
        for url in list_1 + list_2 + list_3:
            if url.endswith('.pdf'):
                module_pdf = True
                yield scrapy.Request(url, callback=self.parse_pdf)
                break
        if not module_pdf:
            self.logger.warning(f'No PDF found for {response.url}')

    def parse_pdf(self, response: scrapy.http.Response) -> scrapy.Item:
        """Parse the PDFs to extract the relevant information"""
        module_count: int = 0
        url_pdf: str = response.url
        item: scrapy.Item = CrawlerItem()
        url_contents: bytes = urllib.request.urlopen(url_pdf).read()
        pdf_stream: io.BytesIO = io.BytesIO(url_contents)
        pdf_file: fitz.Document = fitz.open(stream=pdf_stream, filetype='pdf')
        max_page: int = pdf_file.page_count
        cur_page: int = 0
        while cur_page < max_page:
            blocks: list = LMUParser.get_blocks(pdf_file, cur_page)
            if LMUParser.check_module(blocks):
                while True:
                    cur_page += 1
                    try:
                        new_blocks: list = LMUParser.get_blocks(pdf_file, cur_page)
                    except IndexError:
                        break
                    else:
                        if LMUParser.check_module(new_blocks):
                            break
                        blocks += new_blocks
                item['uni'] = 'LMU'
                item['name'] = LMUParser.get_name(blocks)
                item['level'] = LMUParser.get_level(blocks)
                item['language'] = LMUParser.get_lang(blocks)
                item['ects'] = LMUParser.get_ects(blocks)
                item['description'] = LMUParser.get_contents(blocks)
                item['link'] = url_pdf
                item['link_type'] = 'PDF'
                module_count += 1
                yield item
            else:
                cur_page += 1
        if module_count:
            self.logger.info(f'Scraped {module_count} modules from PDF {response.url}')
        else:
            self.logger.warning(f'Scraped {module_count} modules from PDF {response.url}')

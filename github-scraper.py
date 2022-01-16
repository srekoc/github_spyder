import re
import scrapy
from scrapy.selector import Selector
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser

class GitHubSpider(scrapy.Spider):
    name = "github_spider"
    start_urls = ['https://github.com/login']
    
    def parse(self, response):
        return FormRequest.from_response(response, 
                                         formdata={
                                                   'password':{self.github_pass}, 
                                                   'login':{self.github_user},
                                                  }, 
                                         callback=self.parse_page1)    
    
    def parse_page1(self, response):
        # open_in_browser(response)
        github_server_url = 'https://github.com'
        request_url = f'{github_server_url}/search?q={self.search_string}+language:{self.language_type}&type=Code'
        # yield {'result': request_url}
        return scrapy.Request(request_url,callback=self.parse_page2)
                          
    def parse_page2 (self, response):
        # open_in_browser(response)
        for searchset in response.xpath('//div[contains(@class,"code-list-item")]'):
            final_str = ""
            final_str_l = []
            final_str_m = ""
            for line in searchset.xpath('.//td[contains(@class, "blob-code")]'):
                text = "".join(line.xpath('.//text()').extract())
                #result = re.match('password\'\]\s*\=\s*\\"', text)
                #if result:
                final_str += text.strip() + "\n"
                 
            yield {
                'repo_name' : searchset.xpath('.//div[contains(@class, "flex-auto")]/a[1]/text()').extract_first(),
                'filename'  : searchset.xpath('.//div[contains(@class, "flex-auto")]/a[2]/@title').extract_first(),
                'updated'   : searchset.xpath('.//span[contains(@class, "updated-at")]/relative-time/text()').extract_first(),
                'code'      : final_str,
            }            
        # follow pagination link
        next_page_url = response.xpath('//a[@class="next_page"]/@href').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_page2)

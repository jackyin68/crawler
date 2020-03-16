# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib import parse
from baidu_info.items import UrlInfoItem
from scrapy import Request
import urllib
from urllib import request


class BaiduSpider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = []

    # params = {"wd": "上海交通大学"}
    params = {"wd": "nlp语义搜索上海招聘"}
    wd = parse.urlencode(params)
    query_url = 'http://www.baidu.com/s?' + wd
    start_urls.append(query_url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36',
        'Cookie': 'BAIDUID=01791EBEB0B10CCA8BE39D9E631D9ECB:FG=1; PSTM=1583941820; BIDUPSID=15C0ED42CAAA9E49274869C6DD1F2217; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_UPN=123353; BDUSS=lhZ21YREtUSmFVZU5aLUZ4Ukd6cVB6ajY1eUp6YklMc084ZH5tNU9RamR5NUZlRVFBQUFBJCQAAAAAAAAAAAEAAAC05Ph0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN0-al7dPmpeRG; BDSFRCVID=d30sJeCCxG3ewrTuHhKyXGLOJQBTF9vvRq-x3J; H_BDCLCKID_SF=JRAjoK-XJDv8fJ6xhbo_-D60e2T22-usBN4LQhcH0hOWsIONeqJo5tLwD-AH0xJ3JD6KaM3obn6Feb7hDUC0Djb-Da8fJTnJ-D6206uatRcoH6rnhPF3065QKP6-3MJO3b77anrFbR5ChU3HbMo0h689BPcOBPkHJJrgohFLtDthhDPxj5K35n-Wqx5Ka43tHD7yWCv90hQcOR5J35onDPI4jfbtBPj4a2jGoKKb5hvv8CTO3hOmM4t70GoDBj8J0jn85MQkW-OHsq0x0bOcbUuNL4OaBjjuLDOMahkM5h7xOKQoQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTXDa_DqT8JtJ3fL-082-5HjJbpMtvEq4tehHnt-Prd-KOtQJOHqRoffb0I5JOVBPt_hq3Ka4bXqCCDonDhjt5MDf7zbtOE5trK-HLjq-Djb67Z0lOnMp05jxIG-no1-xLgyMnqbqJn-jbaapnaBpo5MIO_e6K5D553DN-fqbbfb-oEBnTM2Ru_Hn7zeP85DbtpbtbmhU-e56vH-P5d2pvBoh3sXU6GLl0zeqjqQJ_LMn7ZVJO-KKCMMD_wDU5; delPer=0; BD_CK_SAM=1; PSINO=3; BD_HOME=1; sugstore=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=30974_1422_21081_30794_30904_30824_31085_26350; H_PS_645EC=5ae9bE2M%2Bj9c50kD1hK%2BqM3ZwCzm5kBMnPQzWi00gji4dIoRbXrEQlNPivk; BDSVRTM=113',
    }

    rules = (
        # Rule(LinkExtractor(allow=r'.*/s?' + wd + '.*'), callback='parse_url', follow=True),
        # Rule(LinkExtractor(allow=r'.*/s\?.+&pn=.+'), callback='parse_url', follow=True),
        # Rule(LinkExtractor(allow=r'.*/s\?wd=%E5%B0%B9%E5%BF%97%E6%AD%A6&pn=.+'), callback='parse_url', follow=True),
        # Rule(LinkExtractor(allow=r'https://www.baidu.com/link?url=.*'), callback='parse_content', follow=False),
        Rule(LinkExtractor(allow=r'.*/s\?' + wd + '&pn=.+&rsv_page=1'), callback='parse_url', follow=True),
        Rule(LinkExtractor(allow=r'.*/s\?' + wd + '&pn=.+'), callback='parse_url', follow=False),
        # Rule(LinkExtractor(allow=r'.*/s\?' + wd + '&pn=.+&rsv_page=1'),  follow=True),
        # Rule(LinkExtractor(allow=r'.*/s\?' + wd + '&pn=.+'), follow=False),
        # Rule(LinkExtractor(allow=r'https://www.baidu.com/link?url=.*'), callback='parse_content', follow=True),
    )

    def parse_url(self, response):
        results = response.xpath("//div[@id='content_left']/div[contains(@class,'result')]")
        for result in results:
            link = result.xpath("./h3/a/@href").get()
            print(f"=================link: {link}")
            # req = request.Request(link, headers=self.headers)
            # content = request.urlopen(req).read().decode("gb18030", "ignore")
            content = ""
            # print(f"content: {content}")
            title = result.xpath("./h3/a/text()").getall()
            title = "".join(title)
            abstract = result.xpath(".//div[@class='c-abstract']/text()").getall()
            abstract = "".join(abstract)
            # print(f"title: {title}")
            # print(f"abstract: {abstract}")
            url_info = UrlInfoItem(link=link, title=title, abstract=abstract, content=content)
            yield url_info

    def parse_content(self, response):
        pass
        # content = response.read()
        # print(content)

    def start_requests(self):
        cookies = {"BAIDUID": "01791EBEB0B10CCA8BE39D9E631D9ECB:FG=1", "BDORZ": "B490B5EBF6F3CD402E515D22BCDA1598",
                   "BDSFRCVID": "d30sJeCCxG3ewrTuHhKyXGLOJQBTF9vvRq-x3J",
                   "BDUSS": "lhZ21YREtUSmFVZU5aLUZ4Ukd6cVB6ajY1eUp6YklMc084ZH5tNU9RamR5NUZlRVFBQUFBJCQAAAAAAAAAAAEAAAC05Ph0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN0-al7dPmpeRG",
                   "BD_CK_SAM": "1", "BD_UPN": "123353", "BIDUPSID": "15C0ED42CAAA9E49274869C6DD1F2217",
                   "COOKIE_SESSION": "5682_0_9_9_42_77_0_3_9_9_8_3_5678_0_2_0_1584274741_0_1584274739%7C9%230_0_1584274739%7C1",
                   "H_BDCLCKID_SF": "JRAjoK-XJDv8fJ6xhbo_-D60e2T22-usBN4LQhcH0hOWsIONeqJo5tLwD-AH0xJ3JD6KaM3obn6Feb7hDUC0Djb-Da8fJTnJ-D6206uatRcoH6rnhPF3065QKP6-3MJO3b77anrFbR5ChU3HbMo0h689BPcOBPkHJJrgohFLtDthhDPxj5K35n-Wqx5Ka43tHD7yWCv90hQcOR5J35onDPI4jfbtBPj4a2jGoKKb5hvv8CTO3hOmM4t70GoDBj8J0jn85MQkW-OHsq0x0bOcbUuNL4OaBjjuLDOMahkM5h7xOKQoQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjTXDa_DqT8JtJ3fL-082-5HjJbpMtvEq4tehHnt-Prd-KOtQJOHqRoffb0I5JOVBPt_hq3Ka4bXqCCDonDhjt5MDf7zbtOE5trK-HLjq-Djb67Z0lOnMp05jxIG-no1-xLgyMnqbqJn-jbaapnaBpo5MIO_e6K5D553DN-fqbbfb-oEBnTM2Ru_Hn7zeP85DbtpbtbmhU-e56vH-P5d2pvBoh3sXU6GLl0zeqjqQJ_LMn7ZVJO-KKCMMD_wDU5",
                   "H_PS_645EC": "0019syKp1%2BJNPq8a13sqYy68oJb4jLvtmsDRMkDxZxOvofTZjIg8yakvHPc",
                   "H_PS_PSSID": "30974_1422_21081_30794_30904_30824_31085_26350", "PSINO": "3", "PSTM": "1583941820",
                   "delPer": "0", "sugstore": "0"}

        # print(cookies)
        yield scrapy.Request(url=self.start_urls[0],
                             cookies=cookies,
                             headers=self.headers,
                             callback=self.parse,
                             dont_filter=True)

    def _build_request(self, rule, link):
        r = Request(url=link.url, headers=self.headers, errback=self._errback, callback=self._callback)
        r.meta.update(rule=rule, link_text=link.text)
        return r

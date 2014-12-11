# -*- coding: utf-8 -*-
from scrapy import Spider, log
from scrapy.http import Request
from musicgeeks.items import SongPage
from dateutil import parser
import urlparse

class SongsSpider(Spider):
    name = "songs"
    allowed_domains = ["musicgeeks.co"]
    start_urls = ('http://www.musicgeeks.co/all',)

    def parse(self, response):
      songs = response.xpath("//li/a[@class='post-link']/@href").extract()

      for song in songs:
        url = urlparse.urljoin(response.url[:-4], song.strip())
        yield Request(url=url, callback=self.parseSongPage)

    def parseSongPage(self, response):
      song = SongPage()
      song['url'] = response.url
      song['slug'] = urlparse.urlparse(response.url).path.replace('/', '')
      song['soundcloud_url'] = response.xpath("//iframe/@src").extract()[0]
      song['gif_url'] = response.xpath("//img[@class='dancing-gif']/@src").extract()[0]

      love_divs = response.xpath("//div[@class='post-love']/p")
      if love_divs:
        for n in range(0,3):
          check = love_divs[n].extract()
          value = check.partition('<br>')[2][:-4]
          if 'WHO' in check:
            song['who_where'] = value
          elif 'CRED' in check:
            song['cred'] = value
          else:
            song['love'] = value

      song['page_title'] = response.xpath("//header[@class='post-header']").xpath(".//h1/text()").extract()[0]
      song['posted_on'] = parser.parse(response.xpath("//head/meta[@property='article:published_time']/@content").extract()[0]).strftime("%Y-%m-%d %H:%M:%S")
      return song
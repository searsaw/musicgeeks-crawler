# -*- coding: utf-8 -*-
from scrapy import Spider, log
from scrapy.http import Request
from musicgeeks.items import SongPage
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
      log.msg('Creating item from %s' % response.url, level=log.INFO)
      song = SongPage()
      song['url'] = response.url
      song['soundcloud_url'] = response.xpath("//iframe/@src").extract()
      song['gif_url'] = response.xpath("//img[@class='dancing-gif']/@src").extract()

      love_divs = response.xpath("//div[@class='post-love']/p")
      if love_divs:
        song['love'] = love_divs[0].extract()[11:-4]
        song['who_where'] = love_divs[1].extract()[21:-4]
        song['cred'] = love_divs[2].extract()[11:-4]

      post_header = response.xpath("//header[@class='post-header']")
      song['page_title'] = post_header.xpath(".//h1/text()").extract()
      song['posted_on'] = post_header.xpath(".//p[@class='meta']/text()").extract()
      return song
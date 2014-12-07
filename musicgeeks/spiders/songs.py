# -*- coding: utf-8 -*-
from scrapy import Spider
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
      song = SongPage()
      song['url'] = response.url
      # song['page_title'] =
      # song['artist'] =
      # song['song_title'] =
      # song['soundcloud_url'] =
      # song['gif_url'] =
      # song['love'] =
      # song['who_where'] =
      # song['cred'] =
      # song['attribution'] =
      # song['posted_on'] =
      return song
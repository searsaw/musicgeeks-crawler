from scrapy import Field

class SongPage(scrapy.Item):
  url = Field()
  page_title = Field()
  artist = Field()
  song_title = Field()
  soundcloud_url = Field()
  gif_url = Field()
  love = Field()
  who_where = Field()
  cred = Field()
  attribution = Field()
  posted_on = Field()
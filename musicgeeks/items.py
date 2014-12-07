from scrapy import Field, Item

class SongPage(Item):
  url = Field()
  page_title = Field()
  artist = Field()
  song_title = Field()
  soundcloud_url = Field()
  gif_url = Field()
  love = Field()
  who_where = Field()
  cred = Field()
  posted_on = Field()
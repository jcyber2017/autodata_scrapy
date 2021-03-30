import scrapy
import json

class MarksSpider(scrapy.Spider):
  name = 'marks'

  start_urls = ['https://www.auto-data.net/en/allbrands']
  allowed_domains = ['www.auto-data.net']

  def parse(self, response):
    markite = response.css('div.brands')
    links = markite.css('a.marki_blok::attr(href)').getall()
    names = markite.css('a.marki_blok strong::text').getall()
    images = markite.css('a.marki_blok img::attr(src)').getall()
    data = []
    for x in range(0, len(links)):
      data.append({'name': names[x],
                   'url': response.urljoin(links[x]),
                   'image': response.urljoin(images[x])})
    with open('marks.json', 'w') as f:
      json.dump(data, f)
    return data

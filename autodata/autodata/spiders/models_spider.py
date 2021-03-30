import scrapy
import json

class ModelsSpider(scrapy.Spider):
  name = 'models'
  allowed_domains = ['www.auto-data.net']

  def start_requests(self):
    with open('marks.json', 'r') as f:
      data = json.load(f)
      result = []
      for row in data:
        if 'models' in row:
          result.append(row)
          continue
        yield scrapy.Request(row['url'], self.parse)

  def parse(self, response):
    modelite = response.css('ul.modelite')
    links = modelite.css('a.modeli::attr(href)').getall()
    names = modelite.css('a.modeli strong::text').getall()
    images = modelite.css('a.modeli img::attr(src)').getall()
    data = []
    for x in range(0, len(links)):
      data.append({'name': names[x],
                   'url': response.urljoin(links[x]),
                   'image': response.urljoin(images[x])})
    if not data:
      return []
    with open('marks.json', 'r') as f:
      marks = json.load(f)
      for x in range(0, len(marks)):
        if marks[x]['url'] != response.url:
          continue
        marks[x]['models'] = data
        break
      with open('marks.json', 'w') as f:
        json.dump(marks, f)
    return data

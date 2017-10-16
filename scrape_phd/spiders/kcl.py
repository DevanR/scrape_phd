# -*- coding: utf-8 -*-
import scrapy

#def get_row()
#
#def get_name()
#
#def get_email()
#
#def get_bio()


class KclSpider(scrapy.Spider):
    name = "kcl"
    start_urls = [
        'https://www.kcl.ac.uk/nms/depts/informatics/people/phdstudents.aspx/'
    ]
    download_delay = 1.5

    def parse(self, response):
        filename = "kcl.html"
        rows = response.css("tr")
        with open(filename, 'wb') as f:
            for row in rows:
                f.write(row.extract())
        self.log('Saved file %s' % filename)

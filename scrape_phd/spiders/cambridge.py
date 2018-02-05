# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv
import re

class KclSpider(scrapy.Spider):
    name = "cambridge"
    postfix = '@cl.cam.ac.uk' 
    start_urls = [
        'https://www.cl.cam.ac.uk/people/students.html'
    ]

    def parse(self, response):
        filename = "cambridge.csv"
        soup = BeautifulSoup(response.text, 'lxml')
        with open(filename, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            table = soup.find("table", {"class": "directory"})
            rows = table.findChildren("tr")

            for row in rows[2:]:
                if len(row.contents) > 1:
                    name = ' '.join(row.contents[0].text.split(',')[::-1])
                    email = row.contents[3].text.strip('\n')
                    email = email + self.postfix
                    print("{}, {}".format(name, email))
                    writer.writerow([name, email])
        self.log('Saved file %s' % filename)

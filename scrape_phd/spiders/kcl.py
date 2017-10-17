# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv
import re
regex = re.compile('[^a-zA-Z ]')

class KclSpider(scrapy.Spider):
    name = "kcl"
    start_urls = [
        'https://www.kcl.ac.uk/nms/depts/informatics/people/phdstudents.aspx/'
    ]

    def parse(self, response):
        filename = "kcl.csv"
        soup = BeautifulSoup(response.text, 'lxml')
        with open(filename, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for row in soup.find_all("tr")[1:]:
                name = row.contents[1].text.strip()
                name = regex.sub('', name)
                email = (row.contents[3].text+'@kcl.ac.uk').strip()
                print("{}, {}".format(name, email))
                writer.writerow([name, email])
        self.log('Saved file %s' % filename)

# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv
import re
regex = re.compile('[^a-zA-Z ]')

class WarwickSpider(scrapy.Spider):

    name = "warwick"
    start_urls = [
            'https://www2.warwick.ac.uk/fac/sci/eng/people/rd/'
            ]
    student_header = "https://www2.warwick.ac.uk/fac/sci/eng/people/bio/?tag="
    
    filename = "warwick.csv"
    f = open(filename, 'w')
    writer = csv.writer(f, delimiter=',')

    def parse(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        for row in soup.find_all("tr"):
            tag = row.a['href'].split('=')
            if len(tag) == 2:
                student_url = self.student_header + tag[1]
                yield scrapy.http.Request(student_url, callback=self.parse_2)


    def parse_2(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        name = soup.find_all("h2")
        name = name[0].text.strip().split(',')[0]

        email = soup.find_all("h6")
        email = email[0].contents[5].text
        email = email[email.find("(")+1:email.find(")")].strip("\"")
        email = email.replace(" ", ".") + "@warwick.ac.uk"

        print("{}, {}".format(name, email))
        self.writer.writerow([name, email])




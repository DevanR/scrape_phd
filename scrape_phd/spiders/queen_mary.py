# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv
import re
regex = re.compile('[^a-zA-Z ]')

class QueenMarySpider(scrapy.Spider):
    name = "queen_mary"
    start_urls = [
        'http://www.eecs.qmul.ac.uk/people/phd/'
    ]
    filename = "queen_mary.csv"
    f = open(filename, 'w')
    writer = csv.writer(f, delimiter=',')

    def parse(self, response):

        filename = "queen_mary.csv"
        soup = BeautifulSoup(response.text, 'lxml')

        last_page = soup.findAll("a", { "class" : "page-next" })[1]['href']
        total_pages = int(last_page.split('/')[-1].strip('P'))/10 + 1

        url_list = []
        for num in range(int(total_pages)):
            if num  == 0:
                url_list.append('http://www.eecs.qmul.ac.uk/people/phd/' + str(num))
            else:
                url_list.append('http://www.eecs.qmul.ac.uk/people/phd/P' + str(num*10))
            
        for page in url_list:
            yield scrapy.http.Request(page, callback=self.parse_2)

    def parse_2(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        students = soup.findAll("div", { "class" : "person-left-details" })

        for student in students:
            name = student.text.split("\n")[1][:-1] 
            email = student.text.split("\n")[4]

            print("{}, {}".format(name, email))
            self.writer.writerow([name, email])

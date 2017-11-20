# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import csv
import re
regex = re.compile('[^a-zA-Z ]')

def find_last_page(soup):
    """
    Return the number of pages 
    """
    for i in range(1, 10):
        links = soup.findAll(text=str(i))
        if len(links) != 2:
            break
        page_num= links[0]
    return int(page_num)

class ImperialSpider(scrapy.Spider):
    name = "imperial"
    start_urls = [
        'http://www.imperial.ac.uk/electrical-engineering/about/people/research-postgraduates/',
        'http://www.imperial.ac.uk/electrical-engineering/about/people/taught-postgraduates/'
    ]
    filename = "imperial.csv"
    f = open(filename, 'w')
    writer = csv.writer(f, delimiter=',')

    def parse(self, response):

        filename = "imperial.csv"
        soup = BeautifulSoup(response.text, 'lxml')
        total_pages = find_last_page(soup)

        url_list = []
        if response.url == "http://www.imperial.ac.uk/electrical-engineering/about/people/taught-postgraduates/":
            url = "http://www.imperial.ac.uk/electrical-engineering/about/people/taught-postgraduates/?instanceid=%2felectrical-engineering%2fall-staff%2ftaught&pplist-action=people.html&page"
        if response.url == "http://www.imperial.ac.uk/electrical-engineering/about/people/research-postgraduates/":
            url = "http://www.imperial.ac.uk/electrical-engineering/about/people/research-postgraduates/?instanceid=%2felectrical-engineering%2fall-staff%2fpostgraduate&pplist-action=people.html&page="

        for num in range(1, total_pages):
            url_list.append(url + str(num))
            
        for page in url_list:
            yield scrapy.http.Request(page, callback=self.parse_2)

    def parse_2(self, response):

        soup = BeautifulSoup(response.text, 'lxml')

        students = soup.findAll("div", { "class" : "name-wrapper" })

        for student in students:
            name = student.find("span", {"class": "person-name"}).text
            email = student.find("a", {"class":"email"})["href"].split(":")[1]

            print("{}, {}".format(name, email))
            self.writer.writerow([name, email])

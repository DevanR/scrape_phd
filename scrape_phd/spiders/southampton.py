# -*- coding: utf-8 -*-
import csv
import re

import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
        StaleElementReferenceException,
        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

regex = re.compile('[^a-zA-Z ]')

class SouthhamptonSpider(scrapy.Spider):
    name = "southampton"
    start_urls = [
            'http://www.ecs.soton.ac.uk/people'
            ]
    filename = "southampton.csv"
    f = open(filename, 'w')
    writer = csv.writer(f, delimiter=',')

    driver = webdriver.PhantomJS()
    wait = WebDriverWait(driver, 10)

    def parse(self, response):
        self.driver.get(response.url)

        dismiss_flash_btn = self.wait.until(EC.element_to_be_clickable(
            (By.ID, 'js-flash-dismiss')))
        dismiss_flash_btn.click()

        search_bar = self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, 'search')))
        search_bar.send_keys("postgraduate research student")

        # To get actual number of pages
        pages = self.driver.find_elements_by_class_name("page")
        second_last_page = pages[-2]
        second_last_btn = self.wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, '3')))
        second_last_btn.click()

        pages = self.driver.find_elements_by_class_name("page")
        total_pages = len(pages)+1
        # Reset to first page
        pages[0].click()

        for page in range(1, total_pages):
            page_btn = self.wait.until(EC.element_to_be_clickable(
                (By.LINK_TEXT, str(page))))
            page_btn.click()

            # Scrape page
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            students = soup.findAll("tr")
            student_number = len(students)

            for index in range(1, student_number):
                url = 'http://www.ecs.soton.ac.uk'+students[index].contents[1].a['href']
                yield scrapy.http.Request(url, callback=self.parse_2)

        self.driver.quit()


    def parse_2(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        name = soup.findAll("h1")[0].text
        email = soup.findAll("a", property="email")[0].text

        print("{}, {}".format(name, email))
        self.writer.writerow([name, email])

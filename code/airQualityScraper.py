#! /usr/bin/env python

import urllib2
from selenium import webdriver
import time
import re
import csv
from bs4 import BeautifulSoup as bs

driver = webdriver.Firefox()

with open('stations.csv', "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    headers = ['Station Name', 'Address', 'Latitude', 'Longitude', 'Station Type', 'Height of Air Intake', 'Elevation ASL', 'Pollutants Measure']
    writer.writerow(headers)

    driver.get('http://airqualityontario.com/history/station.php')
    for i in range(1,40,1):
        driver.find_element_by_xpath("//select[@name='stationid']/option[" + str(i) + "]").click()
        driver.find_element_by_css_selector('.station-button').click()

        page = driver.page_source

        initial_soup = bs(page, "html.parser")
        for wr in initial_soup.find('sub'):
            wr.replace_with('')

        tables = initial_soup.findChildren('table')

        my_table = tables[0]

        rows = my_table.findChildren(['th', 'tr'])

        csvlist=[]

        for row in rows:
            cells = row.findChildren('td')
            for cell in cells:
                value = cell.text
                if value.find(":") == -1:
                    csvlist.append(value)
                else:
                    continue
        writer.writerow(csvlist)

import urllib.request
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

# find all states

url = 'https://www.nps.gov/index.htm'
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

searchList = soup.find('ul', attrs={'class': 'dropdown-menu SearchBar-keywordSearch'})
if not searchList:
    print('Cannot find states.')
    exit(0)

stateURLs = {}
for searchItem in searchList.find_all('li'):
    stateLink = searchItem.a
    if stateLink:
        stateName = stateLink.string
        stateURL = stateLink['href']
        if stateName and stateURL:
            stateURLs[stateName] = stateURL
if not stateURLs:
    print('Cannot find states.')
    exit(0)

# find all parks

parks = [['Type', 'Name', 'Description', 'Location', 'State']]

for stateName, stateURL in stateURLs.items():
    stateURL = 'https://www.nps.gov' + stateURL
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    try:
        client = webdriver.Chrome(options=options)
        client.get(stateURL)
        parkList = client.find_element_by_id('list_parks').find_elements_by_class_name('list_left')
        for parkItem in parkList:
            parkType = parkItem.find_element_by_tag_name('h2').text
            if not parkType:
                parkType = "None"
            parkName = parkItem.find_element_by_tag_name('h3').text
            if not parkName:
                parkName = "None"
            parkDescription = parkItem.find_element_by_tag_name('p').text
            if not parkDescription:
                parkDescription = "None"
            parkLocation = parkItem.find_element_by_tag_name('h4').text
            if not parkLocation:
                parkLocation = "None"
            parkState = stateName
            park = [parkType, parkName, parkDescription, parkLocation, parkState]
            parks.append(park)
    except Exception as e:
        print(e)
        pass

# write csv file

with open('parks.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(parks)

import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

base_url = 'https://minneapolis.craigslist.org'
url = base_url + '/search/cto'
for i in range(4):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    cars = []
    for car in soup.find_all(attrs={'class':'result-row'}):
        price_tag = car.find(attrs={'class':'result-price'})
        title_tag = car.find(attrs={'class':'result-title'})
        try:
            cost = int(price_tag.text[1:])
            year = int(title_tag.text.split()[0])
        except:
            print(title_tag.text)
            continue

        if cost < 100000 and cost > 1: # because some people are just dumb
            if year < 100 and year >= 20:
                year += 1900
            elif year >=0 and year < 30:
                year += 2000
            
            if year > 2020 or year < 1990:
                print(title_tag.text)
                continue

            plt.plot(year, cost, 'ro')

    url = base_url + soup.find(attrs={'class':'next'})['href']


# plt.plot(cars, 'ro')
plt.ylabel('Minneapolis Car Prices')
plt.show()
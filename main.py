import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

MAX_PRICE = 10000


def get_pages(url, i, base_url):

    years = []
    costs = []

    for _ in range(i):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for car in soup.find_all(attrs={'class':'result-row'}):
            price_tag = car.find(attrs={'class':'result-price'})
            title_tag = car.find(attrs={'class':'result-title'})
            try:
                cost = int(price_tag.text[1:])
                year = int(title_tag.text.split()[0])
            except:
                # print(title_tag.text)
                continue

            if cost < 100000 and cost > 1: # because some people are just dumb
                if year < 100 and year >= 20:
                    year += 1900
                elif year >=0 and year < 30:
                    year += 2000
                
                if year > 2020 or year < 1990:
                    # print(title_tag.text)
                    continue

                years.append(year)
                costs.append(cost)
                # print('year', year, 'cost', cost)

        if not soup.find(attrs={'class':'next'}):
            print('breaking')
            break   # no next button; return what we have
        url = base_url + soup.find(attrs={'class':'next'})['href']
        print(url)
    return years, costs
    
class CL_Formatter:
    def __init__(self, city='minneapolis', options={}):
        self.city = city
        self.options = options
        self.base_url = 'https://{}.craigslist.org'.format(self.city)

    def format_url(self):
        url = self.base_url + '/search/cto?'
        url += "&".join(['{}={}'.format(k,v) for k,v in self.options.items()])
        return url

    def set_opt(self, key, value):
        self.options[key] = value

    def get_base_url(self):
        return self.base_url

def get_costs_by_year(make, craigslist_results_pages=3):
    clf.set_opt('auto_make_model', make)
    years, costs = get_pages(
        clf.format_url(),
        craigslist_results_pages,
        clf.get_base_url()
    )
    
    costs_by_year = {}
    for year, cost in zip(years, costs):
        if year not in costs_by_year:
            costs_by_year[year] = []
        costs_by_year[year].append(cost)
    return costs_by_year


def graph_costs_by_year(make, drawing_context):
    costs_by_year = get_costs_by_year(make)
    drawing_context.boxplot(
        [costs_by_year[i] for i in sorted(costs_by_year.keys())],
        labels=[x if x%3==0 else '' for x in sorted(costs_by_year.keys())]
    )
    drawing_context.set_title(make + 's')
    drawing_context.set_ylim(ymin=0, ymax=MAX_PRICE)


# set up formatter
clf = CL_Formatter('minneapolis', {
    'max_price':MAX_PRICE,      # $0 - $10k
    'auto_title_status':1,  # clean title
    'auto_transmission':2,  # auto trans
})

# makes = ['Honda', 'Kia', "Mitsubishi", "Toyota"]  # asian
# makes = ['Chrysler', 'Ford', "Dodge", "Chevy"]    # american
# makes = ['VW', 'Mercedes', "Audi", "BMW"]         # german
# makes = ['Hyundai', 'Ford', 'Honda', 'BMW']
# makes = ['Lexus', 'Acura', 'Scion', 'BMW']  # luxury
makes = [...]   # TODO: Only filter for good cars. ;)

fig, axs = plt.subplots(2, 2)
for i,make in enumerate(makes):
    graph_costs_by_year(make, axs[1 if i>1 else 0, 0 if i%2==0 else 1])
plt.show()
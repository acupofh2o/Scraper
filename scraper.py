from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from time import sleep
from time import time
from random import randint
from user_agent import generate_user_agent
from lxml.html import fromstring
from itertools import cycle


random_headers = {'User-Agent': generate_user_agent()}

requests = 0
nr_of_pages = 100
pages = [str(i) for i in range(0, nr_of_pages)]

ids = []
names = []
localss = []
prices = []
nrcam = []
size = []


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


proxies = get_proxies()

proxy_pool = cycle(proxies)


def get_summary(anunt):

    id = str(anunt.a['id'])[6:]
    ids.append(id)

    nume = anunt.h2.a.text
    names.append(nume)

    localizare = anunt.find('div', class_='localizare').p.text
    localss.append(localizare.lstrip())

    preturi = anunt.find_all('span', {"class": ["pret-mare", "tva-luna"]})
    if (anunt.find_all('span', {"class": ["pret-mare", "tva-luna"]})):
        preturi = anunt.find_all('span', {"class": ["pret-mare", "tva-luna"]})
        if (preturi[0].get_text()) is not None:
            if (preturi[1].get_text()) is not None:
                pret = preturi[0].get_text().lstrip() + ' ' + preturi[1].get_text().lstrip()
    else:
        if (anunt.find('div',
                       class_='pret necomunicat')):
            """ preturi=anunt.find('div', class_='pret necomunicat')
            pret=preturi.get_text().lstrip() """
            pret = 'PretNecomunicat'

    prices.append(pret)

    nr_camere = anunt.find('ul', class_='caracteristici').find_all('span')[0].get_text().lstrip()
    nrcam.append(nr_camere)

    mp = anunt.find('ul', class_='caracteristici').find_all('span')[1].get_text().lstrip()
    size.append(mp)


start_time = time()



for page in pages:

    proxy = next(proxy_pool)

    url = 'https://www.imobiliare.ro/vanzare-apartamente/bucuresti?pagina='

    response = get(url + page, timeout=10, headers=random_headers, proxies={"http": proxy})

    sleep(randint(4, 20))

    requests = requests + 1

    timp_trecut = time() - start_time

    freq = requests / timp_trecut

    print 'Page#: ' + str(requests), 'Frequency: ' + str(freq) + ' requests/s'

    if response.status_code != 200:
        print "Warning! Request: " + str(requests) + 'has an error status code:' + str(response.status_code)

    html_soup = BeautifulSoup(response.text, 'html.parser')
    anunt_containers = html_soup.find_all('div', itemtype='http://schema.org/Offer')

    for anunt in anunt_containers:
        get_summary(anunt)

table = pd.DataFrame({
    'ID': ids,
    'Nume': names,
    'Metri_Patrati': size,
    'Localizare': localss,
    'Pret': prices,
    'Nr_Camere': nrcam

})

tablecolumns = ['ID', 'Nume', 'Nr_Camere', 'Metri_Patrati', 'Pret', 'Localizare']
table = table.reindex(columns=tablecolumns)

print table.info()

table.to_csv("date_imobiliare.ro.csv", index=False, encoding='utf8')



table.to_json('date_imobiliare.json', orient='records', lines=True)

from bs4 import BeautifulSoup
import urllib3
from itertools import count
import pandas as pd

ZIP_CODE_URL = 'http://www.unitedstateszipcodes.org/wa/#zips-list'

STATE_ZIP_SEARCH_URL = 'http://farm.ewg.org/addrsearch.php?z=1&zip={zip}&page={page}'

def get_soup_from_link(link):
    http = urllib3.PoolManager()
    page = http.request('GET', link)

    if page.status == 200:
        return BeautifulSoup(page.data, 'html.parser')
    else:
        return None

zips_soup = get_soup_from_link(ZIP_CODE_URL)

#zip_containers = zips_soup.find_all('div', {'class': 'list-group-item'})

state_zips = list(map(lambda x: x.find('a').text,
                  zips_soup.find_all('div', {'class': 'list-group-item'})))

farmers = []
for zip in state_zips:
    for i in count():
        farm_soup = get_soup_from_link(STATE_ZIP_SEARCH_URL.format(zip=zip, page=i))
        trs = farm_soup.find_all('tr')[1:]
        if trs:
            farmers.extend(list(map(lambda y: (y[1].find('a').text, y[2].text ),
                               map(lambda x: x.find_all('td'), trs))))
        else:
            break

farmers_df = pd.DataFrame(farmers, columns = ['Name', 'Address'])

farmers_df.to_excel('washington_farmers.xls', index=False)
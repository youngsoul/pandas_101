import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


url = 'http://www.isp.state.il.us/districts/districtx.cfm?DistrictID='


df = pd.read_csv('./data/police-il/IL-clean.csv', usecols=['fine_grained_location'])

def process_district(district_id):
    # print(district_id)
    district_address = ''
    counties_served = ''

    # district 4 closed
    if district_id in [4, '4']:
        return {
            'district_id': district_id,
            'district_address': 'Village of Crestwood',
            'counties_serviced': 'Cook'
        }

    page = requests.get(f'{url}{district_id}')
    soup = BeautifulSoup(page.content, 'html.parser')
    """
    <td colspan="3" class="tmpl_tabbackgroundcolor">2700 Ogden Ave.&nbsp;&nbsp;Downers Grove,&nbsp;Illinois&nbsp;&nbsp;60515</td>        
    """
    elements = soup.find_all('td', {'class': 'tmpl_tabbackgroundcolor', 'colspan': '3'})
    if elements:
        district_address = elements[0].text
        counties_served = ''
        if len(elements) >= 2:
            counties_served = elements[1].text.strip()

    if counties_served:
        counties_served = [x.strip() for x in counties_served.split('\r\n')]
    # print(district_address, counties_served)
    return {
        'district_id': district_id,
        'district_address': district_address.replace('\xa0', ' '),
        'counties_serviced': counties_served[2:]
    }

unique_district_ids = df.fine_grained_location.unique()

for id in unique_district_ids:
    if id not in ['nan', np.nan]:
        d = process_district(id)
        print(d)
        print("-----------------")






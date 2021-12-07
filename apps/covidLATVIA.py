import requests
from datetime import date, timedelta

def get_covid():
    yesterday = date.today() - timedelta(days=1)
    today = date.today()
    try:
        URL = 'https://data.gov.lv/dati/lv/api/3/action/datastore_search?&resource_id=d499d2f0-b1ea-4ba2-9600-2c701b03bd4a&filters={{%22Datums%22:%22{}T00:00:00%22}}'.format(today)
        response = requests.get(URL)
        text = response.json()
        data = text['result']['records']
        skaits = data[0]['ApstiprinataCOVID19InfekcijaSkaits']
    except:
        URL = 'https://data.gov.lv/dati/lv/api/3/action/datastore_search?&resource_id=d499d2f0-b1ea-4ba2-9600-2c701b03bd4a&filters={{%22Datums%22:%22{}T00:00:00%22}}'.format(yesterday)
        response = requests.get(URL)
        text = response.json()
        data = text['result']['records']
        skaits = data[0]['ApstiprinataCOVID19InfekcijaSkaits']

    if (skaits%10 == 1 or skaits == 11):
        latviskojums1 = 'saslimis'
        latviskojums2 = 'cilvēks'
    else:
        latviskojums1 = 'saslimuši'
        latviskojums2 = 'cilvēki'
    return ':flag_lv: Latvijā vakar {} **{}** {}'.format(latviskojums1, skaits, latviskojums2)

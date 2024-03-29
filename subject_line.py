from urllib.parse import urlencode

import requests
import keyring

# delete this line after running the code once:
# keyring.set_password("zendesk", "your_zendesk_email", "your_zendesk_password")

my_query = input("Please enter your query search term: ")

# credentials = '[your_zendesk_email]', keyring.get_password("zendesk", "[your_zendesk_email]")

session = requests.Session()
session.auth = credentials


params = {
    'query': my_query,
    'page[size]': '100',
    'filter[type]': 'ticket'
}
# url = 'https://zybooks.zendesk.com/api/v2/search.json?' + urlencode(params)
url = 'https://zybooks.zendesk.com/api/v2/search/export.json?' + urlencode(params)

response = session.get(url)
if response.status_code != 200:
    print('Status:', response.status_code, 'Problem with the request. Exiting.')
    exit()

# clear contents of link.txt file
file = open("results.csv","r+")
file.truncate(0)
file.close()

while url:
    response = session.get(url)
    data = response.json()
    for result in data['results']:
        res = (result['url']).replace(".json", "")
        res = res.replace("https://zybooks.zendesk.com/api/v2/tickets/", "https://zybooks.zendesk.com/agent/tickets/")
        subj = result['subject']
        f = open("results.csv", "a")
        f.write(res)
        f.write('\t')
        f.write(subj)
        f.write("\n")
        print(res, subj)
        
    # url = data['next_page']
    if data['meta']['has_more'] == True:
        url = data['links']['next']
    else:
        break

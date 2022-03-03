from urllib.parse import urlencode
from urllib.request import urlopen

import requests
import keyring
import csv

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

# # clear contents of link.txt file
# file = open("links.txt","r+")
# file.truncate(0)
# file.close()

# "WGUC9582018" custom_field_360048185134:* -"BUG CORRECTION"
columns = ["Ticket", "User email"]
rows = []
while url:
    response = session.get(url)
    data = response.json()
    
    for result in data['results']:
        res_url = session.get(result['url'])
        res_data = res_url.json()
        # print(res_data)
        ticket = "https://zybooks.zendesk.com/agent/tickets/" + str(res_data['ticket']['id'])
        user_url = session.get("https://zybooks.zendesk.com/api/v2/users/" + str(res_data['ticket']['requester_id']) + ".json")
        # print (user_url)
        user_data = user_url.json()
        email = user_data['user']['email']

        
        temp = [ticket, email]
        print(temp)
        rows.append(temp)

        with open('links.csv', 'w') as f: 
            write = csv.writer(f) 
            write.writerow(columns) 
            write.writerows(rows) 

    
        
    # url = data['next_page']
    if data['meta']['has_more'] == True:
        url = data['links']['next']
    else:
        break
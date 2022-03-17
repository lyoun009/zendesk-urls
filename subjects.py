from urllib.parse import urlencode
from urllib.request import urlopen

import requests
import keyring
import csv

# delete this line after running the code once:
# keyring.set_password("zendesk", "your_zendesk_email", "your_zendesk_password")

file_name = input("Please enter your input file name: ")

credentials = 'lindsey.young@zybooks.com', keyring.get_password("zendesk", "lindsey.young@zybooks.com")
session = requests.Session()
session.auth = credentials



columns = ["Ticket", "Subject"]
rows = []

ff = open(file_name, "r")
for x in ff:
    url = x.replace("https://zybooks.zendesk.com/agent/tickets/", "https://zybooks.zendesk.com/api/v2/tickets/")

    response = session.get(url)
    data = response.json()
    
    ticket = "https://zybooks.zendesk.com/agent/tickets/" + str(data['ticket']['id'])
    tags = data['ticket']['tags']
    filter_object = filter(lambda a: 'subject' in a, tags)

    subject = ""
    for i in filter_object:
        subject = str(i)
        subject = subject.replace("subject:", "")

        
    temp = [ticket, subject]
    print(temp)
    rows.append(temp)

    with open('links.csv', 'w') as f: 
        write = csv.writer(f) 
        write.writerow(columns) 
        write.writerows(rows) 
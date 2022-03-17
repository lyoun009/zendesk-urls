# Zendesk URLs


## Setup
### Install necessary python3 packages

Install keyring (https://pypi.org/project/keyring/)
This is to store zendesk credentials so its NOT in plain text on the file. On macOS, it will use mac's Keychain to store the password. (Alternatively, you can hash the credentials instead too.)

    pip3 install keyring

Install requests library

    pip3 install requests



### Set credentials using keyring
In zendesk.py, change these lines of code accordingly:

    keyring.set_password("zendesk", "[your_zendesk_email]", "[your_zendesk_password]")

    credentials = '[your_zendesk_email]', keyring.get_password("zendesk", "[your_zendesk_email]")


### Run the script once (to set up the credentials)

  

    python3 zendesk.py


### Delete the line in the script where you set your credentials

    keyring.set_password("zendesk", "[your_zendesk_email]", "[your_zendesk_password]"



## How to Search

- when prompted, you can paste in the query as you would normally search Zendesk

Examples:

    49218884
 
    group:support updated<"2021-03-31" tags:instructor updated>"2021-01-01"
    
    subject:"rush"
    
    "manual tests"

All of these would work just fine.


The script should print the tickets to the terminal. It will also print the tickets to a "links.txt" file. 

**NOTE: the links.txt file will be overwritten every time the script is run.**

## Variations
#### ``zendesk.py``
- the original script
- input: a Zendesk query
- output: a .txt file of ticket URLs
#### ``user-emails.py``
- gets ticket URLs + requestor email
- input: a Zendesk query
- output: a .csv file of ticket URLs + requestor email
#### ``subjects.py``
- used for getting the subject (ie. cpp, python3, etc.) of a ticket
- input: a .txt file of Zendesk URLs, separated by newlines
- output: a .csv file of ticket URLs + subject


## Known Limitation(s)

- **3/17/2022**: ``user-emails.py`` script is slow compared to the original script
    This appears to be a limitation of the Zendesk API. The ticket URL is stored in a different place than the user info, so a second call to the Zendesk API is required, which slows the process. 
    The API returns results as a JSON, and since there are 2 API calls for one ticket, parsing through both JSONs is required, which also adds to the slowness.

- **2/2/2022**: uses Zendesk Export API instead of Search API to get around 1000 limit
    Tested and was able to get over 20,000 results from a query

- **11/10/2021**: only gets 1000 results total. 
    This appears to be the same as when searching zendesk in the browser which caps at 34 pages (ie. 34 * 30 = 1020 results).

- **7/9/2021**: only gets 100 results total. need to implement pagination -> DONE 
    https://developer.zendesk.com/documentation/developer-tools/pagination/paginating-through-lists/

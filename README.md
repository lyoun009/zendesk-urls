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



## Known Limitation(s)

- only gets 100 results total. need to implement pagination -> DONE 
    https://developer.zendesk.com/documentation/developer-tools/pagination/paginating-through-lists/

- EDIT: only gets 1000 results total. 
      This appears to be the same as when searching zendesk in the browser which caps at 34 pages (ie. 34 * 30 = 1020 results).

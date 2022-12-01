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
    
NOTE: Do not include the square brackets. eg. ``keyring.set_password("zendesk", "john.smith@zybooks.edu", "Password123")``



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
- output: a 'links.txt' file of ticket URLs
#### ``user-emails.py``
- gets ticket URLs + requestor email
- input: a Zendesk query
- output: a 'links.csv' file of ticket URLs + requestor email
#### ``subjects.py``
- used for getting the subject (ie. cpp, python3, etc.) of a ticket
- input: a .txt file of Zendesk URLs, separated by newlines
- output: a 'links.csv' file of ticket URLs + subject
#### ``subject_line.py``
- used for getting the subject line of a ticket
- input: a Zendesk query
- output: a 'results.csv' file of ticket subjects


## Known Limitation(s) / Planned features
- **12/1/2022**: TO DO: want to make a menu interface + combine the different scripts into one consolidated script (ie. run the single script -> give options get URLs, get subjects, get emails, or all of the above, etc. -> output based on user's selection.)

- **3/17/2022**: ``user-emails.py`` script is slow compared to the original script
    This appears to be a limitation of the Zendesk API. The ticket URL is stored in a different place than the user info, so a second call to the Zendesk API is required, which slows the process. 
    The API returns results as a JSON, and since there are 2 API calls for one ticket, parsing through both JSONs is required, which also adds to the slowness.

- **2/2/2022**: uses Zendesk Export API instead of Search API to get around 1000 limit
    Tested and was able to get over 20,000 results from a query

- **11/10/2021**: only gets 1000 results total. 
    This appears to be the same as when searching zendesk in the browser which caps at 34 pages (ie. 34 * 30 = 1020 results).

- **7/9/2021**: only gets 100 results total. need to implement pagination -> DONE 
    https://developer.zendesk.com/documentation/developer-tools/pagination/paginating-through-lists/

## Token Authentication
For users that don't have a Zendesk password, or for users that user 2FA, please follow these instructions.

### Generate a token on Zendesk Admin
- Name the token something identifiable, such as "John's token", so we can idenify it in the future.
- Don't press save or close since the token will be hidden permanently once you leave the page.

### Test the token in the terminal  
Use this curl command to test your token. (Remember do NOT include the square brackets.)
```
curl https://zybooks.zendesk.com/api/v2/users.json \
  -u [user email]/token:[token here]
```


Run the curl command. You should see a JSON file being outputted to the terminal. If not, check that you copied the token correctly.

### Convert the email+token credentials to base64. 
You can do so using this command in the terminal.
    
    echo -n [user email]/token:[your token here] | base64
    
The echo command should return some long alpha-numeric string. **You will need this later**.

### Update the .py script to account for token authentication
In VS code (or code editor of choice), modify the line of code that sets the password in Keyring:

    # keyring.set_password("zendesk", "[your_zendesk_email]", "[your_zendesk_password]")

Change it to:

    keyring.set_password("zendesk", "token", "[that alpha-numeric base64 string from the previous step]")


Under ``params``, add a line of code to call the token you set in Keyring:

    my_headers={'Authorization': 'Basic '+keyring.get_password("zendesk", "token")}

Change the ``response`` to call ``my_headers``. Do this by changing this line:

    response = session.get(url)

to this:

    response = session.get(url, headers=my_headers)

There should be **2 instances** of this line. One right before the ``if response.status_code != 200:`` block and the other in the ``while`` loop.

You can also delete/comment out the lines of code:
``# credentials = '[your_zendesk_email]', keyring.get_password("zendesk", "[your_zendesk_email]")`` and ``session.auth = credentials`` since we won't be using traditional credentials to authenticate anymore.

### Run the .py script
Now, run the .py script once. This is just to set the token in Keyring.

Then, delete the line where you wrote the credentials:

        keyring.set_password("zendesk", "token", "[that alpha-numeric base64 string from the previous step]")










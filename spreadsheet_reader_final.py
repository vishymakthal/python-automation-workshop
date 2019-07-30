from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import Mailer
import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SHEET_ID = '1ovzYvlZcneaMAMydn53AMqqYg792O-STm2_SUkgtYwU'

store = file.Storage('sheets_token.json')
creds = store.get()


if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range='A2:H').execute()

review_items_sheet = result['values']

print(review_items_sheet)

# 1. Create empty due item list
items_due = []

# 2. Grab the current date in MM/DD format
current_date = '{}/{}'.format(datetime.datetime.now().month,datetime.datetime.now().day)

# 3. Create for loop
for item in review_items_sheet:

    # 4. Check if the item is due for review Today
    if current_date in item:

        # 5. Construct a review item string and append to the items list
        item_str = ' - '.join(item[0:3])
        items_due.append(item_str)

# 6. Call Mailer and send out items due
Mailer.send_reminder_email(items_due)

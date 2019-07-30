from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://mail.google.com/']

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

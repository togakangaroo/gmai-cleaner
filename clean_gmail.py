# [[file:README.org::*Final script][Final script:1]]
import time
import re
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import buildhttps://github.com/togakangaroo/gmai-cleaner

credentials = Credentials.from_authorized_user_file('./.credentials/gmauer-credentials.json')
service = build('gmail', 'v1', credentials=credentials)

def messages_to_spam():
   today = datetime.today()
   search_window = today - timedelta(days=2)
   query = f'after:{search_window.strftime("%Y-%m-%d")} in:inbox'
   response = service.users().messages().list(userId='me', q=query).execute()

   for message in response.get('messages', []):
      message_data = service.users().messages().get(userId='me', id=message['id']).execute()
      if any((1 for h in message_data.get('payload', {}).get('headers', [])
            if h['name'] in ('To', 'CC') \
              and re.search(r'\bGrace\w*@', h['value'], re.IGNORECASE ) )) \
              and not message_data.get('payload', {}).get('body', {}).get('size', 0):
         yield message_data

start_time = time.time()

modification = {'removeLabelIds': ['INBOX'], 'addLabelIds': ['SPAM']}
for message_data in messages_to_spam():
    print(f'Modifying message {message_data["id"]}')
    service.users().messages().modify(userId='me', id=message_data['id'], body=modification).execute()

print(f'Done in {time.time() - start_time}')
# Final script:1 ends here

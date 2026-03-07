from pygrister.api import GristApi
from dotenv import load_dotenv

load_dotenv()
grist = GristApi()
status_code, response = grist.list_records('BoxBot_Entries')
entries = [entry['A'] for entry in response]
print(entries)
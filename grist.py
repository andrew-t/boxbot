from pygrister.api import GristApi
from dotenv import load_dotenv

from fonts import text_fits_on_screen

load_dotenv()
grist = GristApi()
status_code, response = grist.list_records('BoxBot_Entries')
entries = [entry['A'] for entry in response]

for entry in entries:
	print(entry)
	if not text_fits_on_screen(entry):
		print(" -- This entry does does not fit on the screen")

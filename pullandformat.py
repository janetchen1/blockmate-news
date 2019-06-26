import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

from yattag import Doc

def GetSheet(sheet_name):
	# authenticate to Google sheets
	scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('sheets_secret.json', scope)
	client = gspread.authorize(creds)

	# get all records in sheet
	sheet = client.open(sheet_name).sheet1

	return sheet

def GetNewMessages(sheet):
	all_rows = sheet.get_all_records()

	return all_rows

def MessagesToHTML(rows):
	# format rows into rich text email
	doc, tag, text = Doc().tagtext()
	with tag('html'):
		with tag('h1', ('align', 'center')):
			text('Blockmate Newsletter!')
		with tag('body', ('align', 'center')):
			for row in rows:
				# submitter's name and date
				with tag('h3', id = row['name']):
					with tag('font', ('color', row['color'].lower())):
						date = row['timestamp'].split(' ', 1)[0]
						text(row['name'] + ' on ' + date)
				# submitter's message
				with tag('p', id=row['name']):
					with tag('font', ('color', row['color'].lower())):
						text(row['msg'])
						doc.attr(style = "color:" + row['color'].lower() + ';"')
				# submitter's photos
				photo_urls = [x.strip() for x in row['photos'].split(',')]
				for photo in photo_urls:
					# use uc?export format instead of open
					url = photo.replace('open?','uc?export=view&',1)
					with tag('div', id='photo-container'):
						doc.stag('img', src=url, width=300)
	return(doc.getvalue())

def ClearOldMessages(sheet_name):
	sheet = GetSheet(sheet_name)
	rows = GetNewMessages(sheet)
	num_rows = len(rows)
	# delete rows starting from bottom
	for i in range(num_rows + 1,1,-1):
		sheet.delete_row(i)

	# use to check that all rows deleted
	new_rows = GetNewMessages(sheet)
	new_num = len(new_rows)
	return new_num

def CheckSubmitters(sheet_name, submitter_dict):
	sheet = GetSheet(sheet_name)
	rows = GetNewMessages(sheet)

	# fill in submitters dict with 1 if person has submitted
	for row in rows:
		submitter = row['name']
		if submitter_dict[submitter] == 0:
			submitter_dict[submitter] = 1

	# create list of submitters
	submitted_list = []
	for s in submitter_dict.keys():
		if submitter_dict[s] == 1:
			submitted_list.append(s)

	return submitted_list











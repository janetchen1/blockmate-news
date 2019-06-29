import pprint
from yattag import Doc
import sheet_utils


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
	sheet = sheet_utils.GetSheet(sheet_name)
	rows = sheet_utils.GetRows(sheet)
	num_rows = len(rows)
	# delete rows starting from bottom
	for i in range(num_rows + 1,1,-1):
		sheet.delete_row(i)

	# use to check that all rows deleted
	new_rows = sheet_utils.GetRows(sheet)
	new_num = len(new_rows)
	return new_num

def CheckSubmitters(sheet_name, submitter_dict):
	sheet = sheet_utils.GetSheet(sheet_name)
	rows = sheet_utils.GetRows(sheet)

	# fill in submitters dict with 1 if person has submitted
	for row in rows:
		submitter = row['name']
		if submitter_dict[submitter]['count'] == 0:
			submitter_dict[submitter]['count'] = 1

	# create list of submitters
	submitted_list = []
	for s in submitter_dict.keys():
		if submitter_dict[s]['count'] == 1:
			submitted_list.append(s)

	return submitted_list











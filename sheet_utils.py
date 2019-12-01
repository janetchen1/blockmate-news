import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sheets_secret_creator as ssc

def GetSheet(sheet_name):
	# authenticate to Google sheets
	scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
	ssc.writeSheetsSecrets()
	creds = ServiceAccountCredentials.from_json_keyfile_name('sheets_secret.json', scope)
	ssc.clearSheetsSecrets()
	client = gspread.authorize(creds)

	# get all records in sheet
	sheet = client.open(sheet_name).sheet1

	return sheet

def GetRows(sheet):
	all_rows = sheet.get_all_records()

	return all_rows
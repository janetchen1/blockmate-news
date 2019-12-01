import os
import json


def writeSheetsSecret():
	with open('sheets_secret_dynamic.json', 'w') as outfile:
	    json.dump({
	    "type":"service_account",
	    "project_id": os.getenv('SHEETS_PROJECT_ID',None),
	  	"private_key_id": os.getenv('SHEETS_PRIVATE_KEY_ID',None),
	  	"private_key": os.getenv('SHEETS_PRIVATE_KEY',None)
	  	"client_email": os.getenv('SHEETS_CLIENT_EMAIL',None),
	  	"client_id": os.getenv('SHEETS_CLIENT_ID',None),
	  	"auth_uri": "https://accounts.google.com/o/oauth2/auth",
	  	"token_uri": "https://oauth2.googleapis.com/token",
	  	"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
	  	"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/submissions%40blockmate-newsle-1561390342869.iam.gserviceaccount.com"
	    }, outfile)

def clearSheetsSecret():
	open("sheets_secret_dynamic.json", "w").close()



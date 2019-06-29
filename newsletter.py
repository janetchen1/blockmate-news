from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors

from httplib2 import Http
from oauth2client import file, client, tools
from base64 import urlsafe_b64encode

import config
import quickstart_mail
import message
import submission_management as sm
import sheet_utils
import groups


def IsNewsletterReady(submissions_sheet, submitter_directory):
	submitters_list = sm.CheckSubmitters(submissions_sheet, submitter_directory)
	if len(submitters_list) == len(submitter_directory.keys()):
		return True
	else:
		# if not ready, check how many submitters missing
		missing = list(set(submitter_directory.keys()) - set(submitters_list))
		if len(missing) == 0:
			return True
		elif len(missing) == 1:
			# initialize service
			mail_creds = None
			if not os.path.exists('mail_token.pickle'):
			  quickstart.main()
			with open('mail_token.pickle', 'rb') as mail_token:
			  mail_creds = pickle.load(mail_token)
			  service_mail = build('gmail', 'v1', credentials=mail_creds)
			  
			# email the missing person
			address = submitter_directory[missing[0]]['email']
			missingSubmission = message.CreateMessage(config.SENDER,address,'Submit to the Blockmate Newsletter!', 'submit')
			missingSend = message.SendMessage(service_mail, 'me', missingSubmission)
			return False


def MakeNewsletter(submissions_sheet, group, test):
	# initialize service
	mail_creds = None
	if not os.path.exists('mail_token.pickle'):
	  quickstart.main()
	with open('mail_token.pickle', 'rb') as mail_token:
	  mail_creds = pickle.load(mail_token)
	  service_mail = build('gmail', 'v1', credentials=mail_creds)

	# get new submissions, format them, and send newsletter via email
	sheet = sheet_utils.GetSheet(submissions_sheet)
	messages = sheet_utils.GetRows(sheet)
	email_body = sm.MessagesToHTML(messages)
	
	# generate recipient list
	recipient_list = []
	for name in group['submitter_directory'].keys():
		recipient_list.append(group['submitter_directory'][name]['email'])
	recipient_string = ', '.join(recipient_list)
	if test:
		recipient_string = config.TEST_RECIPIENT
	newsletterMessage = message.CreateMessage(config.SENDER,recipient_string, config.SUBJECT, email_body)
	newsletterSend = message.SendMessage(service_mail, 'me', newsletterMessage)

	# cleanup: if send successful, clear submissions spreadsheet
	if 'SENT' in newsletterSend['labelIds']:
		# clear submissions spreadsheet
		clr = sm.ClearOldMessages(submissions_sheet)
		if clr != 0:
			# if not all entries deleted, notify admin
			admin = group['admin_email']
			notClearedError = message.CreateMessage(config.SENDER,admin, 'Submissions not cleared', '')
			errorSend = message.SendMessage(service_mail, 'me', notClearedError)
	else:
		# if email failed to send, attempt to notify admin
		notSentError = message.CreateMessage(config.SENDER,config.ADMIN, 'Newsletter not sent', '')
		errorSend = message.SendMessage(service_mail, 'me', notSentError)

	return

def main():
	group_directory = groups.MakeGroupDict(config.GROUPS_SPREADSHEET, config.USERS_SPREADSHEET)
	for group in group_directory.keys():
		submission_sheet = group_directory[group]['sp_name']
		submitter_directory = group_directory[group]['submitter_directory']
		ready = IsNewsletterReady(submission_sheet, submitter_directory)
		if ready:
			MakeNewsletter(submission_sheet, group_directory[group], True)

main()

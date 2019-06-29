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


def IsNewsletterReady():
	submitters = sm.CheckSubmitters(config.SHEET_NAME, config.SUBMITTER_DIRECTORY)
	if len(submitters) == len(config.SUBMITTER_DIRECTORY.keys()):
		return True
	else:
		# if not ready, check how many submitters missing
		missing = list(set(config.SUBMITTER_LIST) - set(config.submitters))
		if len(missing) == 0:
			return True
		elif len(missing) == 1:
			# email the missing person
			address = config.SUBMITTER_EMAILS[missing[0]]
			missingSubmission = message.CreateMessage(config.SENDER,address,'Submit to the Blockmate Newsletter!', 'submit')
			missingSend = message.SendMessage(service_mail, 'me', missingSubmission)
			return False


def MakeNewsletter():
	# initialize service
	mail_creds = None
	if not os.path.exists('mail_token.pickle'):
	  quickstart.main()
	with open('mail_token.pickle', 'rb') as mail_token:
	  mail_creds = pickle.load(mail_token)
	  service_mail = build('gmail', 'v1', credentials=mail_creds)

	# get new submissions, format them, and send newsletter via email
	sheet = sheet_utils.GetSheet(config.SHEET_NAME)
	messages = sheet_utils.GetRows(sheet)
	email_body = sm.MessagesToHTML(messages)
	newsletterMessage = message.CreateMessage(config.SENDER,config.RECIPIENT, config.SUBJECT, email_body)
	newsletterSend = message.SendMessage(service_mail, 'me', newsletterMessage)

	# cleanup: if send successful, clear submissions spreadsheet
	if 'SENT' in newsletterSend['labelIds']:
		# clear submissions spreadsheet
		clr = sm.ClearOldMessages(config.SHEET_NAME)
		if clr != 0:
			# if not all entries deleted, notify admin
			notClearedError = message.CreateMessage(config.SENDER,config.ADMIN, 'Submissions not cleared', '')
			errorSend = message.SendMessage(service_mail, 'me', notClearedError)
	else:
		# if email failed to send, attempt to notify admin
		notSentError = message.CreateMessage(config.SENDER,config.ADMIN, 'Newsletter not sent', '')
		errorSend = message.SendMessage(service_mail, 'me', notSentError)

	return


MakeNewsletter()
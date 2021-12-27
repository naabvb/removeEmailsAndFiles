#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Service that removes files and correspoding emails

import os
import pickle
import json
import ast
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://mail.google.com/']
BASE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/'


def main():

    alreadyRead = []
    if os.path.exists(BASE_PATH + 'alreadyRead.json'):
        with open(BASE_PATH + 'alreadyRead.json', 'r') as json_file:
            alreadyRead = json.load(json_file)
            if type(alreadyRead) is not list:
                try:
                    alreadyRead = ast.literal_eval(alreadyRead)
                except:
                    print("Type translation failed")

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(BASE_PATH + 'token.pickle'):
        with open(BASE_PATH + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                BASE_PATH + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(BASE_PATH + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)

    downloaded_images = os.listdir(BASE_PATH + 'images')

    trash_images = os.listdir(BASE_PATH + 'trash')

    for image in trash_images:
        if image in downloaded_images:
            if (os.path.exists(BASE_PATH + 'images/' + image)):
                email_Id = image.split('_')[0]
                try:
                    service.users().messages().delete(userId='me', id=email_Id).execute()
                    alreadyRead.remove(email_Id)
                    print("Deleted " + email_Id)
                except errors.HttpError as error:
                    print(error)
                os.remove(BASE_PATH + 'images/' + image)
    with open(BASE_PATH + 'alreadyRead.json', 'w') as output:
        json.dump(alreadyRead, output)


if __name__ == '__main__':
    main()

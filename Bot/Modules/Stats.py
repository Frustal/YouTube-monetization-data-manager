# -*- coding: utf-8 -*-

import sys
import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/yt-analytics-monetary.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = os.path.join(sys.path[0], "Modules/Creds/StatsCreds.json")

  

def GetVideoMetrics(videoList, startDate, endDate, channel_name):
    TOKEN_NAME = os.path.join(sys.path[0], "Tokens/" + channel_name + '.json')
  
    def get_service():
      creds = None
      if os.path.exists(TOKEN_NAME):
        creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
      if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
          creds = flow.run_console()
        with open(TOKEN_NAME, 'w') as token:
          token.write(creds.to_json())   
          
      with open("rest.json") as f:
        service = json.load(f)
      return discovery.build_from_document(service, credentials = creds)

    def execute_api_request(client_library_function, **kwargs):
      response = client_library_function(
        **kwargs
      ).execute()
      return response['rows']
      
    print("Connecting to Youtube data")
    youtubeAnalytics = get_service()
    print("Done")

    print("Getting video stats")
    executed = execute_api_request(
      youtubeAnalytics.reports().query,
      ids='channel==MINE',
      startDate=f'{startDate}', #2021-11-18
      endDate=f'{endDate}',
      metrics='estimatedRevenue,cpm,views,adImpressions',
      dimensions='video', 
      filters=f'video=={videoList}'
  ) 
    print("Done")
    return executed
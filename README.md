# BIS_googledive_app
App to create and manage google drive nested client directories for Buyer Invested Selling

Requirements:
python 3.10 or later
google-api-python-client 
google-auth-httplib2 
google-auth-oauthlib

setup:
create and enable a new google API service via your account on google cloud. 
create OAuth credentials for app and download credentials to project folder as 'credentials.json'

run:
python create_BIS_project.py
enter name of client when prompted

note:
when running for the first time, a brower window will open asking you to select a google account and authorize access to google drive. 
If at any point you change the SCOPES of the permissions for the app to the google drive account, delete the 'token.json' file and rerun

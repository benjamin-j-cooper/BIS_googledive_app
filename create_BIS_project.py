import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/drive.metadata', 'https://www.googleapis.com/auth/drive']

target_folder_id = '1jLEX1BduFS9Jn_2nmHYD31Qq-7iMSMdp'

def create_folder(parent_folder_id, folder_name, service):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder['id']


def create_nested_folders(parent_folder_id, folder_names, service):
    nested_folder_ids = []

    for folder_name in folder_names:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        nested_folder_ids.append(folder['id'])

    return nested_folder_ids


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(pageSize=1, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        if items:
            print("Connection Successfull!")

            client_name = input('Enter the name of the new client to create a google drive course folder for: ')
            folder_id = create_folder(target_folder_id, client_name, service)

            print(f'Successfully created folder "{client_name}" with ID {folder_id}.')

            nested_folder_names = ['BAM_Portal', 'ADMIN']
            nested_folder_ids = create_nested_folders(folder_id, nested_folder_names, service)
            
            for folder_name, nested_folder_id in zip(nested_folder_names, nested_folder_ids):

                if folder_name in 'BAM_Portal':

                    nested_folder_names = ['1-Course Materials','2-Recommended Readings','3-Frameworks','4-Storytelling','5-Playbook','6-Intelligence Questions','7-Email Archive']
                    nested_folder_ids = create_nested_folders(nested_folder_id, nested_folder_names, service)
                    
                elif folder_name in 'ADMIN':

                    nested_folder_names = ['Course Materials',"Readings",'Frameworks','Storytelling','Playbook','Intelligence Questions','Email Archive']
                    nested_folder_ids = create_nested_folders(nested_folder_id, nested_folder_names, service)

                print(f'Successfully created folder "{folder_name}" with ID {nested_folder_id} and subfolders.')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()    

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/drive.metadata', 'https://www.googleapis.com/auth/drive']

# change the target folder ID to the parent folder you want to work in
# target_folder_id = '1jLEX1BduFS9Jn_2nmHYD31Qq-7iMSMdp'
target_folder_id = '18k8B9KzTMebdV-Nc3JGQiRsD6FUfUIMb'
# folders where static files are stored
templates = '1VA1v5riOhl76TXfl0Mcsmzc2bCQmjfdG'
artifacts = '1MqXp_2TZAA_Daeb6oqIfZgEj62X1GEav'

def create_folder(parent_folder_id, folder_name, service):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
        
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder['id']


def create_nested_folders(parent_folder_id, folder_names, service,folder_color_rgb):
    nested_folder_ids = []

    for folder_name in folder_names:
        # Retrieve the color for the current folder_name from the mapping
        color = folder_color_rgb.get(folder_name, '#000000')  # Default to black if not found
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id],
            'folderColorRgb': color
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

            bam_portal_name = client_name + ' BAM Portal'
            nested_folder_names = [bam_portal_name, 'BIS ADMIN']
            base_colors = {
                'BIS ADMIN':"#d06b64",
                bam_portal_name:"#9a9cff"
            }

            nested_folder_ids = create_nested_folders(folder_id, nested_folder_names, service, base_colors)
            
            # make color mapping dict for main level nested folders
            colorPalette = {
                'Glossary':"#fa573c",
                'Course Materials':"#ff7537",
                # "#ffad46",
                'Prospect Profiles':"#fad165",
                # "#7bd148",
                'Five Chords':"#16a765",
                'Tools':"#92e1c0",
                'Sales Playbook':"#9a9cff",
                # "#9fc6e7",
                'Conferences and Events':"#cd74e6",
                'Weekly Email Archive':"#8f8f8f"
                }
            for folder_name, nested_folder_id in zip(nested_folder_names, nested_folder_ids):

                if folder_name in bam_portal_name:

                    nested_folder_names = ['Glossary','Course Materials','Prospect Profiles','Five Chords','Tools','Sales Playbook','Conferences and Events', 'Weekly Email Archive']
                    nested_folder_ids = create_nested_folders(nested_folder_id, nested_folder_names, service,colorPalette)

                    for folder_name, nested_folder_id in zip(nested_folder_names, nested_folder_ids):
                        if folder_name in 'Tools':

                            tools_folder_names = ['Frameworks','Articles','Intelligence Questions','Storytelling','Video Links']
                            tool_colors = {
                                'Frameworks':"#92e1c0",
                                'Articles':"#92e1c0",
                                'Intelligence Questions':"#92e1c0",
                                'Storytelling':"#92e1c0",
                                'Video Links':"#92e1c0"
                            }
                            nested_folder_ids = create_nested_folders(nested_folder_id, tools_folder_names, service, tool_colors)
                            # for name in tools_folder_names:
                            #     folder_id = create_folder(nested_folder_id, name, service)

                elif folder_name in 'BIS ADMIN':

                    nested_folder_names = ['Glossary','Course Materials','Prospect Profiles','Five Chords','Tools','Sales Playbook','Conferences and Events', 'Weekly Email Archive']
                    nested_folder_ids = create_nested_folders(nested_folder_id, nested_folder_names, service,colorPalette)

                    for folder_name, nested_folder_id in zip(nested_folder_names, nested_folder_ids):
                        if folder_name in 'Tools':

                            tools_folder_names = ['Frameworks','Articles','Intelligence Questions','Storytelling','Video Links']
                            tool_colors = {
                                'Frameworks':"#92e1c0",
                                'Articles':"#92e1c0",
                                'Intelligence Questions':"#92e1c0",
                                'Storytelling':"#92e1c0",
                                'Video Links':"#92e1c0"
                            }
                            nested_folder_ids = create_nested_folders(nested_folder_id, tools_folder_names, service, tool_colors)
                            # for name in tools_folder_names:
                            #     folder_id = create_folder(nested_folder_id, name, service)

                print(f'Successfully created folder "{folder_name}" with ID {nested_folder_id} and subfolders.')

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()    

### Possible google drive colors:
#   "Chocolate ice cream":"#ac725e",
#   "Old brick red":"#d06b64",
#   "Cardinal":"#f83a22",
#   "Wild straberries":"#fa573c",
#   "Mars orange":"#ff7537",
#   "Yellow cab":"#ffad46",
#   "Spearmint":"#42d692",
#   "Vern fern":"#16a765",
#   "Asparagus":"#7bd148",
#   "Slime green":"#b3dc6c",
#   "Desert sand":"#fbe983",
#   "Macaroni":"#fad165",
#   "Sea foam":"#92e1c0",
#   "Pool":"#9fe1e7",
#   "Denim":"#9fc6e7",
#   "Rainy sky":"#4986e7",
#   "Blue velvet":"#9a9cff",
#   "Purple dino":"#b99aff",
#   "Mouse":"#8f8f8f",
#   "Mountain grey":"#cabdbf",
#   "Earthworm":"#cca6ac",
#   "Bubble gum":"#f691b2",
#   "Purple rain":"#cd74e6",
#   "Toy eggplant":"#a47ae2"
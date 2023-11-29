import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/drive.metadata', 'https://www.googleapis.com/auth/drive']

target_folder_id = '1jLEX1BduFS9Jn_2nmHYD31Qq-7iMSMdp'

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

def create_folder(parent_folder_id, folder_name, folder_color_rgb, service):
    folder_color_rgb="#cd74e6"
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id],
        # 'folderColorRgb': folder_color_rgb
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    return folder['id']

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

            defualt_color = {
                # '#434343'
                "#ac725e"
            }
            client_name = input('Enter the name of the new client to create a google drive course folder for: ')
            client_folder_id = create_folder(target_folder_id, client_name, defualt_color, service)

            print(f'Successfully created folder "{client_name}" with ID {client_folder_id}.')

            bam_portal_name = client_name + '_BAM_Portal'
            root_folder_names = [bam_portal_name, 'BIS_ADMIN']
            base_colors = {
                "#d06b64",
                "#9a9cff"
            }
            nested_folder_names = ['1-Course Materials','2-Recommended Readings','3-Frameworks','4-Storytelling','5-Playbook','6-Intelligence Questions','7-Email Archive']
            colorPalette = {
            "#fa573c",
            "#ff7537",
            "#ffad46",
            "#7bd148",
            "#92e1c0",
            "#9a9cff",
            "#cd74e6"
            }
            # Create the nested folders under the specified parent folder with different colors
            for folder_name, color in zip(root_folder_names, base_colors):
                folder_id = create_folder(client_folder_id, folder_name, color, service)
                print(f'Successfully created folder "{folder_name}" with ID {folder_id} and color {color}.')

                if folder_name in bam_portal_name:

                    # Create the nested folders under the specified parent folder with different colors
                    for folder_name, color in zip(nested_folder_names, colorPalette):
                        folder_id = create_folder(folder_id, folder_name, color, service)
                    
                elif folder_name in 'BIS_ADMIN':

                    # Create the nested folders under the specified parent folder with different colors
                    for folder_name, color in zip(nested_folder_names, colorPalette):
                        folder_id = create_folder(folder_id, folder_name, color, service)

        print(f'Successfully created project for {client_name}.')
            
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()    

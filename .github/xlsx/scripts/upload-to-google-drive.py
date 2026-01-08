from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import sys

if len(sys.argv) < 2:
    print ('usage: upload-to-google-drive.py <drive-file-id> <version>')
    print ('drive-file-id is the id of the file to update, version is optional')
    exit(1)

def set_version():
    return f"-{str(sys.argv[2])}" if (len( sys.argv ) > 2) else ""

def set_file_id():
    return str(sys.argv[1]) if (len( sys.argv ) > 1) else ""

def set_sheet_title(version):
   return "WSTG-Checklist{version}.xlsx".replace('{version}', version)

# The authentication
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# Set Version
version = set_version()
# Set Title
title = set_sheet_title(version)
#
id = set_file_id()

# Upload file
upload_file_path = 'checklists/checklist.xlsx'
f = drive.CreateFile({'id': id})
f.SetContentFile(upload_file_path)
f.Upload()

# Update title
a=drive.auth.service.files().get(fileId=id).execute()
a['title']= title
update=drive.auth.service.files().update(fileId=id,body=a).execute()

# Insert the permission.
permission = f.InsertPermission({'type': 'anyone', 'value': 'anyone','role': 'reader'})


# Empty the variable used to upload the files to Google Drive
# If the file stays open in memory and causes a memory leak
# therefore preventing its deletion
f = None
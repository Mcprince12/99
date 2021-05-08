import sys
import dropbox

from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


TOKEN = input("Access token goes here")

LOCALFILE = input("Put local file path here")

BACKUPPATH = input("Back up path goes here")


def backup():
    with open(LOCALFILE, 'rb') as f:

        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:

            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()


def checkFileDetails():
    print("Checking file details")

    for entry in dbx.files_list_folder('').entries:
        print("File list is : ")
        print(entry.name)


if __name__ == '__main__':

    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token.")

    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(TOKEN)

    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit(
            "ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    try:
        checkFileDetails()
    except Error as err:
        sys.exit("Error while checking file details")

    print("Creating backup...")

    backup()

    print("Done!")

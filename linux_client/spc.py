import os
import requests
import argparse
import csv
import getpass
from spc_functions import current_user,login,logout,upload_file,display_filelist,delete_file,change_encryption_scheme,download_file
from spc_functions import sync_file_from_client,sync_file_from_server,sync_dir_from_client,sync_dir_from_server,sync_delete_from_client,sync_delete_from_server
from spc_functions import change_sync_status


def  Main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--login',action='store',nargs=2)
    parser.add_argument('--logout',type=str,action='store',nargs=2)
    parser.add_argument('--remove_account',type=str,action='store')
    
    parser.add_argument('-u','--upload',type=str,action='store',nargs=2)
    parser.add_argument('-d','--download',type=str,action='store',nargs=2)
    parser.add_argument('-l','--list',action='store_true')
    parser.add_argument('--delete',type=str,action='store',nargs=2)
    parser.add_argument('--encdec',type=str,action='store',nargs=3)
    parser.add_argument('-sfc','--sync_from_client',type=str,nargs=2)
    parser.add_argument('-sfs','--sync_from_server',type=str,nargs=2)

    # parser.add_argument('--server',type=str,nargs=0)
    # parser.add_argument('--status',type=str,nargs=0)
    parser.add_argument('-v','--version',type=str,action='store',nargs=1)
    parser.add_argument('--help_section',action='store',nargs=1)

    args=parser.parse_args()


# LOGIN :
    if (args.login):
        file_exists1=os.path.isfile(os.getenv('HOME')+'/current_user.txt')
        if not file_exists1:
            os.system('touch '+os.getenv('HOME')+'/current_user.txt')
        file_exists2=os.path.isfile(os.getenv('HOME')+'/token.txt')
        if not file_exists2:
            os.system('touch '+os.getenv('HOME')+'/token.txt')
        if (current_user() != ''):
            response=input('Another user is already logged in from this device. Do you want to proceed? [Y/N]')
            if (response == 'Y' or response == 'y'):
                logout(current_user())
                login(args.login[0])
            else :
                print('Process aborted by user.')
        else :
            login(args.login[0])

               
# LOGOUT :
    if(args.logout):
        user=args.logout[0]
        logout(user)


# VERSION :
    if (args.version):
        print('BETA_VERSION 1.0.0.1')


# REMOVE ACCOUNT :
    if (args.remove_account):
        username=str(input('Username : '))
        response=input('Are you sure you wish to delete your account? [Y/N]')
        if (response == 'y' or response == 'Y'):
            with open('loginData.csv','r') as csvfile:
                reader=csv.DictReader(csvfile)
                for row in reader :
                    if (row['username'] == username and row['saved'] == yes):
                        response1=print('Do you wish to use the saved password? [Y/N]')
                        if (response1 == 'y' or response1 == 'Y'):
                            delete_account(username,row[password])
                        else :
                            password=getpass.getpass(prompt='Password : ',stream=None)
                            if (password == check_password(username)):
                                delete_account(username,password)
                            else :
                                print('Password incorrect.')
        else :
            print('Process aborted by user.')
# Make a suggestion form sort of thing when the user deletes the account


 # UPLOAD :
    if (args.upload):
        # change_sync_status('0')
        relfilepath=os.path.relpath(args.upload[0],os.getenv('HOME'))
        filepath=os.getenv('HOME')+'/'+relfilepath
        if (os.path.exists(filepath)):
            upload_file(filepath)
        else :
            print('No such file exists :')
            print(filepath)
        # change_sync_status('1')


# LIST OF UPLOADED FILES :
    if (args.list):
        display_filelist()


# DELETE FILE
    if (args.delete):
        filename=args.delete[0]
        delete_file(filename)


# ENCRYPTION DECRYPTION:
    if (args.encdec):
        command=args.encdec[0]
        change_encryption_scheme(command)


# DOWNLOAD :
    if (args.download):
        filepath=args.download[0]
        file_exists=os.path.isfile(filepath)
        if not file_exists:
            response1=download_file(filepath)
            if (response1 == 1):
                print('Download successful.')
            elif (response1 == 2):
                os.system('rm -f '+filepath)
                print('Error while downloading. Try again.')
        else:
            response=input('File already exists. Do you wish to overwrite it? [Y/N]')
            if (response == 'Y' or response =='y'):
                os.system('rm -f '+filepath)
                response1=download_file(filepath)
                if (response1 == 1):
                    print('Download successful. File overwritten.')
                elif (response1 == 2):
                    os.system('rm -f '+filepath)
                    print('Error while overwriting. Try again.')
            elif (response == 'N' or response == 'n'):
                print('Process aborted by user.')


# SYNC FROM CLIENT TO SERVER :
    if (args.sync_from_client):
        dirpath=args.sync_from_client[0]
        dir_exists=os.path.isdir(dirpath)
        file_exists=os.path.isfile(dirpath)
        if file_exists:
            sync_file_from_client(dirpath)
        elif dir_exists:
            sync_delete_from_server(dirpath)
            sync_dir_from_client(dirpath)
        else :
            print('No such file or directory exists :')
            print(dirpath)           


# SYNC FROM SERVER TO CLIENT :
    if (args.sync_from_server):
        dirpath=args.sync_from_server[0]
        dir_exists=os.path.isdir(dirpath)
        file_exists=os.path.isfile(dirpath)
        if file_exists:
            sync_file_from_server(dirpath)
        elif dir_exists:
            sync_delete_from_client(dirpath)
            sync_dir_from_server(dirpath)
        else :
            print('No such file or directory exists :')
            print(dirpath)     

# HELP
    if (args.help_section):
        print('Help section:')
        print('1. --login username: login with the given username')
        print('2. --logout username: logout user with the given username')
        print('3. --upload filepath: upload file from the given filepath to the server')
        print('4. --download filepath: download given file from the server which corresponds to the given filepath')
        print('5. --delete filepath: delete file from the server which corresponds to the given filepath')
        print('6. --list: list out all the files uploaded by the currently logged in user')
        print('7. --sync_from_client directory: sync the given directory from client to the server')
        print('8. --sync_from_server directory: sync the given directory from server to the client')
        print('9. --version: print the current version of spc')
        print('10. --help_section: display the help section')


if __name__=='__main__':
    Main()

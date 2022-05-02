import os
import csv
import getpass
import json
from pathlib import Path
import pickle
import re
import requests
from tempfile import NamedTemporaryFile
import shutil

# Functions available in the file :
# check_password
# check_return_password
# current_user
# change_current_user
# get_token
# change_token
# file_name
# mdsum
# get_scheme
# change_scheme
# get_decryption_key
# file_type
# create_login_csv
# login
# login_user
# save
# req_send
# logout
# upload_file
# upload_file_info
# upload_file_content
# display_filelist
# delete_file
# change_encryption_scheme
# download_file
# sync_file_from_client
# sync_file_from_server
# sync_dir_from_client
# sync_delete_from_server
# sync_dir_from_server
# sync_delete_from_client



def check_password(user):
    with open(os.getenv('HOME')+'/loginData.csv','r') as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            if(row['username'] == user):
                return row['password']
    return ''


def check_return_password(user):
    with open(os.getenv('HOME')+'/loginData.csv','r') as csvfile :
        reader=csv.DictReader(csvfile)
        for row in reader :
            if (row['username'] == user):
                if (row['savepassword'] == 'yes'):
                    return row['password']
                else:
                    print('No password saved.')
                    return ''
    return ''


def check_user(user):
    with open (os.getenv('HOME')+'/loginData.csv','r') as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader :
            if (row['username'] == user):
                return True
        return False


def current_user():
    with open(os.getenv('HOME')+'/current_user.txt','r') as f:
        return f.read()


def change_current_user(user):
    with open(os.getenv('HOME')+'/current_user.txt','w') as f:
        f.write(user)


def get_token():
    with open(os.getenv('HOME')+'/token.txt','r') as f:
        return f.read()


def change_token(token):
    with open(os.getenv('HOME')+'/token.txt','w') as f:
        f.write(token)        


def file_name(filepath):
    return os.popen('basename '+ filepath).read().split('\n')[0]


def mdsum(filepath):
    relfilepath=os.path.relpath(filepath,os.getenv('HOME'))
    homefilepath=os.getenv('HOME')+'/'+relfilepath
    command='md5sum '+homefilepath
    return os.popen(command).read().split()[0]
    


def get_scheme(user):
    with open(os.getenv('HOME')+'/loginData.csv','r') as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            if(row['username'] == user):
                return row['scheme']
    return ''


def change_scheme(user,scheme):
    with open(os.getenv('HOME')+'/loginData.csv','w') as csvfile:
        writer=csv.DictWriter(csvfile)
        for row in writer:
            if(row['username'] == user):
                row['scheme']=scheme


def get_decryption_key(user):
    with open(os.getenv('HOME')+'/loginData.csv','r') as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            if (row['username'] == user):
                return row['decryptionkey']

def change_decryption_key(user):
    key=''
    while (key == ''):
        key=input('Enter encryption key: ')
    with open(os.getenv('HOME')+'/loginData.csv','w') as csvfile:
        writer=csv.DictWriter(csvfile)
        for row in writer:
            if(row['username'] == user):
                row['decryptionkey']=key
    print('Encryption key changed.')


def file_type(filename):
    if(filename.lower().endswith('.pdf')):
        return 'pdf'
    elif(filename.lower().endswith(('.jpg','.png','.jpeg','.gif','.webp','.svg','.ai','.ps'))):
        return 'image'
    elif(filename.lower().endswith(('.flv','.avi','.mkv','.mov','.mp4','.mpg','.mwv','.3pg','.asf','.rm','.swf'))):
        return 'video'
    elif(filename.lower().endswith(('.aif','.cda','.mid','.midi','.mp3','.ogg','.mpa','.wav','.wma','wpl'))):
        return 'audio'
    elif(filename.lower().endswith(('.zip','tar.gz','.7z','.rar','.pkg','.arj','.deb','.rpm'))):
        return 'archieve'
    else:
        return 'document'



def change_sync_status(syncstatus):
    token=get_token()
    data={
        'syncstatus': str(syncstatus)
    }
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization':token
        }
    url='http://10.2.224.70:8000/files/sync/'
    r=requests.post(url,data=data,headers=headers)


def get_sync_status():
    token=get_token()
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization':token
        }
    url='http://10.2.224.70:8000/files/get-sync/'
    r=requests.get(url,headers=headers)
    json_data=json.loads(r.content)
    print(json_data)
    js=json.dumps(json_data[0]['sync_status'])
    return js


def create_login_csv():
    file_exists=os.path.isfile(os.getenv('HOME')+'/loginData.csv')
    if not file_exists:
        with open (os.getenv('HOME')+'/loginData.csv', 'w') as csvfile:
            fieldnames=['username','password','savepassword','scheme','decryptionkey']
            writer=csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=fieldnames)
            writer.writeheader()


def login(user):
    create_login_csv()
    defaultscheme='aes'
    print('Username: '+user)
    if check_user(user):
        login_user(user)
    else:
        response=input('Have you registered? [Y/N]')
        if (response == 'Y' or response == 'y'): 
            print('Encryption schemes available: ')
            print('1. AES')
            print('2. DES')
            n=int(input('To select the scheme,type the corresponding index: '))
            if (n == 1 or n == 2):
                if (n == 1):
                    defaultscheme='aes'
                else:
                    defaultscheme='des'
            save(user,'','no',defaultscheme,'')
            login_user(user)
        elif (response == 'N' or response == 'n'):
            print('To use this service, you need to register at :')
            print('http://10.2.224.70:8000/register/')
        

def login_user(user):
    defaultscheme='aes'
    password=check_return_password(user)
    if(password != ''):
        req_send(user,password)
    else:
        password=str(getpass.getpass(prompt='Password: ', stream=None))    
        if (req_send(user,password) == 200):
            savepassword=input('Do you want to save your password? [Y/N]')
            if(savepassword == 'Y' or savepassword == 'y'):
                save(user,password,'yes',defaultscheme,'')
                print('Password saved successfully.')
            elif (savepassword == 'N' or savepassword == 'n'):
                save(user,'','no',defaultscheme,'')
            else:
                print('Value not recognized. [Y/N]')
        else:
            print('Provided username or password is incorrect.')


def save(user,password,command,scheme,decryptionkey):
    rows=[]
    with open(os.getenv('HOME')+'/loginData.csv','r') as csvfile:
        reader=csv.DictReader(csvfile)
        for row in reader:
            if(row['username'] != user):
                rows.append(row)
    with open(os.getenv('HOME')+'/loginData.csv','w') as csvfile:
        fieldnames=['username','password','savepassword','scheme','decryptionkey']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    with open(os.getenv('HOME')+'/loginData.csv','a') as f_append:
        fieldnames=['username','password','savepassword','scheme','decryptionkey']
        writer=csv.DictWriter(f_append,fieldnames=fieldnames)
        writer.writerow({'username':user,'password':str(password),'savepassword':command,'scheme':scheme, 'decryptionkey':'',})


def req_send(user,password):
    headers={
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
    login_data={
        'username': user,
        'password': password,
        'action':'login'
        }
    with requests.Session() as s:
        url='http://10.2.224.70:8000/files/api-token-auth/'
        r=s.post(url, data=login_data, headers=headers)
        if(r.status_code == 200):
            Token='JWT '+(r.json())['token']
            print('Login successful.')
            change_current_user(user)
            change_token(Token)
        else:
            print('Provided password is incorrect. Try again.')
            save(user,'','no',get_scheme(user),'')
        return r.status_code


def logout(user):
    if (current_user() != ''):
        if (current_user() == user):
            change_current_user('')
            change_token('')    
            print('Logout successful.')
        else:
            print('Provided username is incorrect.')
    else:
        print('No user is logged in.')


def upload_file(filepath):
    relfilepath=os.path.relpath(filepath,os.getenv('HOME'))
    if (os.path.getsize(os.getenv('HOME')+'/'+relfilepath) > 0):
        response=upload_file_info(filepath)
        if (response == 1):
            if upload_file_content(filepath):
                print('File successfully uploaded.')
            else:
                print('Error while encrypting the file.')    
        elif (response == 2):
            if (delete_file(filepath) == 204):
                upload_file(filepath)
        elif (response == 3):
            print('Process aborted by user.')
        elif (response == 4):
            print('Unknown error.')
    else:
        print('File empty.')


def upload_file_info(filepath):
    filename=file_name(filepath)
    filetype=file_type(filename)
    md5sum=mdsum(filepath)
    relfilepath=os.path.relpath(filepath,os.getenv('HOME'))
    token=get_token()
    fileinfo={
        'filename': relfilepath,
        'filetype': filetype,
        'md5sum': md5sum
        }
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization':token
        }
    url2='http://10.2.224.70:8000/files/'+relfilepath+'/'
    r2=requests.get(url2,headers=headers)
    if (r2.status_code == 404):
        url1='http://10.2.224.70:8000/files/create/'
        r1=requests.post(url1,data=fileinfo,headers=headers)
        return 1
    elif (r2.status_code == 200):
        response=input('File already exists. Do you wish to overwrite it? [Y/N]')
        if (response == 'Y' or response =='y'):
            return 2
        elif (response == 'N' or response == 'n'):
            return 3
    else:
        return 4


def upload_file_content(filepath):
    user=current_user()
    scheme=get_scheme(user)
    filename=file_name(filepath)
    relfilepath=os.path.relpath(filepath,os.getenv('HOME'))
    encryptedfilepath=filepath+'.'+scheme
    token=get_token()
    if (scheme == 'aes'):
        os.system('cat '+filepath+' | openssl enc -base64 | openssl aes-256-cbc -a -salt > '+encryptedfilepath)
    elif (scheme == 'des'):
         os.system('cat '+filepath+' | openssl enc -base64 | openssl des-cbc -a -salt > '+encryptedfilepath)
    content=''
    with open(encryptedfilepath,'r') as f:
        content += f.read()
    content.replace('\n','')
    os.system('rm -f '+encryptedfilepath)
    fileinfo={
        'filename': relfilepath,
        'content': content
        }
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization':token
    }
    url='http://10.2.224.70:8000/files/upload/'
    r=requests.post(url,data=fileinfo,headers=headers)
    if(r.status_code == 201):
        return True
    else:
        return False
    # else:
        # command ='openssl genrsa -aes128 -passout pass:'+p+' -out p.pem'
    #     os.popen(command).read()
    #     command='openssl rsa -in p.pem -passin pass:'+p+' -pubout -out p.pub'
    #     os.popen(command).read()
    #     command='openssl rsautl -encrypt -pubin -inkey public.key -in plaintext.txt -out encrypted.txt'


def display_filelist():
    token=get_token()
    headers={
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Authorization':token
        }
    url='http://10.2.224.70:8000/files/'
    r=requests.get(url, headers=headers)
    if r.status_code != 500:
        json_lst=r.json()
        print('{}   {}  {}'.format('Filename','Filetype','Date'))
        for lst in json_lst:
            print('{}   {}  {}'.format(lst['filename'], lst['filetype'], lst['date_upload']))
    else:
        print('No files uploaded or shared.')


def delete_file(filepath):
    relfilepath=os.path.relpath(filepath,os.getenv('HOME'))
    print('File: '+relfilepath)
    token=get_token()
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization':token
    }
    url='http://10.2.224.70:8000/files/'+relfilepath+'/delete/'
    r=requests.delete(url,headers=headers)
    if (r.status_code == 204):
        print('File deleted successfully.')
        return 204
    elif (r.status_code == 404):
        print('No such file exists.')
        return 404
    else:   
        print('Unknown error.')
        return r.status_code


def change_encryption_scheme(command):
    user=current_user()
    last_scheme=get_scheme(user)
    last_key=get_decryption_key(user)
    if (command == 'list'):
        print('Encryption schemes available: ')
        print('1. AES')
        print('2. DES')
    elif (command == 'change_scheme'):
        print('1. AES')
        print('2. DES')
        n=int(input('To change the scheme,type the corresponding number: '))
        if (n == 1 or n == 2):
            password=check_return_password(user)
            if (password == ''):
                password=str(getpass.getpass(prompt='Password: ',stream=None))
            if (password == check_password(user)):
                if (n == 1):
                    change_scheme(user,'aes')
                else:
                    change_scheme(user,'des')
                if (get_scheme(user) != last_scheme):
                    key=change_decryption_key(user)
                else:
                    key=change_decryption_key(user)
            else :
                print('Entered password is incorrect.')
        else :
            print('Please select a valid option.')


def download_file(filepath):
    user=current_user()
    relfilepath=os.path.relpath(filepath,os.getenv('HOME'))
    scheme=get_scheme(user)
    token=get_token()
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization': token
    }
    url='http://10.2.224.70:8000/files/'+relfilepath+'/'
    r=requests.get(url,headers=headers)
    json_data=json.loads(r.content)
    json_content=json.dumps(json_data['content'])
    json_content = json_content.split('"')[1]
    json_md5sum = json.dumps(json_data['md5sum'])
    if (scheme == 'aes'):
        with open('input.aes','w') as f:
            f.write(re.sub('(.{64})','\\1\n',json_content,0,re.DOTALL))
        os.system('cat input.aes | openssl enc -base64 -d | openssl aes-256-cbc -d -a | openssl enc -base64 -d > '+os.getenv('HOME')+'/'+relfilepath)
        os.system('rm -f input.aes')
    elif (scheme == 'des'):
        with open('input.aes','w') as f:
            f.write(re.sub('(.{64})','\\1\n',json_content,0,re.DOTALL))
        os.system('cat input.aes | openssl enc -base64 -d | openssl des-cbc -d -a | openssl enc -base64 -d > '+os.getenv('HOME')+'/'+relfilepath)
        os.system('rm -f input.aes')
    # md5sum=mdsum(os.getenv('HOME')+'/'+relfilepath)
    # if (json_md5sum.split('\"')[1] == md5sum):
    #     return 1
    # else:
    #     return 2
    return 1
    

def sync_file_from_client(filepath):
    filename=file_name(filepath)
    md5sum=mdsum(filepath)
    relfilepath=os.path.relpath(filepath,os.getenv('HOME'))
    token=get_token()
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization':token
    }
    url='http://10.2.224.70:8000/files/'+relfilepath+'/'
    r=requests.get(url,headers=headers)
    print('Syncing: '+filename)
    if (r.status_code == 404):
        upload_file(filepath)
    else:
        json_data=json.loads(r.content)
        json_md5sum=json.dumps(json_data['md5sum'])
        if (json_md5sum.split('\"')[1] != md5sum):
            delete_file(filepath)
            upload_file(filepath)
    print('Sync successful.')


def sync_file_from_server(filepath):
    filename=file_name(filepath)
    md5sum=mdsum(filepath)
    relfilepath=os.path.relpath(filepath,os.getenv('HOME'))
    token=get_token()
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization':token
    }
    url='http://10.2.224.70:8000/files/'+relfilepath+'/'
    r=requests.get(url,headers=headers)
    json_data=json.loads(r.content)
    json_md5sum=json.dumps(json_data['md5sum'])
    if (r.status_code == 404):
        print('No such file exists.')
    else:
        print('Syncing: '+filename)
        json_data=json.loads(r.content)
        json_md5sum=json.dumps(json_data['md5sum'])
        if (json_md5sum.split('\"')[1] != md5sum):
            os.system('rm -rf '+os.relfilepath)
            download_file(filepath)
        print('Sync successful.')


def sync_dir_from_client(dirpath):
    for f in os.listdir(dirpath):
        fpath=dirpath+'/'+f
        if os.path.isfile(fpath):
            sync_file_from_client(fpath)
        elif os.path.isdir(fpath):
            sync_dir_from_client(fpath)


def sync_delete_from_server(dirpath):
    token=get_token()
    headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Authorization':token
    }
    url='http://10.2.224.70:8000/files/'
    r=requests.get(url,headers=headers)
    json_data=json.loads(r.content)
    for file_info in json_data:
        filepath=file_info['filename']
        reldirpath=os.path.relpath(dirpath,os.getenv('HOME'))
        relfilepath=os.path.relpath(filepath,reldirpath)
        if not relfilepath.startswith('..'):
            file_exists=os.path.isfile(os.getenv('HOME')+'/'+filepath)
            if not file_exists:
                delete_file(os.getenv('HOME')+'/'+filepath)


def sync_dir_from_server(dirpath):
    token=get_token()
    headers={
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Authorization':token
        }
    url='http://10.2.224.70:8000/files/'
    r=requests.get(url, headers=headers)
    json_data=r.json()
    for file_info in json_data:
        filepath=os.getenv('HOME')+'/'+file_info['filename']
        reldirpath=os.path.relpath(dirpath,os.getenv('HOME'))
        relfilepath=os.path.relpath(filepa8th,dirpath)
        if not relfilepath.startswith('..'):
            if os.path.isfile(filepath):
                sync_file_from_server(filepath)
            else:
                if (relfilepath.count('/') > 0  ):
                    innerdir_list=relfilepath.split('/')[0:-1]
                    filename=relfilepath.split('/')[-1]
                    innerdir=''
                    for d in innerdir_list:
                        innerdir=innerdir+'/'+d
                    final_path=os.getenv('HOME')+'/'+reldirpath+innerdir
                    os.system('mkdir -p '+final_path)
                    os.system('touch '+final_path+'/'+filename)
                    sync_file_from_server(final_path+'/'+filename)
                else:
                    final_path=os.getenv('HOME')+'/'+reldirpath
                    os.system('touch '+final_path+'/'+filename)
                    sync_file_from_server(final_path+'/'+filename)


def sync_delete_from_client(dirpath):
    reldirpath=os.path.relpath(dirpath,os.getenv('HOME'))
    homedirpath=os.getenv('HOME')+'/'+reldirpath
    for d in os.listdir(homedirpath):
        if os.path.isfile(homedirpath+'/'+d):
            token=get_token()
            headers={
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Authorization':token
            }
            url='http://10.2.224.70:8000/files/'+reldirpath+'/'+d+'/'
            r=requests.get(url,headers=headers)
            if (r.status_code == 404):
                os.system('rm -f '+homedirpath+'/'+d)
        elif os.path.isdir(homedirpath+'/'+d):
            sync_delete_from_client(dirpath+'/'+d)
    if not os.listdir(dirpath):
        os.rmdir(dirpath)


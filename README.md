# Secure Personal Cloud
## Linus client Usage:
usage: spc.py [-h] [--login LOGIN] [--logout LOGOUT] [--remove_account REMOVE_ACCOUNT] [-u UPLOAD] [-d DOWNLOAD] [-l] [--delete DELETE]
              [--encdec ENCDEC ENCDEC] [-sfc SYNC_FROM_CLIENT] [-sfs SYNC_FROM_SERVER] [-v VERSION] [--help_section]

optional arguments:<br/>
  -h, --help            show this help message and exit<br/>
  --login LOGIN<br/>
  --logout LOGOUT<br/>
  --remove_account REMOVE_ACCOUNT<br/>
  -u UPLOAD, --upload UPLOAD<br/>
  -d DOWNLOAD, --download DOWNLOAD<br/>
  -l, --list<br/>
  --delete DELETE<br/>
  --encdec ENCDEC ENCDEC<br/>
  -sfc SYNC_FROM_CLIENT, --sync_from_client SYNC_FROM_CLIENT<br/>
  -sfs SYNC_FROM_SERVER, --sync_from_server SYNC_FROM_SERVER<br/>
  -v VERSION, --version VERSION<br/>
  --help_section<br/>
## Tasks Accomplished
### 1. Web Server:
* Registration of Users
* Receive encrypted data
*Store received information in database
* Changing the encrption scheme on the user’s request
* Provide Django-REST-API framework
* Lock-based sync implementation

### 2. Web Client:
* Registration and login page for users
* Encryption scheme selection page
* Viewing text and image files on the browser
* Opening media files on the browser
* Storage of scheme and key in the local storage of the browser

### 3. Linux Client:
* Terminal command to access web server
* Login to the server from the client
* Upload/download files to/from the server
* View the files uploaded on the server
* Sync to the server from the client and vice versa
* Allowing only one sync at a time

## Analysis
### 1. Registration:
1. The user can register for his/her account using the web client.
2. While using the web client, the user is provided with a registraion form where the required information is to be filled in.
3. Information required includes user name, email-id and password.
4. Django form is used for registration.
### 2. Login:
1. An existing user can login using the web client or the linux client.
2. While using the web client, the user is asked for his/her user name followed by the password that was entered during registration.
3. The same procedure applies to the linux client.
4. After login, the user is redirected to the page containing his/her uploads.
### 3. Encryption Scheme:
1. OpenSSL library is used for encryption-decryption procedure.
2. The user is provided with AES as the default encryption scheme at the time of registration.
3. The user can change the encryption scheme anytime using either the web client or the linux client.
4. Encryption schemes provided are AES and DES.
5. The user must know the decryption key for the scheme used by him/her.

### 4. File Upload and Download:
1. The files can be upoaded only using the linux client.
2. The files are encrypted using the chosen encrpytion scheme before uploading.
3. The encrypted files are converted to base-64 representation before encryption.
4. Encrypted files are sent to the server through the API.
5. Uploaded files can be downloaded through linux client as well as web client.
6. The user can also delete the files on the server.

### 5. API:
1. All the interaction between the linux client and the web server takes place through the API.
2. The API verifies the user through the token provided at the time of login
3. The API can access the user’s data on the server.
### 6. Database:
1. The encryption scheme is stored in user class which is derived from the class AbstractUser.
2. The file object has the following fields:
* File name.
* File type.
* md5sum of the file.
* File content in encrypted binary form.
* Owner of the file as foreign key.
### 7. Libraries and Modules:
* Front-end : Bootstrap
* API : DjangoREST framework
* Authentication : JWD token
* Encrpytion-Decryption : OpenSSL library
* Encrpytion-Decryption : CryptoJS
* Python : os, argparse, json and request modules

## References
[1] Django documentation, available at [Django-2.1](https://docs.djangoproject.com/en/2.1/)
<br />
[2] Python documentation, available at [Python3](https://docs.python.org/3/)

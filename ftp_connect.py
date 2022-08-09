import getpass
import os
from ftplib import FTP

try:
    def connect_ftp(ftp_server, ftp_login, ftp_password,
                    folder, filename_pdf):
        ftp = FTP(ftp_server)
        ftp.login(ftp_login, ftp_password) 
        user = getpass.getuser()

        ftp.cwd('')

        dir_file = fr'C:\Users\{user}\Downloads\{filename_pdf}'
        file = open(dir_file, 'rb')
        name_file = os.path.basename(dir_file)
        
        if folder == 'Option1':
            ftp.cwd('Folder1')
            ftp.storbinary(f'STOR {name_file}', file)
                
        if folder == 'Option2':
            ftp.cwd('Folder2')
            ftp.storbinary(f'STOR {name_file}', file)
                
        if folder == 'Option3':
            ftp.cwd('Folder3')
            ftp.storbinary(f'STOR {name_file}', file)

        #   close ftp
        file.close()
        ftp.quit()


except Exception as exc:
    print(exc)
    

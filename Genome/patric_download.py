
# import
import ftplib
import os
# set url and password
url = "ftp.patricbrc.org"
user = "anonymous"
password = "anonymous"

# login
ftp = ftplib.FTP(url)
ftp.login(user, password)
root = "/patric2/genomes"

# a function to download from patric
def downloader(ID):
    
    local_filename = os.path.join("/home/hermuba/resistanceExp/genome", ID+'.fna')
    lf = open(local_filename, "wb")

    ftp.cwd(root + '/' + ID)
    ftp.retrbinary("RETR " + ID + ".fna", lf.write, 8*1024)
    lf.close()


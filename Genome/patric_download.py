
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

# path of genome
mypath = "/home/hermuba/resistanceExp/genome"
# a function to download from patric
def downloader(ID):
    
    local_filename = os.path.join(mypath, ID+'.fna')
    lf = open(local_filename, "wb")

    ftp.cwd(root + '/' + ID)
    ftp.retrbinary("RETR " + ID + ".fna", lf.write, 8*1024)
    lf.close()

# check if we already have that file
def update(ID):
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    if ID+'.fna' in onlyfiles:
        print("we already have", ID)
    else:
        downloader(ID)

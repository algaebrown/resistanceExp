
# import
import ftplib
import os
from multiprocessing import Pool

# set url and password
url = "ftp.patricbrc.org"
user = "anonymous"
password = "anonymous"


# path of genome
mypath = "/home/hermuba/data/genome/"
# a function to download from patric
def downloader(ID):

    local_filename = os.path.join(mypath, ID+'.fna')
    print("downloading ",ID, ' to ', local_filename)

    with open(local_filename, "wb") as lf:
        ftp.cwd(root + '/' + ID)
        ftp.retrbinary("RETR " + ID + ".fna", lambda data: lf.write(data))

# check if we already have that file
missing = []
def update(ID):

    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

    if ID+'.fna' in onlyfiles:
        print("we already have", ID)
    else:
        missing.append(ID)


with open('/home/hermuba/data0118/genomeList/all') as f:
    genome_list = f.readlines()
genome_list = list(map(lambda x: x.replace('\n', ''), genome_list))

for i in genome_list:
    update(i)

# login
ftp = ftplib.FTP(url)
ftp.login(user, password)
root = "/patric2/genomes"
print(len(missing), len(genome_list))
with Pool(5) as p:
    p.map(downloader, missing)

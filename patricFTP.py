# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 18:56:08 2017
extract data from PATRIC ftp
@author: Charl
"""

#!/bin/env python


import ftplib
import wanted # write wanted files in a variable "wanted" as a list

# configuration
url = "ftp.patricbrc.org"
user = "anonymous"
password = "anonymous"

ftp = ftplib.FTP(url) # url
ftp.login(user, password) # user and password

files = []

# recursive downloading of wanted files
def digg(nlst_old, path):
    for possible in nlst_old: 
        try:
            ftp.cwd(path + '/' + possible)
            nlst_new = ftp.nlst()
            digg(nlst_new, path + '/' + possible)
        except:
            if possible in wanted.wanted: # please fill the wanted list in wanted.py
                ftp.transfercmd('GET ' + possible)

root = '/patric2/genomes'
digg(ftp.nlst(root), root)
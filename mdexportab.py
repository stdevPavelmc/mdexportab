#!/usr/bin/env python3

########################################################
# Script to export the MDaemon Addresbook for all users
# in a domain folder
#
# Author: pavelm@gmail.com @stdevPavelmc in github
# 
# Python 3 for windows or copy the domain folder to linux
########################################################

import os
import xml.etree.ElementTree as ET

DEBUG = False

def detect_folders_inside(fpath):
    """Detect folders inside a specific path, retuned as a list"""

    if DEBUG:
        print(":: Parsing folder {}".format(fpath))
    
    folders = []
    for d in os.listdir(fpath):
        if DEBUG:
            print("::: {}".format(d))
        
        if os.path.isdir(os.path.join(fpath, d)):
            folders.append(d)
        else:
            if DEBUG:
                print("::: Discard file: {}".format(d))

    return folders

def get_mrk_files(fpath):
    """Get the addressbook files and parse it on an array indexed by the username
    return that array"""

    files = []

    # r=root, d=directories, f= files
    for r, d, f in os.walk(fpath):
        for file in f:
            if '.mrk' in file:
                files.append(os.path.join(r, file))

    return files

def parse_mrk_file(userab, ab):
    """Parse the ab file, ignoring already parsed entries"""

    for c in ab.iter('contact'):
        try:
            name = c.find('fullName').text
            email = c.find('email').text

            # final string
            entry = name + ";" + email + ";"
            if not entry in userab:
                userab.append(entry)
        except:
            pass

    return userab

if __name__ == "__main__":
    # work on local path
    path = './'

    # domain, first folder on actual path
    domain = detect_folders_inside(path)[0]
    print(">> Local domain folder is:\n{}".format(domain))
    dpath = os.path.join(path, domain)

    # users
    users = detect_folders_inside(os.path.join(path, domain + os.sep))
    print(">> User's folders detected on that domain:")
    for uf in users:
        print(uf)

    # create the output directory
    opath = os.path.join(path, "output")
    print(opath)
    os.makedirs(opath, exist_ok=True)

    # parsing users
    for u in users:
        print("Parsing user: {}".format(u))
        upath = os.path.join(dpath, u)

        # users address book
        userab = []

        files = get_mrk_files(upath)
        for f in files:
            # load the file
            try:
                xf = ET.parse(f)
                ab = xf.getroot()
            except:
                pass
                continue

            # detect if the file has valid entries
            if len(ab) != 0: 
                userab = parse_mrk_file(userab, ab)

        if len(userab) > 0:
            # notice
            print("User: {}, rescued {} contacts".format(u, len(userab)))
            # write the file for that user
            uf = os.path.join(opath, u + ".csv")
            print(uf)
            with open(uf, mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(userab))

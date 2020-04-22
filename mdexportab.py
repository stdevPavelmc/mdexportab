#!/usr/bin/env python3

#########################################################################################
# Script to export the MDaemon Addresbook for all users in one or various domain folders
#
# Author: pavelm@gmail.com @stdevPavelmc in github
# 
# Instructions:
#   - Install Python 3.5 or later for windows
#   - Copy this script to the "Users" folder where MDaemon put it's domain folders 
#   - Run the script from inside that folder 
#########################################################################################

import os
from xml.etree import ElementTree as ET
from quopri import encodestring as qpencode

def detect_folders_inside(fpath):
    """Detect folders inside a specific path, retuned as a list"""

    folders = []
    for d in os.listdir(fpath):
        if os.path.isdir(os.path.join(fpath, d)):
            folders.append(d)

    return folders

def get_mrk_files(fpath):
    """Get the addressbook files for a given path"""

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
        contact = []
        try:
            name = c.find('fullName').text
            email = c.find('email').text
        except:
            pass
            continue

        # create the contact list
        if email != "":
            contact.append(name)
            contact.append(email)

        # append if not already
        if not contact in userab:
            userab.append(contact)

    return userab

def vcfWriter(contact):
    """Adapted from the file format produced by mozilla thunderbird and some examples online"""

    name, email = contact
    vcfLines = []
    vcfLines.append('begin:vcard')
    vcfLines.append('version:2.1')
    if name != email:
        ename = qpencode(name.encode()).decode()
        vcfLines.append('fn;quoted-printable:{}'.format(ename))
    vcfLines.append('email;internet:{}'.format(email))
    vcfLines.append('end:vcard')
    vcfString = '\n'.join(vcfLines) + '\n\n'
    return vcfString

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
            uf = os.path.join(opath, u + ".vcf")
            print(uf)
            with open(uf, mode='wt', encoding='utf-8') as myfile:
                for c in userab:
                    myfile.write(vcfWriter(c))

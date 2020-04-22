# Python script to export the MDaemon users's address books in case of a mail server migration

That's it: a handy python script to export all the users addressbooks from the WorldClient MDaemon to a vCard format.

## Motivation

- I need a simple tool to make this for my daily job (IT FLOSS migration services in Cuba)
- It's a trivial task
- Some apps out there ask you more than $50 bucks (USD) for a licence.

## What's the deal?

A simple python script that will give you a folder plenty of `[username].vcf` files in the vCard format 2.1, that can be imported in most email clients out there.

The script is GPLv3 aka free/libre software, contributions, bug reports & comment are welcomed.

## How to make it work?

0. Install python 3.5 or later on your windows PC that runs the MDaemon instance and add the python executable to the environment _(google search: windows add python.exe to the environment PATH)_
0. Copy the `mdexport.py` script to the MDaemon's "Users" folder that holds your domain(s) accounts
0. Open a windows's cmd or powershell session and move to that folder
0. Run `python.exe mdexportab.py` in your console and wait for it
0. Your data will reside on a newly created `output` folder

## FAQ

**It's possible to export the data in another format?**

Yes, drop me a tweet (@co7wt) or an issue on this repository and I will think about it

**It only works with that precise version of Python?**

No, it _must_ work with any python in the 3.x branch; for example in a recent migration job I found that a Windows 2008 server can't install the latest python 3.8.x and ask me for a service pack and a .NET version... using an old python version (3.5) I managed to wun it and avoid the nasty & time-consumming upgrade and .NET install

**Why it's not exporting data for some users? or I have 200 users and only exported data for 123 of them?**

Simply, some users don't have any address in their addressbook files, that users will not have a .vcf file

**I ran the script and it's taking ages to finish, is that normal?**

It depends on the user count, the contacts per users, and even on the hardware & PC load at the time of run

For example: in a Production PC that is a Corei3 (4th gen) PC with 8 GB of RAM and Windows Server 2008 r2 with other services in the bacground (MSSQL, Domain Controller & MDaemon server) it took about 8 minutes for ~50 users and about 1200 contacts globally

**I wonder if your script can do A, B or even C new feature... can you implement that?**

Yes, but remember It's a hobby for me and I work on it holliday/weekend style; it can take a while to be implemented, use the issues feature ot github to report your request

**Hey! this is a great tool and I want to donate some of the saved ~$50 bucks to you**

Thank you, please contact me on twitter for instructions my nick there is @co7wt

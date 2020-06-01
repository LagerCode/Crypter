import sqlite3, subprocess
from tkinter import *
from tkinter import filedialog
import os




#encryption function
def enc():
    try:
        #Choosing file to encrypt
        fileToBeEnc = filedialog.askopenfilename(initialdir="/home/",
                            title="Select a file")

        # Encrypting the choosen file with pgp, using a passphrase
        subprocess.run(["gpg", "-c", fileToBeEnc],
                       shell=False,)

        #Removing the unecrypted file
        subprocess.run(["rm", fileToBeEnc],
                       shell=False)

        #clear gpg cache after encryption so password for decrypting is required immediatly
        getdir = os.getcwd()
        subprocess.run(getdir+'/crypterSH/cleargpgcache.sh',
                       shell=False)

    except:
        print("Something went wrong")

#decryption function
def dec():
    try:
        #Choosing file to decrypt
        fileToBeDec = filedialog.askopenfilename(initialdir="/home/",
                                             title="Select a file")

        #Decrypting the file with gpg, using a passphrase
        subprocess.run(['gpg', fileToBeDec],
                       shell=False,
                       stdout=True,
                       stdin=True)
    except:
        print("Something went wrong")








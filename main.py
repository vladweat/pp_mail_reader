import os
import re
import email
import base64
import imaplib

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.header import decode_header

load_dotenv()

mail_pass = os.getenv("MAIL_PASS")
mail_addr = os.getenv("MAIL_ADDRESS")
imap_server = "imap.rambler.ru"

def get_mail_sever(mail_addr, mail_pass, imap_server):
    imap = imaplib.IMAP4_SSL(imap_server)
    if imap.login(mail_addr, mail_pass)[0] == "OK":
        return imap
    else:
        print(imap.login(mail_addr, mail_pass))

imap = get_mail_sever(mail_addr, mail_pass, imap_server)
print(imap.select("INBOX"))
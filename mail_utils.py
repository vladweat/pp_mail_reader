import os
import re
import email
import base64
import imaplib

from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from email.header import decode_header

load_dotenv()

def parse_date(date):
    date = datetime(
        year=date[0],
        month=date[1],
        day=date[2],
        hour=date[3],
        minute=date[4],
    )
    return date


def get_mail_sever(mail_addr, mail_pass, imap_server):
    imap = imaplib.IMAP4_SSL(imap_server)
    if imap.login(mail_addr, mail_pass)[0] == "OK":
        return imap
    else:
        print(imap.login(mail_addr, mail_pass))


# imap = get_mail_sever(mail_addr, mail_pass, imap_server)
def get_date(imap, index):
    msg = get_letter(imap, index)
    
    letter_date = email.utils.parsedate_tz(
        msg["Date"]
    )

    return parse_date(letter_date)

def get_header(imap, index):
    msg = get_letter(imap, index)
    
    try:
        letter_subject = decode_header(msg["Subject"])[0][0].decode()
    except:
        letter_subject = msg["Subject"]

    return letter_subject


def get_num_of_emails(imap):
    num = int(imap.select("INBOX")[1][0].decode("utf-8"))
    return num


def get_index_of_letter(imap, index):
    imap.select("INBOX")
    tmp = imap.search(None, "ALL")[1][0].decode("utf-8")
    num_of_letters = tmp.split(" ")[index - 1].encode("utf-8")
    return num_of_letters


def get_letter(imap, index):
    index_of_letter = get_index_of_letter(imap, index)
    res, msg = imap.fetch(index_of_letter, "(RFC822)")

    msg = email.message_from_bytes(msg[0][1])
    return msg


def get_letter_text(imap, index):
    msg = get_letter(imap, index)

    letter_date = email.utils.parsedate_tz(
        msg["Date"]
    )  # дата получения, приходит в виде строки, дальше надо её парсить в формат datetime
    letter_id = msg["Message-ID"]  # айди письма
    letter_from = msg["Return-path"]  # e-mail отправителя

    # проверка на заголовка на латиницу/кириллицу
    try:
        letter_subject = decode_header(msg["Subject"])[0][0].decode()
    except AttributeError:
        letter_subject = msg["Subject"]

    # проверка наличия заголовка, если нет, то указывается строка
    if letter_subject is None:
        letter_subject = "NoneType"

    # for part in msg.walk():
    #     print(part.get_content_type())

    if msg.is_multipart():
        try:
            for part in msg.walk():
                if (
                    part.get_content_maintype() == "text"
                    and part.get_content_subtype() == "html"
                ):
                    return base64.b64decode(part.get_payload()).decode()
        except:
            for part in msg.walk():
                if (
                    part.get_content_maintype() == "text"
                    and part.get_content_subtype() == "html"
                ):
                    return part.get_payload()
    else:
        return "Nothing"

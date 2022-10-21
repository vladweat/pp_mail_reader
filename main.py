from mail_utils import *
from bs4 import BeautifulSoup

mail_pass = os.getenv("MAIL_PASS")
mail_addr = os.getenv("MAIL_ADDRESS")
imap_server = "imap.rambler.ru"


def write_text(path, text):
    with open(path, "a+") as file:
        file.write(text)
    
    with open(path, "r") as file:
        lines = file.readlines()
        lines[:] = [line for line in lines if line.strip()]

    with open(path, "w") as file:
        file.writelines(lines)

def write_header_and_time(path, header, date):
    string = f"{header} \n {date} \n"
    
    with open(path, "a+") as file:
        file.write(string)

def get_clear_text(imap, index):
    soup = BeautifulSoup(get_letter_text(imap, index))
    clear_text = soup.get_text()
    return clear_text

def archive_all_mails():
    imap = get_mail_sever(mail_addr, mail_pass, imap_server)
    num_mails = get_num_of_emails(imap)

    for i in range(8):
        header = get_header(imap, i)
        date = get_date(imap, i)
        text = get_clear_text(imap, i)
        
        write_header_and_time(f"archive/{mail_addr[:8]}-{i + 1}.txt", header, date)
        write_text(f"archive/{mail_addr[:8]}-{i + 1}.txt", text)

# еахождения такого же заголовка как и header, затем изьятие кодов и т.д.
def find_all_filtered(header):
    imap = get_mail_sever(mail_addr, mail_pass, imap_server)
    num_mails = get_num_of_emails(imap)

    indexes = []
    
    for i in range(num_mails, 0, -1):
        if get_header(imap, i) == header:
            print("find")
            indexes.append(i)
    print(indexes)
    
if __name__ == "__main__":
    # find_all_filtered("Amazon Authentication")
    archive_all_mails()
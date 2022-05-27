#check mailbox for images and drop them into nextcloud
import imaplib
import email
from datetime import datetime

from dotenv import dotenv_values

def download_attachments():
    config = dotenv_values('.env')
    with imaplib.IMAP4_SSL(host=config['HOST'], port=993) as imap_ssl:
        resp_code, response = imap_ssl.login(config['EMAIL'], config['PASSWORD'])

        resp_code, mail_count = imap_ssl.select(mailbox='Inbox')

        resp_code, mails = imap_ssl.search(None, '(SUBJECT "text message") UNSEEN')

        for mail_id in mails[0].decode().split()[-2:]:
            resp_code, mail_data = imap_ssl.fetch(mail_id, '(RFC822)')
            message = email.message_from_bytes(mail_data[0][1])
            subject = message.get('Subject')
            print(subject)
            if '***REMOVED***' in subject:
                path = config['BASEPATH'] + '***REMOVED***/files/Photos/Phone_Uploads/'
            elif '***REMOVED***' in subject:
                path = config['BASEPATH'] + '***REMOVED***/files/Photos/Phone_Uploads/'
            for part in message.walk():
                filename = part.get_filename() if part.get_filename() else str(datetime.now())+'.jpg'
                if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                    open(path + filename, 'wb').write(part.get_payload(decode=True))
            imap_ssl.copy(mail_id, 'Processed_Photos')
            imap_ssl.store(mail_id, '+FLAGS', '\Deleted')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    download_attachments()


#check mailbox for images and drop them into nextcloud
import imaplib
import email
from datetime import datetime

from dotenv import dotenv_values

import nextcloud_client

def download_attachments():
    config = dotenv_values('/usr/local/sbin/imap-to-nextcloud/.env')
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
                path = config['BASEPATH'] + '/Photos/'
            elif '***REMOVED***' in subject:
                path = config['BASEPATH'] + '/Photos (***REMOVED***)/'
            for part in message.walk():
                filename = part.get_filename() if part.get_filename() else str(datetime.now())+'.jpg'
                if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                    add_to_nextcloud(config, part, path+filename)
            imap_ssl.copy(mail_id, 'Processed_Photos')
            imap_ssl.store(mail_id, '+FLAGS', '\Deleted')


def add_to_nextcloud(config, part, filename):
    nc = nextcloud_client.Client(config['NEXTCLOUD_DOMAIN'])

    nc.login(config['NEXTCLOUD_USER'], config['NEXTCLOUD_PASSWORD'])

    nc.put_file_contents(filename, part.get_payload(decode=True))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    download_attachments()


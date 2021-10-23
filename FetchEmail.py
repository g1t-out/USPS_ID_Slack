import email
import imaplib
import os
import re
## Came from https://stackoverflow.com/questions/6225763/downloading-multiple-attachments-using-imaplib
class FetchEmail():

    connection = None
    error = None

    def __init__(self, mail_server: str, username: str, password: str) -> None:
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()
    
    def select_folder(self,folder: str) -> None:
        self.connection.select(folder,readonly=False)

    def save_attachments(self,msg_uid: str, download_folder: str="/tmp") -> list[str]:
        """
        Given a message in the folder. It will pull the message and save the attachments to a download folder
        Returns a list of paths to attachments
        """
        return_val = []
        if download_folder.endswith("/"):
            download_folder = download_folder[:-1] #Stripping off the trailing /
        ret, data = self.connection.uid('FETCH', msg_uid,'(RFC822)')
        if ret == 'OK':
            mail = email.message_from_bytes(data[0][1])
            for part in mail.walk():
                if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                    try:
                        open(download_folder + '/' + part.get_filename(), 'wb').write(part.get_payload(decode=True))
                        return_val.append(download_folder + "/" + part.get_filename())
                    except:
                        raise Exception("Could not write to output folder.")
            return return_val
        else:
            raise Exception("Could not fetch message")

    def move_message(self, msg_uid: str, new_folder: str) -> None:
        """
        Given a message uid and a folder, will move a message to a different folder.
        Run select_folder before this, so it has a folder to operate in.
        """
        result, data = self.connection.uid('COPY', msg_uid, new_folder)

        if result == 'OK': #Item was copied okay
            mov, data2 = self.connection.uid('STORE',msg_uid, '+FLAGS', '(\Deleted)')
            data2 = self.connection.expunge()

    def delete_message(self, msg_uid: str) -> None:
        """
        Give a message uid, it will delete the item.
        Run select_folder before this, so it has a folder to operate in.
        """
        mov, data = self.connection.uid('STORE',msg_uid, '+FLAGS', '(\Deleted)')
        data = self.connection.expunge()

    """ This function is untested.
    def fetch_unread_messages(self):
        
        Retrieve unread messages
        
        emails = []
        (result, messages) = self.connection.search(None, 'UnSeen')
        if result == "OK":
            for message in messages[0].split():
                try: 
                    ret, data = self.connection.fetch(message,'(RFC822)')
                except:
                    print("No new emails to read.")
                    self.close_connection()
                    exit()

                msg = email.message_from_bytes(data[0][1])
                if isinstance(msg, str) == False:
                    emails.append(msg)
                response, data = self.connection.store(message, '+FLAGS','\\Seen')

            return emails

        self.error = "Failed to retreive emails."
        return emails
    """
    def fetch_messages(self) -> list[str]:
        """
        Returns a list of message UIDs in the currently selected folder
        """
        pattern_uid = re.compile(r'\d+ \(UID (?P<uid>\d+)\)')
        returnval = []
        (result, messages) = self.connection.search(None, 'All')
        if result == "OK":
            for message in messages[0].split():
                (resp, data) = self.connection.fetch(message, "(UID)")
                if resp == "OK":
                    uid = pattern_uid.match(data[0].decode())
                    returnval.append(uid.groups(0)[0])
                else:
                    raise Exception("Could not get UID for message")
        else:
            raise Exception("Retrieve Messages was not Okay")
        return returnval
import os.path
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

class cred_managment:
    def make_cred():
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.send']
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('data\\token.json'):
            creds = Credentials.from_authorized_user_file('data\\token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('data\\credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('data\\token.json', 'w') as token:
                token.write(creds.to_json())
    
    def load_cred():
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.send']
        if os.path.exists('data\\token.json'):
            creds = Credentials.from_authorized_user_file('data\\token.json', SCOPES)
        else:
            cred_managment.make_cred()
            creds = Credentials.from_authorized_user_file('data\\token.json', SCOPES)
        return creds
    
    
def gmail_send_message(logger,username,message,receiver_email):
    try:
        creds = cred_managment.load_cred()
        
        try:
            # create gmail api client
            service = build('gmail', 'v1', credentials=creds)

            Message = EmailMessage()

            Message.set_content(message)

            Message['To'] = receiver_email
            Message['From'] = os.getenv('EMAILER_MAIL_FOR_SEND')
            Message['Subject'] = 'Automated draft'

            # encoded message
            encoded_message = base64.urlsafe_b64encode(Message.as_bytes()).decode()

            create_message = {'raw': encoded_message}
            # pylint: disable=E1101
            send_message = (service.users().messages().send(userId="me", body=create_message).execute())
            print("Email send successfully")
            logger.info("[INFO] Email send successfully from user: "+username+" ,with id:"+send_message["id"])
            
        except HttpError as error:
            print("Error sending email")
            logger.warning("[SECURITY] Error while trying to send email from user: "+username)
            logger.debug("[DEBUG] Error: "+str(e))
            
    except Exception as e:
        print("Error sending email")
        logger.warning("[SECURITY] Error while trying to send email from user: "+username)
        logger.debug("[DEBUG] Error: "+str(e))


if __name__ == '__main__':
    gmail_send_message('',"","test","(testmail@gmail.com)")
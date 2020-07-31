import smtplib
import os
from dotenv import load_dotenv

load_dotenv()


def send_email(msg):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(os.environ['EMAIL1'], os.environ['EMAIL_PASS'])
    smtpObj.sendmail(
        os.environ['EMAIL1'], os.environ['EMAIL2'], f'{msg}')
    smtpObj.quit()

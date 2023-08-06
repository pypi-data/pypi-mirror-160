import smtplib
from typing import List

from mailer.messageable import Messageable
from mobile.email import Email
from mobile.phone_number import PhoneNumber
from providers.email_credentials import Credentials
from email.mime.text import MIMEText


class TextMessage:
    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    def _createHeader(self, subject: str, body: str, recipients: List[str]) -> MIMEText:
        msg = MIMEText(body)
        msg['From'] = self.credentials.email
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject

        return msg

    def send(self, subject: str, body, recipients: List[Messageable]):
        pass

    def text(self, subject: str, body: str, recipients: List[PhoneNumber]):
        self.send(subject=subject, body=body, recipients=recipients)

    def email(self, subject: str, body: str, recipients: List[str]) -> None:
        emails = list(map(lambda num: Email(num), recipients))
        self.send(subject=subject, body=body, recipients=emails)

    def email(self, subject: str, body: str, recipients: List[Email]):
        self.send(subject=subject, body=body, recipients=recipients)

    def send(self, subject: str, body: str, recipients: List[Messageable]):
        emails = list(map(lambda num: num.email, recipients))
        server = smtplib.SMTP(host=self.credentials.provider.host, port=self.credentials.provider.port)
        server.connect(host=self.credentials.provider.host, port=self.credentials.provider.port)
        server.starttls()
        server.login(user=self.credentials.email, password=self.credentials.password)
        msg = self._createHeader(subject=subject, body=body, recipients=emails)
        server.sendmail(from_addr=self.credentials.email, to_addrs=emails, msg=msg.as_string())
        server.quit()
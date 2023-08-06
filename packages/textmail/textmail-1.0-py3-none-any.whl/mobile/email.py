from mailer.messageable import Messageable


class Email(Messageable):

    def __init__(self, email):
        self._email = email

    @property
    def email(self):
        return self._email

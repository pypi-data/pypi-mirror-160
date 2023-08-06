from abc import abstractmethod

from mailer.messageable import Messageable


class PhoneNumber(Messageable):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    @property
    @abstractmethod
    def email_extension(self) -> str:
        pass

    @property
    def number(self) -> str:
        return self.clean() + "@" + self.email_extension

    def clean(self) -> str:
        return str(self.phone_number).replace("-", "")

    @property
    def email(self):
        return self.number



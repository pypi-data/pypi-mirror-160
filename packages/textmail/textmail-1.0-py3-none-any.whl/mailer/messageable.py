from abc import abstractmethod


class Messageable:

    @property
    @abstractmethod
    def email(self):
        pass
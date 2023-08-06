from abc import abstractmethod


class MailProvider:
    def __init__(self):
        pass

    @property
    @abstractmethod
    def host(self) -> str:
        pass

    @property
    @abstractmethod
    def port(self) -> int:
        pass

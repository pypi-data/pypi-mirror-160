from providers.provider import MailProvider


class Credentials:
    def __init__(self, email: str, password: str, provider: MailProvider):
        self._email = email
        self._password = password
        self._provider = provider

    @property
    def provider(self) -> MailProvider:
        return self._provider

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

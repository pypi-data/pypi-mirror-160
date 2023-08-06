from providers.provider import MailProvider


class Gmail(MailProvider):
    @property
    def host(self) -> str:
        return "smtp.gmail.com"

    @property
    def port(self) -> int:
        return 587

from providers.provider import MailProvider


class Yahoo(MailProvider):
    @property
    def host(self) -> str:
        return "smtp.mail.yahoo.com"

    @property
    def port(self) -> int:
        return 465

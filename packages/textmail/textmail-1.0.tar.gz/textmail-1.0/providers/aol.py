from providers.provider import MailProvider


class AOL(MailProvider):
    @property
    def host(self) -> str:
        return "smtp.aol.com"

    @property
    def port(self) -> int:
        return 587

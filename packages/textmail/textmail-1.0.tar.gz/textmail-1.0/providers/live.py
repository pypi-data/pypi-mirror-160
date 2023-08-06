from providers.provider import MailProvider


class Outlook(MailProvider):
    @property
    def host(self) -> str:
        return "smtp.live.com"

    @property
    def port(self) -> int:
        return 587

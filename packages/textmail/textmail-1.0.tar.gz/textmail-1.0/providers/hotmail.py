from providers.provider import MailProvider


class Hotmail(MailProvider):
    @property
    def host(self) -> str:
        return "smtp.live.com"

    @property
    def port(self) -> int:
        return 465

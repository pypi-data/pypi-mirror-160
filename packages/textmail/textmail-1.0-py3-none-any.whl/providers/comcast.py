from providers.provider import MailProvider


class Comcast(MailProvider):
    @property
    def host(self) -> str:
        return "smtp.comcast.net"

    @property
    def port(self) -> int:
        return 587

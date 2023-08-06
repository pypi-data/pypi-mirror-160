from providers.provider import MailProvider


class Office365(MailProvider):
    @property
    def host(self) -> str:
        return "smtp.office365.com"

    @property
    def port(self) -> int:
        return 587

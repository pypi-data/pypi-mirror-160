from mobile.phone_number import PhoneNumber


class TMobile(PhoneNumber):
    @property
    def email_extension(self) -> str:
        return "tmomail.net"

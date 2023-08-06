from mobile.phone_number import PhoneNumber


class Verizon(PhoneNumber):
    @property
    def email_extension(self) -> str:
        return "vtext.com"

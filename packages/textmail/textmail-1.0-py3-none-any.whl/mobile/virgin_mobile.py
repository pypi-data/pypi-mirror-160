from mobile.phone_number import PhoneNumber


class VirginMobile(PhoneNumber):
    @property
    def email_extension(self) -> str:
        return "vmobl.com"

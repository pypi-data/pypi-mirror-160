from mobile.phone_number import PhoneNumber


class ATNT(PhoneNumber):
    @property
    def email_extension(self) -> str:
        return "txt.att.net"

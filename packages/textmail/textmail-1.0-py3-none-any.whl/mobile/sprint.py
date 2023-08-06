from mobile.phone_number import PhoneNumber


class Sprint(PhoneNumber):
    @property
    def email_extension(self) -> str:
        return "messaging.sprintpcs.com"

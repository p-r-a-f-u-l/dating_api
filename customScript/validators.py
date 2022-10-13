from datetime import datetime
import re
from django.utils.translation import gettext_lazy as _


def email_validation(value):
    if re.search(r"^[a-zA-Z]+\.[a-zA-Z]+-[a-zA-Z]+@gmail\.com$", value):
        raise ValueError(_("Invalid Email."))


def phone_validation(value):
    if len(value) > 10 and len(value) < 10:
        raise ValueError(_("Phone Number is Invalid."))


def dob_validation(value):
    print(value)


def check_horo(value):
    horo = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]
    if not value in horo:
        raise ValueError(_("Invalid Zodio Submitted."))

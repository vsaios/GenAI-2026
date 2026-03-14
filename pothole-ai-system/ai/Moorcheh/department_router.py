# One job: potholes go to 311 Toronto. That's it.

TORONTO_311 = {
    "name":    "City of Toronto — Transportation Services",
    "email":   "311@toronto.ca",
    "address": "City Hall, 100 Queen St W, Toronto, ON M5H 2N2"
}

def get_311_contact() -> dict:
    return TORONTO_311

def get_311_email() -> str:
    return TORONTO_311["email"]

def get_311_name() -> str:
    return TORONTO_311["name"]

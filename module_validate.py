def validate_email(email):
    if "@" in email and email.endswith(".com") or email.endswith(".edu"):
        local_part, domain_part = email.split("@", 1)
        if local_part and domain_part.startswith("gmail.")  or domain_part.startswith("yahoo.") or domain_part.startswith("outlook."):
            return True
    return False

def validate_contact(no):
    if len(no)<10 or not(no.isdigit()):
        return False
    else:
        return True


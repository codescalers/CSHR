import random
import string


def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    domain = random.choice(['example.com', 'example', ''])
    return f"{random_string}@{domain}"


def generate_random_password():
    random_char = random.choices(string.ascii_letters + string.digits, k=10)
    random_password = ''.join(random_char)
    return random_password


def generate_random_emails(num_emails):
    emails = []
    for _ in range(num_emails):
        email = generate_random_email()
        emails.append(email)
    return emails


def generate_random_passwords(num_passwords):
    passwords = []
    for _ in range(num_passwords):
        password = generate_random_password()
        passwords.append(password)
    return passwords


def generate_random_invalid_email():
    invalid_chars = ['!', '#', '$', '%', '&', '*', '/', '=', '?']
    invalid_domains = ['example', 'invalid', 'test']

    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    domain = random.choice(invalid_domains)
    invalid_char = random.choice(invalid_chars)

    return f"{random_string}{invalid_char}@{domain}.com"


def get_random_invalid_email(num_number):
    numbers = [generate_random_invalid_email() for _ in range(num_number)]
    return numbers

import random
import string


def generate_random_link():
    scheme = random.choice(["http", "https", "  "])
    rando = random.choices(string.ascii_lowercase, k=random.randint(5, 10))
    domain = ''.join(rando)
    extension = random.choice(["com", "org", "net", "  "])
    link = f"{scheme}://www.{domain}.{extension}"
    return link


def create_links(num_links):
    links = [generate_random_link() for _ in range(num_links)]
    return links


def generate_number():
    digits = string.digits + string.ascii_letters + string.punctuation
    length = random.choice([random.randint(1, 5), random.randint(6, 10)])
    larger_number = ''.join(random.choices(digits, k=length))
    smaller_number = ''.join(random.choices(string.digits, k=length))
    return random.choice([larger_number, smaller_number])


def create_numbers(num_number):
    numbers = [generate_number() for _ in range(num_number)]
    return numbers

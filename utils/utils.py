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

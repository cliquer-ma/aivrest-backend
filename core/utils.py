import string
import random

def generate_numbers(string_length=10) :
    assembly = string.digits
    return ''.join(random.choice(assembly) for i in range(string_length))

def generate_string(string_length=10) :
    assembly = string.digits + string.ascii_lowercase
    return ''.join(random.choice(assembly) for i in range(string_length))

def generate_reference(model_name, ref_len):
    reference = None
    while True:
        random = generate_numbers(ref_len)
        if model_name.objects.filter(reference=random).exists():
            continue
        reference = random
        break
    return reference

def is_valid_url(url):
    try:
        import urllib.parse
        urllib.parse.urlparse(url)
        return True
    except ValueError:
        return False

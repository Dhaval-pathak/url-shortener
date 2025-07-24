import random
import string
import re

CODE_LENGTH = 6
ALPHANUM = string.ascii_letters + string.digits


def generate_short_code():
    return ''.join(random.choices(ALPHANUM, k=CODE_LENGTH))


def is_valid_url(url):
    # Basic URL validation
    regex = re.compile(
        r'^(https?://)'  # http:// or https://
        r'([\w.-]+)'    # domain
        r'(:\d+)?'      # optional port
        r'(/[\w./?%&=-]*)?$', re.IGNORECASE)
    return re.match(regex, url) is not None
import re
from urllib.parse import quote

from unidecode import unidecode


def simplify_text(text):

    return unidecode(text)\
        .lower()\
        .replace("'", '')\
        .replace('&', '')


def email_censor(value):
    if '@' not in value:
        return value
    start, end = value.split('@')
    return "{}@{}".format(
        word_censor(start),
        word_censor(end)
    )


def word_censor(value):
    if len(value) <= 1:
        return value
    half = int(len(value) / 2)
    censored = value[0:half] + '*' * (len(value) - half)
    return censored


def pattern_match(pattern, message):
    if re.match(pattern, message):
        return True
    return False


def divide_text(max_chars, text):

    if len(text) <= max_chars:
        return [text]

    texts = []
    for p in re.split('\n', text):
        stripped_p = p.strip()
        if len(stripped_p) > 0:
            texts.append(stripped_p)

    return texts


STRING_OPS = {
    'split': str.split,
    'join': str.join,
    'plain': simplify_text,
    'uppercase': str.upper,
    'lowercase': str.lower,
    'capitalize': str.capitalize,
    'replace': str.replace,
    'trim': str.strip,
    'match?': pattern_match,

    'divide-text': divide_text,
    'url-quote': quote,
    'email-censor': email_censor,
}


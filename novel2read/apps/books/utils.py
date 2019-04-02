import re

from django.utils.text import slugify


def get_unique_slug(cls, name):
    """TODO: other unicode(ru) slugify"""

    slug = slugify(name)
    unique_slug = slug
    num = 1
    while cls.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    return unique_slug


def capitalize_str(string):
    string = ' '.join([w.capitalize() for w in string.split(' ')])
    return string


def capitalize_slug(slug):
    slug = re.sub('\d', '', ' '.join([w.capitalize() for w in slug.split('-')])).strip()
    return slug


def multiple_replace(to_repl, text):
    rep = dict((re.escape(k), v) for k, v in to_repl.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text.strip()

import os
import re
import requests

from mimetypes import guess_extension
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.text import slugify


def download_img(url, file_name):
    resp = requests.get(url)
    resp_type = resp.headers['content-type']
    if resp_type.partition('/')[0].strip() == 'image':
        file_ext = guess_extension(resp_type)
        file_ext = '.jpg' if file_ext == '.jpe' else file_ext
        media_posters = os.path.join(settings.MEDIA_ROOT, 'posters')
        f_path = os.path.join(media_posters, f'{file_name}{file_ext}')
        if not os.path.exists(media_posters):
            os.makedirs(media_posters)
        with open(f_path, 'wb') as f:
            f.write(resp.content)
        return
    else:
        raise ImproperlyConfigured


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

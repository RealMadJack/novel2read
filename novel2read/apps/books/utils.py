import os
import re
import requests

from mimetypes import guess_extension
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils.text import slugify


def download_img(url, file_name):
    url = f'https:{url}' if url[0:1] == '/' else url
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
        return f'{file_name}{file_ext}'
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


def search_multiple_replace(to_repl={}, model='BookChapter'):
    from .models import BookChapterReplace
    b_chap_repls = BookChapterReplace.objects.all()

    for b_chap_repl in b_chap_repls:
        to_repl.update({b_chap_repl.replace: b_chap_repl.replace_to})

    to_repl.update({
        'updatedbyboxnovelcom': '',
        'updatebyboxnovelcom': '',
        'boxnovelcom': '',
        'boxnovel': '',
    })

    if model == 'Book':
        pass
    else:
        from .models import BookChapter
        result = []
        b_chaps = BookChapter.objects.select_related('book')
        for b_chap in b_chaps:
            b_chap_text = re.sub('[^a-zA-Z]+', '', b_chap.text.lower())
            for k, v in to_repl.items():
                if k in b_chap_text:
                    if 'boxnovel' in k:
                        rx_repl = r'.{0,1}\s{0,2}'.join(k)
                    else:
                        rx_repl = k
                    b_chap.text = re.sub(rx_repl, v, b_chap.text, flags=re.I)
                    b_chap.save()
        print(result)
        return result

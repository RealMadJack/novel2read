import logging
import re

from django.conf import settings
from django.utils.text import slugify
from datetime import datetime
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.remote.remote_connection import LOGGER

from .models import Book, BookChapter, BookTag
from .utils import download_img, multiple_replace

# Logging restrictions
# LOGGER.setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


class BookScraper:
    def __init__(self):
        logging.info(f'Creating instance: {self.__class__.__name__}')
        self.url_bb = {
            'webnovel': 'https://www.webnovel.com/book/',
            'boxnovel': 'https://boxnovel.com/novel/',
            'wuxiaworld': 'https://www.wuxiaworld.com/novel/',
            'gravitytails': 'https://gravitytales.com/novel/',
            'lnmtl': 'https://lnmtl.com/novel/',
        }
        self.to_repl = {
            '<p>': '', '</p>': '',
            '  ': '',
            '\n': '',
            '‽': '?!',
            '&#13;': '',
            '*': '',
            '<script>': '', '</script>': '',
            '<?php': '',
        }

    def raw_html_text_filter(self, html_text):
        html_node_3 = ''.join([html_node.text for html_node in html_text[0:3]])
        if html_text[0].text[:100] == html_node_3[:100]:
            del html_text[0]
        if len(html_text[0].text) >= 2000:
            del html_text[0]

        filtered_html_text = []
        for i, text_node in enumerate(html_text):
            text_node = text_node.html
            node = multiple_replace(self.to_repl, text_node)

            if i <= 5:
                if node.lower().startswith('chapter'):
                    node = ''
                if 'translator' and 'editor' in node.lower():
                    node = ''
                if '<ol' in node.lower():
                    node = ''

            if len(node):
                node = f'<p>{node}</p>'
                filtered_html_text.append(node)

        return filtered_html_text

    def get_filter_db_books(self, qs, revisit=False):
        if revisit:
            books = qs.filter(visited=True).exclude(revisit_id__exact='')
        else:
            books = qs.filter(visited=False).exclude(visit_id__exact='')
        return books

    def create_book_tag(self, name):
        slug_name = slugify(name)
        tag = BookTag.objects.filter(slug=slug_name).exists()
        if not tag:
            logging.info(f'-- Creating tag: {name}')
            booktag = BookTag.objects.create(name=name)
            return booktag
        return False

    def add_book_booktag(self, book, tag_name):
        try:
            booktag = BookTag.objects.get(slug=slugify(tag_name))
            if booktag not in book.booktag.all():
                logging.info(f'-- Adding: {tag_name}')
                book.booktag.add(booktag)
                return True
            return False
        except (BookTag.DoesNotExist, Book.DoesNotExist) as e:
            raise e

    def update_db_book_data(self, book, data):
        print(f'Updating book: {book}')
        data = data[0] if isinstance(data, list) else data
        book.title = data['book_name']
        book.title_sm = data['book_name_sm']
        book.author.append(data['book_info_author']) if data['book_info_author'] not in book.author else False
        book.description = data['book_desc']
        poster_filename = download_img(data['book_poster_url'], slugify(data['book_name']))
        book.poster = f'posters/{poster_filename}'
        book.rating = data['book_rating']
        if data['chap_release'] == 'completed':
            book.status_release = 1
        elif isinstance(data['chap_release'], int):
            book.chapters_release = data['chap_release']
        for tag in data['book_tag_list']:
            self.create_book_tag(tag)
            self.add_book_booktag(book, tag)
        book.visited = True
        # book.save()  # prevent celery post_save closure

    def create_book_chapter(self, book, c_title, c_content):
        print(f'Creating: {c_title}')
        bookchapter = BookChapter.objects.create(book=book, title=c_title, text=c_content)
        return bookchapter

    def wn_get_book_data(self, book_url):
        session = HTMLSession()
        r = session.get(book_url)
        book_name_raw = r.html.find('.pt4.pb4.oh.mb4')[0].text
        book_name = ' '.join(book_name_raw.split(' ')[0:-1]).replace('‽', '?!')
        book_name_sm = book_name_raw.split(' ')[-1]
        chap_release_raw = r.html.find('.det-hd-detail strong')[0].text
        chap_release = chap_release_raw.lower().strip() if len(chap_release_raw) < 20 else int(re.findall('\d+', chap_release_raw)[0])
        book_info_chap_count_raw = r.html.find('.det-hd-detail strong')[1].text
        book_info_chap_count = int(re.findall('\d+', book_info_chap_count_raw)[0])
        book_info_author = r.html.find('.ell.dib.vam span')[0].text
        book_rating = float(r.html.find('._score.ell strong')[0].text)
        book_poster_url = ''.join(r.html.find('i.g_thumb img')[1].attrs['srcset'].split(' '))
        book_desc_raw = r.html.find('p.mb48.fs16.c_000')[0].html.split('<br/>')
        book_desc_raw = ['' if 'webnovel' in p.lower() else p for p in book_desc_raw]
        book_desc_raw = [multiple_replace(self.to_repl, p.strip()) for p in book_desc_raw]
        book_desc = ''.join([f"<p>{re.sub(r'<.*?>', '', text)}</p>" for text in book_desc_raw]).replace('<p></p>', '')
        book_tag_list = [a.text.strip() for a in r.html.find('.pop-tags a')]

        book = []
        book.append({
            'book_name': book_name,
            'book_name_sm': book_name_sm,
            'chap_release': chap_release,
            'book_info_chap_count': book_info_chap_count,
            'book_info_author': book_info_author,
            'book_rating': book_rating,
            'book_poster_url': book_poster_url,
            'book_desc': book_desc,
            'book_tag_list': book_tag_list,
        })
        return book

    def wn_get_book_cids(self, book_url, s_from=0, s_to=0):
        driver_opts = webdriver.ChromeOptions()
        driver_opts.add_argument('headless')
        driver_opts.add_argument('disable-gpu')
        driver_opts.add_argument('log-level=3')
        driver_opts.add_argument('silent')

        driver = webdriver.Chrome(chrome_options=driver_opts)
        wait = WebDriverWait(driver, 5)
        driver.get(book_url)
        # DOM
        driver.find_element_by_css_selector('a.j_show_contents').click()
        if s_to:
            c_list = wait.until(lambda driver: driver.find_elements_by_css_selector('.content-list li')[s_from:s_to])
        else:
            c_list = wait.until(lambda driver: driver.find_elements_by_css_selector('.content-list li'))
        c_ids = [li.get_attribute("data-cid") for li in c_list]
        driver.close()
        return c_ids

    def wn_get_book_chap(self, wn_chap_url):
        session = HTMLSession()
        r_chap = session.get(wn_chap_url)
        print(wn_chap_url)
        chap_tit_raw = r_chap.html.find('.cha-tit h3')[0].text
        chap_lock = r_chap.html.find('.cha-content._lock')

        if len(chap_lock) == 0:
            chap_tit = re.split(r':|-|–', chap_tit_raw, maxsplit=1)[1].strip().replace('‽', '?!')
            chap_tit_id = int(re.findall('\d+', chap_tit_raw)[0])

            chap_content_raw = r_chap.html.find('.cha-words p')
            chap_content_filtered = self.raw_html_text_filter(chap_content_raw)
            b_chap = {
                'c_id': chap_tit_id,
                'c_title': chap_tit,
                'c_content': ''.join(chap_content_filtered),
            }
            return b_chap
        return chap_tit_raw

    def wn_get_update_book_chaps(self, book, book_url, c_ids):
        for c_id in c_ids[book.chapters_count:]:
            bn_chap_url = f'{book_url}/{c_id}'
            b_chap = self.wn_get_book_chap(bn_chap_url)
            if isinstance(b_chap, dict):
                self.create_book_chapter(book, b_chap['c_title'], b_chap['c_content'])
            else:
                break
        b_chap = b_chap['c_title'] if isinstance(b_chap, dict) else b_chap
        b_chap_info = {
            'Source': 'webnovel',
            'locked_ended_from': b_chap,
        }
        return b_chap_info

    def bn_get_book_chap(self, bn_chap_url):
        session = HTMLSession()
        r_chap = session.get(bn_chap_url)
        try:
            chap_tit_raw = r_chap.html.find('.reading-content h3')[0].text
        except IndexError:
            chap_tit_raw = r_chap.html.find('.reading-content p')[0].text
        chap_tit = re.split(r':|-|–', chap_tit_raw, maxsplit=1)[1].replace('‽', '?!').strip()
        chap_tit_id = int(re.findall('\d+', chap_tit_raw)[0])
        chap_content_raw = r_chap.html.find('.reading-content p')
        chap_content_filtered = self.raw_html_text_filter(chap_content_raw)

        b_chap = {
            'c_id': chap_tit_id,
            'c_title': chap_tit,
            'c_content': ''.join(chap_content_filtered),
        }
        return b_chap

    def bn_get_update_book_chaps(self, book, book_url, s_to=0):
        s_to = s_to + 1 if s_to else s_to
        b_chaps_len = book.chapters_count
        c_ids = list(range(b_chaps_len + 1, s_to)) if s_to else False
        print(c_ids)

        if s_to:
            for c_id in c_ids:
                bn_chap_url = f'{book_url}/chapter-{c_id}'
                b_chap = self.bn_get_book_chap(bn_chap_url)
                self.create_book_chapter(book, b_chap['c_title'], b_chap['c_content'])
            b_chap_info = {
                'updated': len(c_ids),
                'last': f'{book_url}/chapter-{c_ids[-1]}',
            }
            return b_chap_info
        else:
            b_chaps_upd = 0
            while True:
                b_chaps_len += 1
                b_chaps_upd += 1
                bn_chap_url = f'{book_url}/chapter-{b_chaps_len}'
                try:
                    b_chap = self.bn_get_book_chap(bn_chap_url)
                    self.create_book_chapter(book, b_chap['c_title'], b_chap['c_content'])
                except IndexError as e:
                    b_chap_info = {
                        'updated': b_chaps_upd,
                        'last': bn_chap_url,
                    }
                    break
            return b_chap_info


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(name)-24s: %(levelname)-8s %(message)s')
    start = datetime.now()

    scraper = BookScraper()
    scraper.run()

    finish = datetime.now() - start
    logging.info(f'Done in: {finish}')


if __name__ == '__main__':
    main()

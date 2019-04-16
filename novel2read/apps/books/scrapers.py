import logging
import re
import pprint
import sys
import os
import django

from django.utils.text import slugify
from datetime import datetime
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.remote_connection import LOGGER

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__name__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    django.setup()

from .models import Book, BookChapter, BookTag
from .utils import multiple_replace

# Logging restrictions
LOGGER.setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


class BookScraper:
    def __init__(self):
        logging.info(f'Creating instance: {self.__class__.__name__}')
        self.wn_bb = 'https://www.webnovel.com/book/'
        self.bn_bb = 'https://boxnovel.com/novel/'
        self.ww_bb = 'https://www.wuxiaworld.com/novel/'
        self.gt_bb = 'https://gravitytales.com/novel/'
        self.lnmtl_bb = 'https://lnmtl.com/novel/'
        self.to_repl = {
            '<p>': '', '</p>': '', '  ': '', '\n': '',
            '‽': '?', '&#13;': '', '*': '',
            '<script>': '', '</script>': '', '<?php': '',
        }

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

    def create_book_chapter(self, book, c_title, c_content):
        bookchapter = BookChapter.objects.create(book=book, title=c_title, text=c_content)
        return bookchapter

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

    def wn_get_book_data(self, book_url):
        session = HTMLSession()
        r = session.get(book_url)
        book_name_raw = r.html.find('.pt4.pb4.oh.mb4')[0].text
        book_name = ' '.join(book_name_raw.split(' ')[0:-1])
        book_name_sm = book_name_raw.split(' ')[-1]
        chap_release_raw = r.html.find('.det-hd-detail strong')[0].text
        chap_release = chap_release_raw.lower().strip() if len(chap_release_raw) < 20 else int(re.findall('\d+', chap_release_raw)[0])
        book_info_chap_count_raw = r.html.find('.det-hd-detail strong')[1].text
        book_info_chap_count = int(re.findall('\d+', book_info_chap_count_raw)[0])
        book_info_author = r.html.find('.ell.dib.vam span')[0].text
        book_rating = float(r.html.find('._score.ell strong')[0].text)
        book_poster_url = ''.join(r.html.find('i.g_thumb img')[1].attrs['srcset'].split(' '))
        book_desc_raw = r.html.find('p.mb48.fs16.c_000')[0].html.split('<br/>')
        book_desc_raw = [multiple_replace(self.to_repl, p.strip()) for p in book_desc_raw]
        book_desc = ''.join([f"<p>{re.sub(r'<.*?>', '', text)}</p>" for text in book_desc_raw])
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

    def wn_get_book_chaps(self, book_url, c_ids):
        session = HTMLSession()
        c_ids_len = len(c_ids)
        c_unlocked = 0
        book = []

        for c_id in c_ids:
            wn_chap = f'{book_url}/{c_id}'
            print(wn_chap)
            r_chap = session.get(wn_chap)
            chap_tit_raw = r_chap.html.find('.cha-tit h3')[0].text
            chap_lock = r_chap.html.find('.cha-content._lock')

            if len(chap_lock) == 0:
                chap_tit = re.split(r':|-|–', chap_tit_raw, maxsplit=1)[1].strip()
                chap_tit_id = int(re.findall('\d+', chap_tit_raw)[0])

                logging.info(f'Unlocked: {chap_tit}')

                chap_content_raw = r_chap.html.find('.cha-words p')
                chap_content = []
                for chap_p in chap_content_raw:
                    chap = chap_p.html
                    chap = multiple_replace(self.to_repl, chap)
                    if len(chap):
                        chap = f'<p>{chap}</p>'
                        chap_content.append(chap)

                book.append({
                    'c_id': chap_tit_id,
                    'c_title': chap_tit,
                    'c_content': ''.join(chap_content),
                })
                c_unlocked += 1
                continue
            else:
                break

        # Stats
        c_locked = c_ids_len - c_unlocked
        logging.info(f'Unlocked: {c_unlocked}, Locked: {c_locked}, Locked from: {chap_tit_raw}')
        book.append({
            'unlocked': c_unlocked,
            'locked': c_locked,
            'locked_from': chap_tit_raw,
            'locked_from_id': int(re.findall('\d+', chap_tit_raw)[0]),
        })

        return book

    def update_db_book_data(self, book, data):
        logging.info(f'Updating book: {book}')
        data = data[0] if isinstance(data, list) else data
        book.title = data['book_name']
        book.title_sm = data['book_name_sm']
        book.author.append(data['book_info_author']) if data['book_info_author'] not in book.author else False
        book.description = data['book_desc']
        book.poster_url = data['book_poster_url']
        book.rating = data['book_rating']
        if data['chap_release'] == 'completed':
            book.status_release = 1
        elif isinstance(data['chap_release'], int):
            book.chapters_release = data['chap_release']
        for tag in data['book_tag_list']:
            self.create_book_tag(tag)
            self.add_book_booktag(book, tag)
        book.save()

    def create_update_db_book_chaps(self, book, bookchaps):
        """
        TODO: check book chapter uniq (check last chap c_id)
        """
        if isinstance(bookchaps, list) and len(bookchaps) > 0:
            for chap in bookchaps[0:-1]:
                self.create_book_chapter(book, chap['c_title'], chap['c_content'])
        else:
            raise Exception("You didn't provide chapter list")

    def bn_get_book_chaps(self, book, book_url, s_from=0, s_to=0):
        b_chaps = book.bookchapters.all()
        b_chaps_len = b_chaps.count()
        b_chaps_len = b_chaps_len + s_from if s_from else b_chaps_len
        session = HTMLSession()
        b_chap_list = []

        while True:
            b_chaps_len += 1
            bn_chap_url = f'{book_url}/chapter-{b_chaps_len}'
            print(bn_chap_url)
            try:
                r_chap = session.get(bn_chap_url)
                chap_tit_raw = r_chap.html.find('.reading-content h3')[0].text
                chap_tit = re.split(r':|-|–', chap_tit_raw, maxsplit=1)[1].strip()
                chap_tit_id = int(re.findall('\d+', chap_tit_raw)[0])

                chap_content_raw = r_chap.html.find('.reading-content p')
                chap_content_raw = chap_content_raw[1:] if 'translator' in chap_content_raw[0].text.lower() else chap_content_raw
                chap_content = []
                for chap_p in chap_content_raw:
                    chap = chap_p.html
                    chap = multiple_replace(self.to_repl, chap)
                    if len(chap):
                        chap = f'<p>{chap}</p>'
                        chap_content.append(chap)

                b_chap_list.append({
                    'c_id': chap_tit_id,
                    'c_title': chap_tit,
                    'c_content': ''.join(chap_content),
                })
            except IndexError as e:
                # print(f'Book has: {b_chaps_len - 1} chapters')
                b_chap_list.append({
                    'updated': b_chaps_len - 1,
                    'last': bn_chap_url,
                })
                break
        return b_chap_list

    def substitute_db_book_info(self, qs):
        """
        TODO: different f_books for bn & wn and loops
        wn_visited=True
        bn_visited=False, bool(book.id_bn)
        bn_visited = celery task daily
        check book last c_id => visit book_url/c_id+1
        """
        f_books_wn = self.get_filter_db_books(qs, wn=True)
        f_books_bn = self.get_filter_db_books(qs, bn=True)

        for book in f_books_wn:
            if not book.visited_wn and bool(book.id_wn):
                book_url = f'{self.wn_bb}{book.id_wn}/'

                # Book index page data with static request
                book_data = self.wn_get_book_data(book_url)
                self.update_db_book_data(book, book_data)
                # Book chapters data, c_ids with js request
                c_ids = self.wn_get_book_cids(book_url)
                bookchaps = self.wn_get_book_chaps(book_url, c_ids)
                self.create_update_db_book_chaps(book, bookchaps)

                # Book update
                book.visited_wn = True
                book.save()

        for book in f_books_bn:
            if not book.visited_bn and bool(book.id_bn):
                book_url = f'{self.bn_bb}{book.id_bn}/'
                # Book chapters data, c_ids with js request
                bookchaps = self.bn_get_book_chaps(book, book_url)
                self.create_update_db_book_chaps(book, bookchaps)

                # Book update
                book.visited_bn = True
                book.save()

    def run(self):
        self.substitute_db_book_info()


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(name)-24s: %(levelname)-8s %(message)s')
    start = datetime.now()

    scraper = BookScraper()
    scraper.run()

    finish = datetime.now() - start
    logging.info(f'Done in: {finish}')


if __name__ == '__main__':
    main()

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

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__name__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from .models import Book, BookChapter, BookTag
from .utils import multiple_replace

# Logging restrictions
LOGGER.setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


class BookScraper:
    """
    scrap priority - webnovels
    """

    def __init__(self):
        logging.info(f'Creating instance: {self.__class__.__name__}')
        self.wn_bb = 'https://www.webnovel.com/book/'
        self.bn_bb = 'https://boxnovel.com/novel/'

    def get_filter_db_books(self, bn=False, wn=False):
        if wn:
            books = Book.objects.filter(visited_wn=False)
        elif bn:
            books = Book.objects.filter(visited_bn=False)
        else:
            books = Book.objects.filter(visited_wn=False)
        return books

    def create_book_tag(self, name):
        slug_name = slugify(name)
        tag = BookTag.objects.filter(slug=slug_name).exists()
        if not tag:
            logging.info(f'-- Creating: {name}')
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
        bookchapter = BookChapter.objects.create(
            book=book, title=c_title, text=c_content)
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
        book_info_genre = r.html.find('.det-hd-detail a')[0].text
        chap_release_raw = r.html.find('.det-hd-detail strong')[0].text
        chap_release = chap_release_raw.lower().strip() if len(chap_release_raw) < 20 else int(re.findall('\d+', chap_release_raw)[0])
        book_info_chap_count_raw = r.html.find('.det-hd-detail strong')[1].text
        book_info_chap_count = int(re.findall('\d+', book_info_chap_count_raw)[0])
        book_info_author = r.html.find('.ell.dib.vam span')[0].text
        book_rating = float(r.html.find('._score.ell strong')[0].text)
        book_poster_url = ''.join(r.html.find('i.g_thumb img')[1].attrs['srcset'].split(' '))
        book_desc_raw = r.html.find('p.mb48.fs16.c_000')[0].html.split('<br/>')
        book_desc_raw = [p.replace('&#13;', '').strip() for p in book_desc_raw]
        book_desc = ''.join([f"<p>{re.sub(r'<.*?>', '', p)}</p>" for p in book_desc_raw])
        book_tag_list = [a.text.strip() for a in r.html.find('.pop-tags a')]

        book = []
        book.append({
            'book_name': book_name,
            'book_name_sm': book_name_sm,
            'book_info_genre': book_info_genre,
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

                to_repl = {'<p>': '', '</p>': '', '  ': '', '\n': ''}
                chap_content_raw = r_chap.html.find('.cha-words p')
                chap_content = []
                for chap_p in chap_content_raw:
                    chap = chap_p.html
                    chap = multiple_replace(to_repl, chap)
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
        TODO: check book chapters uniqeness (check last chap c_id)
        """
        if isinstance(bookchaps, list) and len(bookchaps) > 0:
            for chap in bookchaps[0:-1]:
                self.create_book_chapter(book, chap['c_title'], chap['c_content'])
        else:
            raise Exception("You didn't provide chapter list")

    def bn_get_book_chaps(self, book, book_url, s_from=0, s_to=0):
        """
        wn_visited=True
        bn_visited=False, bool(book.book_id_bn)
        bn_visited = celery task daily
        check book last c_id => visit book_url/c_id+1
        """
        pass

    def substitute_db_book_info(self):
        """
        TODO: different f_books for bn & wn and loops
        """
        f_books_wn = self.get_filter_db_books(wn=True)
        # f_books_bn = self.get_filter_db_books(bn=True)

        for book in f_books_wn:
            if not book.visited_wn and bool(book.book_id_wn):
                wn_url = f'{self.wn_bb}{book.book_id_wn}/'

                # Book index page data with static request
                book_data = self.wn_get_book_data(wn_url)
                self.update_db_book_data(book, book_data)
                # Book chapters data, c_ids with js request
                c_ids = self.wn_get_book_cids(wn_url)
                bookchaps = self.wn_get_book_chaps(wn_url, c_ids)
                self.create_update_db_book_chaps(book, bookchaps)

                # Book update
                book.visited_wn = True
                book.save()

    def run(self):
        self.substitute_db_book_info()


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(name)-24s: %(levelname)-8s %(message)s')
    start = datetime.now()

    box_scraper = BookScraper()
    box_scraper.run()

    finish = datetime.now() - start
    logging.info(f'Done in: {finish}')


if __name__ == '__main__':
    main()

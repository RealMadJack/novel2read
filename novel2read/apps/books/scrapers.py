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

    def get_filter_db_books(self):
        books = Book.objects.filter(visited_wn=False)
        return books

    def create_new_tag(self, name):
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
        logging.info(f'Adding: {c_title}')
        bookchapter = BookChapter.objects.create(
            book=book, title=c_title, text=c_content)
        return bookchapter

    def request_bn_book(self, book_id):
        # resp = requests.get(self.bn_link)
        # soup = BeautifulSoup(resp.content, self.parser)
        # post_content = soup.select('.summary_content .post-content')
        # authors_dirty = soup.select('.author-content a')
        # authors = [author.text for author in authors_dirty]

        # resp_chap = requests.get(bn_link_fc)
        # soup_chap = BeautifulSoup(resp_chap.content, self.parser)
        # chap_parag_list = soup_chap.select('.reading-content p')[:5]
        # chap_title = chap_parag_list[0].text.split(' – ')  # re = chapter + :- + int

        # if visited_wn:
            # something with chapter boxnovel and missing book info
        pass

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
        # book_info_chap_count_raw = r.html.find('.det-hd-detail strong')[1].text
        # book_info_chap_count = int(re.findall('\d+', book_info_chap_count_raw)[0])
        book_info_author = r.html.find('.ell.dib.vam span')[0].text
        book_rating = float(r.html.find('._score.ell strong')[0].text)
        book_poster_url = ''.join(r.html.find('i.g_thumb img')[1].attrs['srcset'].split(' '))
        book_desc_raw = r.html.find('p.mb48.fs16.c_000')[0].html.split('<br/>')
        book_desc = ''.join([f"<p>{re.sub(r'<.*?>', '', p)}</p>" for p in book_desc_raw])
        book_tag_list = [a.text.strip() for a in r.html.find('.pop-tags a')]

        book = []
        book.append({
            'book_name': book_name,
            'book_name_sm': book_name_sm,
            'book_info_genre': book_info_genre,
            'chap_release': chap_release,
            # 'book_info_chap_count': book_info_chap_count,
            'book_info_author': book_info_author,
            'book_rating': book_rating,
            'book_poster_url': book_poster_url,
            'book_desc': book_desc,
            'book_tag_list': book_tag_list,
        })
        return book

    def wn_book_get_chaps(self, book_url):
        pass

    def wn_get_book(self, book_id):
        wn_book = f'{self.wn_bb}{book_id}'
        c_ids = self.wn_get_book_cids(wn_book)
        c_ids_len = len(c_ids)
        c_unlocked = 0

        for c_id in c_ids:
            wn_chap = f'{wn_book}/{c_id}'
            r_chap = session.get(wn_chap)
            chap_tit_raw = r_chap.html.find('.cha-tit h3')[0].text

            chap_lock = r_chap.html.find('.cha-content._lock')
            if len(chap_lock) == 0:
                chap_tit = re.split(r':|-|–', chap_tit_raw, maxsplit=1)[1].strip()
                chap_tit_id = int(re.findall('\d+', chap_tit_raw)[0])

                logging.info(f'Unlocked: {chap_tit}')

                chap_content_raw = r_chap.html.find('.cha-words p')[1:]
                chap_content = [
                    chap.html.replace('<p></p>', '').replace('  ', '').replace('\n', '') for chap in chap_content_raw]

                book.append({
                    'c_id': chap_tit_id,
                    'c_tit': chap_tit,
                    'c_content': ''.join(chap_content),
                })
                c_unlocked += 1
                continue
            else:
                break

        c_locked = c_ids_len - c_unlocked
        logging.info(f'Unlocked: {c_unlocked}, Locked: {c_locked}, Locked from: {chap_tit_raw}')
        book.append({
            'book_name': book_name,
            'unlocked': c_unlocked,
            'locked': c_locked,
            'locked_from': chap_tit_raw,
            'locked_from_id': int(re.findall('\d+', chap_tit_raw)[0]),
        })

        return book

    def substitute_db_book_info(self):
        filtered_books = self.get_filter_db_books()

        for book in filtered_books:
            logging.info(f'Trying: {book}')
            if not book.visited_wn and bool(book.book_id_wn):
                book_data = self.wn_get_book(book.book_id_wn)

                book.author.append(book_data[0]['book_info_author']) if book_data[0]['book_info_author'] not in book.author else False
                # book.chapters_max = book_data[0]['book_info_chap_count']
                book.description = book_data[0]['book_desc']
                book.title = book_data[0]['book_name']
                book.title_sm = book_data[0]['book_name_sm']
                book.poster_url = book_data[0]['book_poster_url']
                book.rating = book_data[0]['book_rating']

                if book_data[0]['chap_release'] == 'completed':
                    book.status_release = 1
                elif isinstance(book_data[0]['chap_release'], int):
                    book.chapters_release = book_data[0]['chap_release']

                for tag in book_data[0]['book_tag_list']:
                    self.create_new_tag(tag)
                    self.add_book_booktag(book, tag)

                for chap in book_data[1:-1]:
                    # check if chap exists and update
                    self.create_book_chapter(book, chap['c_tit'], chap['c_content'])
                book.locked_wn = book_data[-1]['locked_from_id']

                logging.info(f'Saving book: {book}')
                book.status = 1 if not book.status else book.status
                book.visited_wn = True
                # pprint.pprint(book_data)
                book.save()

    def check_new_chaps(self):
        pass

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

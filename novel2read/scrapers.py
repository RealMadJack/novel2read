import logging
import re
import pprint
import inspect

from datetime import datetime
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


class BoxNovelScraper:
    """
    scrap priority - webnovels
    steal comments?
    """

    def __init__(self):
        logging.info(f'Creating instance: {self.__class__.__name__}')
        self.wn_bb = 'https://www.webnovel.com/book/'
        self.bn_bb = 'https://boxnovel.com/novel/'

    def get_filter_db_books(self):
        logging.info(f'Calling {inspect.stack()[0][3]} module')
        pass

    def request_external_site(self, book_id='8360425206000005'):
        """
        we take: chap-release, votes_external
        """
        wn_book = f'{self.wn_bb}{book_id}'

        """ JS Search """
        # driver_opts = webdriver.ChromeOptions()
        # driver_opts.add_argument('headless')
        # driver_opts.add_argument('disable-gpu')
        # driver_opts.add_argument('log-level=3')
        # driver_opts.add_argument('silent')

        # driver = webdriver.Chrome(chrome_options=driver_opts)
        # driver.get(wn_book)
        # wait = WebDriverWait(driver, 10)

        # driver.find_element_by_css_selector('a.j_show_contents').click()
        # c_list = wait.until(lambda driver: driver.find_elements_by_css_selector('.content-list li'))
        # c_ids = [li.get_attribute("data-cid") for li in c_list]
        c_ids = ['22522773419115905', '22525235509118345', '23637702117217714', '23577341972235183']
        c_ids_len = len(c_ids)

        # driver.close()
        """ NOJS Search """
        session = HTMLSession()
        r = session.get(wn_book)
        book_name_raw = r.html.find('.pt4.pb4.oh.mb4')[0].text
        book_name = ' '.join(book_name_raw.split(' ')[0:-1])
        book_name_sm = book_name_raw.split(' ')[-1]
        book_info_genre = r.html.find('.det-hd-detail a')[0].text
        book_info_status_release = r.html.find('.det-hd-detail strong')[1].text  # re string
        book_info_author = r.html.find('.ell.dib.vam span')[0].text
        book_poster_url = r.html.find('i.g_thumb img')[1].attrs['srcset']
        book_desc = r.html.find('p.mb48.fs16.c_000')[0].text
        book_tag_list = [a.text for a in r.html.find('.pop-tags a')]  # filter by tag

        book = []
        book.append({
            'book_name': book_name,
            'book_name_sm': book_name_sm,
            'book_info_genre': book_info_genre,
            'book_info_status_release': book_info_status_release,
            'book_info_author': book_info_author,
            'book_poster_url': book_poster_url,
            'book_desc': book_desc,
            'book_tag_list': book_tag_list,
        })

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

                chap_content_raw = r_chap.html.find('.cha-words p')[1:-2]
                chap_content = [
                    chap.html.replace('  ', '').replace('\n', '') for chap in chap_content_raw]

                book.append({
                    'c_id': chap_tit_id,
                    'c_tit': chap_tit,
                    'c_content': chap_content,
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

        pprint.pprint(book)
        return book

        # resp_wn_chap = requests.get(self.wn_link_chap)
        # soup_wn_chap = BeautifulSoup(resp_wn_chap.content, self.parser)
        # wn_chaps = soup_wn_chap.select('.cha-content .cha-words p')[:5]
        # print([chap.text for chap in wn_chaps])

        # resp = requests.get(self.bn_link)
        # soup = BeautifulSoup(resp.content, self.parser)
        # post_content = soup.select('.summary_content .post-content')
        # authors_dirty = soup.select('.author-content a')
        # authors = [author.text for author in authors_dirty]

        # resp_chap = requests.get(bn_link_fc)
        # soup_chap = BeautifulSoup(resp_chap.content, self.parser)
        # chap_parag_list = soup_chap.select('.reading-content p')[:5]
        # chap_title = chap_parag_list[0].text.split(' – ')  # re = chapter + :- + int

    def substitute_db_book_info(self):
        pass

    def run(self):
        self.request_external_site()


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(name)-24s: %(levelname)-8s %(message)s')
    start = datetime.now()

    box_scraper = BoxNovelScraper()
    box_scraper.run()

    finish = datetime.now() - start
    logging.info(f'Done in: {finish}')


if __name__ == '__main__':
    main()

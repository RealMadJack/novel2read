import logging
import inspect
import requests

from datetime import datetime
from bs4 import BeautifulSoup


class BoxNovelScraper:
    """
    scrap priority - webnovels
    steal comments?
    """

    def __init__(self):
        logging.info(f'Creating instance: {self.__class__.__name__}')
        self.parser = 'html.parser'
        self.box_link = 'https://boxnovel.com/novel/reverend-insanity/'
        self.box_link_first_chap = '/chapter-1/'
        self.wn_link = "https://www.webnovel.com/book/7736629105000905/The-Devil's-Cage"
        self.wn_link_chap = "https://www.webnovel.com/book/7931338406001705/21417334738767436/"

    def get_filter_db_books(self):
        logging.info(f'Calling {inspect.stack()[0][3]} module')
        pass

    def request_external_site(self, book_link=''):
        """
        we take: img, author, descr, type, status, chap-release
        we do: boxnovel exclusion
        """
        logging.info(f'Calling {inspect.stack()[0][3]} module')
        chapter_link = f'{self.box_link}{self.box_link_first_chap}'

        resp_wn = requests.get(self.wn_link)
        soup_wn = BeautifulSoup(resp_wn.content, self.parser)
        wn_desc = soup_wn.select('p.mb48.fs16.c_000')

        resp_wn_chap = requests.get(self.wn_link_chap)
        soup_wn_chap = BeautifulSoup(resp_wn_chap.content, self.parser)
        wn_chaps = soup_wn_chap.select('.cha-content .cha-words p')[:5]
        print([chap.text for chap in wn_chaps])

        resp = requests.get(self.box_link)
        soup = BeautifulSoup(resp.content, self.parser)
        post_content = soup.select('.summary_content .post-content')
        authors_dirty = soup.select('.author-content a')
        authors = [author.text for author in authors_dirty]

        resp_chap = requests.get(chapter_link)
        soup_chap = BeautifulSoup(resp_chap.content, self.parser)
        chap_parag_list = soup_chap.select('.reading-content p')[:5]
        chap_title = chap_parag_list[0].text.split(' – ')  # re = chapter + :- + int

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

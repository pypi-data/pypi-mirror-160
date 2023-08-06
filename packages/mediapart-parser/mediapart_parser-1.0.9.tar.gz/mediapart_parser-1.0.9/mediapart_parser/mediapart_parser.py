import tempfile

import feedparser
import requests
import time
import os
import pdfkit
from bs4 import BeautifulSoup
from requests import Session
from deprecated import deprecated
from .mediapart_constants import Global, Login


class MediapartParser:
    mediapart_user = ""
    mediapart_pwd = ""

    def __init__(self, user, pwd):
        self.mediapart_user = user
        self.mediapart_pwd = pwd

    def __get_french_rss_entries(self):
        mediapart_parsed_rss = feedparser.parse(
            Global.RSS_FEED_LINK_FRENCH)
        last_articles = mediapart_parsed_rss.entries
        return last_articles

    def __load_article_page(self, url):
        data = {
            Login.CONNECTION_USER_NAME: self.mediapart_user,
            Login.CONNECTION_USER_PASSWORD: self.mediapart_pwd,
            'op': Login.OP_STRING_FRENCH
        }

        s = Session()
        s.post(Login.LOGIN_PAGE_FRENCH, data=data)
        result = s.get(url)
        s.close()
        return result

    def __write_page_content_in_file(self, final_file_path, page):
        f = open(final_file_path, 'wb')
        f.write(page.content)
        f.close()

        while not os.path.exists(final_file_path):
            time.sleep(1)

    @deprecated(version='1.1.0',
                reason="This will call get_last_french_articles_links().")
    def get_last_articles_links(self):
        self.get_last_french_articles_links()

    def get_last_french_articles_links(self):
        """Returns a list containing all articles
        links available from the RSS feed."""

        all_links = []
        last_articles = self.__get_french_rss_entries()
        for article in last_articles:
            for link in article.links:
                all_links.append(link.href)
        return all_links

    def get_last_english_articles_titles(self):
        """Returns a list containing all french articles
        links available from the website main page."""

        page = requests.get(Global.MAIN_PAGE_LINK_ENGLISH,
                            auth=(self.mediapart_user, self.mediapart_pwd))
        soup = BeautifulSoup(page.text, "html.parser")
        articles_raw = soup.find_all("div", {"data-type": "article"})

        titles = []
        max_array_size = 0
        for article_raw in articles_raw:
            # max return titles is 10 to copy the behavior of other methods
            # that use the rss feed
            if max_array_size < 10:
                title_raw = article_raw.find("h3", {"class": "title"})
                titles.append(title_raw.text.strip())
                max_array_size = max_array_size + 1
            else:
                break
        return titles

    def get_last_articles_titles(self):
        """Return a list containing all articles
        titles available from the RSS feed."""

        titles = []
        last_articles = self.__get_french_rss_entries()
        for article in last_articles:
            titles.append(article.title)
        return titles

    def get_last_articles_categories(self):
        """Returns a list containing all articles
        categories available from the RSS feed."""

        categories = []
        last_articles = self.__get_french_rss_entries()
        for article in last_articles:
            categories.append(article.tags[0].term)
        return categories

    def get_article_id(self, article_url):
        """Resolves the article's unique identifier.
        Parameters:
            article_url -- the url of the article
        Returns:
            article's unique identifier
        """
        page = self.__load_article_page(article_url)

        soup = BeautifulSoup(page.text, "html.parser")
        for a in soup.find_all('a', href=True):
            if "/offrir_article/" in a['href']:
                article_id = a['href'].removeprefix("/offrir_article/")
                break

        return article_id

    # def download_article(self, article_id, file_path):
    #     """Resolves the article's PDF url and download it on the disk.
    #     Parameters:
    #         article_id -- the unique identifier of the article
    #         (can be retrieved using get_article_id)
    #         file_path -- the path on the disk where
    #         you want the article to be written
    #
    #     Returns:
    #         None
    #     """
    #
    #     # resolve article pdf complete url
    #     url = Global.PDF_ARTICLE_BASE_URL + str(article_id)
    #
    #     # load the page
    #     page = self.__load_article_page(url)
    #
    #     # finally write page content in a file
    #     self.__write_page_content_in_file(file_path, page)

    def download_article(self, article_url, file_path):
        """Convert article to PDF then download it on the disk.
        Parameters:
            article_url -- the url of the article
            file_path -- output pdf file absolute path
        Returns:
            None
        """
        tests_tmp_folder = tempfile.gettempdir()
        article_tmp_name = "tmp_article.html"

        # load the page
        page = self.__load_article_page(article_url)

        tmp_file_path = tests_tmp_folder + "/" + article_tmp_name
        f = open(tmp_file_path, 'wb')
        f.write(page.content)
        f.close()

        while not os.path.exists(tmp_file_path):
            time.sleep(1)

        pdfkit.from_file(tmp_file_path, file_path, verbose=True, options={"enable-local-file-access": True,
                                                                          'page-size': 'A4', 'margin-top': '0.50in',
                                                                          'margin-right': '0.50in',
                                                                          'margin-bottom': '0.50in',
                                                                          'margin-left': '0.50in', 'encoding': "UTF-8",
                                                                          'no-outline': None})

        while not os.path.exists(file_path):
            time.sleep(1)

        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

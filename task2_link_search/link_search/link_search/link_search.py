"""
Модуль для поиска ссылок по строке поиска или с конкретного сайта.
При поиске по строке поиска используется Yandex.
"""

__author__ = 'Игнатьев И.В.'

import random
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from .constants import YANDEX_SEARCH_PARAMS, DEFAULT_LINK_LIMIT


class LinkSearch:
    """
    Возвращает ссылки на сайты
    """
    def __init__(self, proxies: list = None):
        """
        :param proxies: Список proxy в формате 'login:passsword@host:port'
        """
        self.user_agents = UserAgent()
        self.proxies = proxies

    def get_search_links(self, search_string: str, link_count: int = None or DEFAULT_LINK_LIMIT, deep=False) -> list:
        """
        Возвращает ссылки результатов поиска в Yandex.
        При глубоком поиске также переходит на найденные в поиске сайты и возвращает найденные на них ссылки.
        :param search_string: Строка поиска
        :param link_count: Количество ссылок в результате
        :param deep: Глубокий поиск (переходить на сайты, являющиеся результатом поиска, и искать ссылки на них)
        :return: Ссылки
        """
        if not search_string:
            return []

        search_page = 0
        links = []

        while len(links) < link_count:
            # Получаем одну страницу ссылок от Yandex
            search_links = self.get_site_links(YANDEX_SEARCH_PARAMS['url'].format(search_string, search_page),
                                               link_class=YANDEX_SEARCH_PARAMS['link_class'])

            if not search_links:
                break

            # При глубоком поиске получаем ссылки с найденных сайтов
            if deep:
                for search_link in search_links:
                    links.append(search_link)
                    if len(links) > link_count:
                        break
                    links += self.get_site_links(search_link)
            else:
                links += search_links

            search_page += 1
        return links[:link_count]

    def get_site_links(self, url: str, link_class=None, link_limit=DEFAULT_LINK_LIMIT) -> list:
        """
        Возвращает список ссылок с переданного сайта
        :param url: URL
        :param link_class: CSS-класс, указанный в ссылке
        :param link_limit: Максимальное количество результатов
        :return: Список ссылок
        """
        if not url:
            return []

        # Выбираем произвольные User-Agent и Proxy
        html = None
        user_agent = self.user_agents.random
        proxies = None
        if self.proxies:
            proxy = self.proxies[random.randint(0, len(self.proxies) - 1)]
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}

        headers = {'User-Agent': user_agent}
        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            html = response.text
        except:
            pass

        if not html:
            return []

        links = []
        parsed_url = urlparse(url)
        soup = BeautifulSoup(html, 'lxml')
        for tag in soup.find_all('a', href=True):
            if link_class is not None and link_class not in (tag.get('class') or []):
                continue

            link = tag['href']
            parsed_link = urlparse(link)
            if not (parsed_link.netloc or parsed_link.path):
                continue

            # Относительные ссылки преобразуем к абсолютным
            if not parsed_link.scheme and not parsed_link.netloc:
                link = (f'{parsed_url.scheme}://' if parsed_url.scheme else '') + f'{parsed_url.netloc}/{link}'

            if link[:2] == '//':
                link = link[2:]

            links.append(link)
            if len(links) == link_limit:
                break
        return links

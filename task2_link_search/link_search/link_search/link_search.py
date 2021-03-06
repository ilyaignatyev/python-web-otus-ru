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
        if not search_string or not link_count or link_count < 0 or not isinstance(link_count, int):
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

    @staticmethod
    def prepare_link(link, opener_scheme, opener_netloc):
        """
        Подготавливает ссылку
        :param link: Ссылка
        :param opener_scheme: Scheme сайта-опенеа (для преобразования относительной ссылки в абсолютную)
        :param opener_netloc: Netloc сайта-опенера (для преобразования относительной ссылки в абсолютную)
        :return: Откорректированная валидная ссылка
        """
        parsed_link = urlparse(link)

        if not (parsed_link.netloc or parsed_link.path):
            return None

        # Относительные ссылки преобразуем к абсолютным
        abs_link_created = False
        if not parsed_link.scheme and not parsed_link.netloc:
            abs_link_created = True
            link = (f'{opener_scheme}://' if opener_scheme else '') + f'{opener_netloc}/{link}'

        if link[:2] == '//':
            link = link[2:]

        # Добавляем схему по-умолчанию, если ее нет
        if not parsed_link.scheme and not abs_link_created:
            link = 'http://' + link

        return link

    def get_site_links(self, url: str, link_class=None, link_limit=DEFAULT_LINK_LIMIT) -> list:
        """
        Возвращает список ссылок с переданного сайта
        :param url: URL
        :param link_class: CSS-класс, указанный в ссылке
        :param link_limit: Максимальное количество результатов
        :return: Список ссылок
        """
        if not url or not link_limit or link_limit < 0 or not isinstance(link_limit, int):
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

            link = self.prepare_link(tag['href'], parsed_url.scheme, parsed_url.netloc)
            if not link:
                continue

            links.append(link)
            if len(links) == link_limit:
                break
        return links

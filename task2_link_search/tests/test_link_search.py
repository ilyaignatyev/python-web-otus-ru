"""
Тесты
"""

import pytest
import validators

from link_search.link_search import LinkSearch


@pytest.fixture(scope='module')
def link_search():
    return LinkSearch()


def test_invalid_params(link_search):
    """
    Тест некорректных параметров
    """
    search_links = link_search.get_search_links(None, 5, False)
    assert len(search_links) == 0

    search_links = link_search.get_search_links('', 5, False)
    assert len(search_links) == 0

    search_links = link_search.get_search_links('wiki', None, False)
    assert len(search_links) == 0

    search_links = link_search.get_search_links('wiki', 0, False)
    assert len(search_links) == 0

    search_links = link_search.get_search_links('wiki', -10, False)
    assert len(search_links) == 0

    search_links = link_search.get_search_links('wiki', 5.5, False)
    assert len(search_links) == 0

    site_links = link_search.get_site_links(None, link_limit=5)
    assert len(site_links) == 0

    site_links = link_search.get_site_links('', link_limit=5)
    assert len(site_links) == 0

    site_links = link_search.get_site_links('wiki', link_limit=0)
    assert len(site_links) == 0

    site_links = link_search.get_site_links('wiki', link_limit=None)
    assert len(site_links) == 0

    site_links = link_search.get_site_links('wiki', link_limit=-10)
    assert len(site_links) == 0

    site_links = link_search.get_site_links('wiki', link_limit=5.5)
    assert len(site_links) == 0


def test_prepare_link(link_search):
    """
    Тест проверки и обработки ссылок
    """
    link = link_search.prepare_link('123.html', 'http', 'site.ru')
    assert link == 'http://site.ru/123.html'

    link = link_search.prepare_link('https://site1.ru/123.html', 'http', 'site.ru')
    assert link == 'https://site1.ru/123.html'

    link = link_search.prepare_link('#', 'http', 'site.ru')
    assert link is None

    link = link_search.prepare_link('javascript:', 'http', 'site.ru')
    assert link is None

    link = link_search.prepare_link('123.html?test=1#page1', 'http', 'site.ru')
    assert link == 'http://site.ru/123.html?test=1#page1'

    link = link_search.prepare_link('//en.wikipedia.org', 'http', 'site.ru')
    assert link == 'http://en.wikipedia.org'


def test_search(link_search):
    """
    Тест поиска (обычный + глубокий)
    """
    search_links = link_search.get_search_links('wiki', 5, False)
    assert len(search_links) == 5
    assert len([link for link in search_links if 'wiki' not in link]) == 0
    assert len([1 for link in search_links if validators.url(link)]) == 5

    search_links_deep = link_search.get_search_links('wiki', 5, True)
    assert len(search_links_deep) == 5
    assert set(search_links_deep) != set(search_links)
    assert len([1 for link in search_links_deep if validators.url(link)]) == 5


def test_get_site_links(link_search):
    """
    Тест получения ссылок с конкретного сайта
    """
    site_links = link_search.get_site_links('http://wikipedia.org', link_limit=5)
    assert 'http://en.wikipedia.org/' in site_links
    assert len([1 for link in site_links if validators.url(link)]) == 5

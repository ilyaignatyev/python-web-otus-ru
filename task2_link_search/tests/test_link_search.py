"""
Тесты
"""

import pytest

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


def test_search(link_search):
    """
    Тест поиска
    """
    search_links = link_search.get_search_links('wiki', 5, False)
    assert len(search_links) == 5
    assert len([link for link in search_links if 'wiki' not in link]) == 0


def test_deep_search(link_search):
    """
    Тест глубокого поиска
    """
    search_links = link_search.get_search_links('wiki', 5, True)
    assert len(search_links) == 5
    assert len([link for link in search_links if 'wiki' not in link]) != 0


def test_get_site_links(link_search):
    """
    Тест получения ссылок с конкретного сайта
    """
    site_links = link_search.get_site_links('http://wikipedia.org', link_limit=5)
    assert 'en.wikipedia.org/' in site_links

# LinkSearch
Модуль для поиска ссылок по строке поиска или с конкретного сайта. 
При поиске по строке поиска используется Yandex.

# Зависимости:
    pip install lxml
    pip install beautifulsoup4
    pip install fake-useragent

# Пример:

    from link_search import LinkSearch

    # Строка поиска
    search_string = 'динозавры'
    
    # Количество ссылок, которое нужно вернуть
    link_limit = 15
    
    # Глубокий поиск (если true - поиск ссылок будет производиться также на сайтах из поисковой выдачи)
    deep = True
    
    # Список прокси, при необходимости
    proxies = [
        'fyTkfJ:DrZV8k@217.29.53.102:14195',
        'fyTkfJ:DrZV8k@217.29.53.105:13960'
    ]

    # Поиск ссылок
    link_search = LinkSearch(proxies=proxies)
    
    # Ссылки по строке поиска
    search_links = link_search.get_search_links(search_string, link_limit, deep)

    print(f'Count: {len(search_links)}')
    for url in search_links:
        print(url)
    
    # Ссылки с конкретного сайта
    site_links = link_search.get_site_links('http://wikipedia.org', link_limit=5)

    print(f'Count: {len(site_links)}')
    for url in site_links:
        print(url)
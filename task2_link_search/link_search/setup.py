from setuptools import setup

PACKAGE = 'link_search'

setup(
    name=PACKAGE,
    version= __import__(PACKAGE).__version__,
    packages=[PACKAGE],
    url='',
    license='',
    author='Ilya Ignatyev',
    author_email='ilyaignatyev@gmail.com',
    description='Searches urls on sites',
    install_requires=[
        'lxml==4.4.2',
        'beautifulsoup4==4.8.1',
        'fake-useragent==0.1.11'
    ]
)

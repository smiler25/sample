import asyncio
import random
from abc import abstractclassmethod
from urllib.parse import urlencode, urlparse, parse_qs

import aiohttp
from bs4 import BeautifulSoup


agents = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/36.0.1985.103 YaBrowser/x14.8.1985.9219 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 YaBrowser/6.2.1364.12390 Safari/537.22',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
    'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1',
    'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
)


async def get_content(url, session):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.read()


class SearchEngine:
    engines = []
    key = None
    has_api = False
    cookies = None

    def __init_subclass__(cls, **kwargs):
        SearchEngine.engines.append(cls)

    @classmethod
    async def search_all(cls, search_term, limit):
        return dict(await asyncio.gather(*[asyncio.ensure_future(e().search(search_term, limit))
                                           for e in cls.engines]))

    async def search(self, search_term, limit):
        headers = {'User-Agent': random.choice(agents)}
        url = self.prepare_url(search_term, limit)
        async with aiohttp.ClientSession(headers=headers, cookies=self.cookies) as session:
            content = await get_content(url, session)
        if content:
            res = self.parse_html(content, limit)
            return self.key, {'result': res}
        return self.key, {'error': 'Search unavailable', 'result': []}

    async def search_api(self, search_term, limit):
        return

    async def search_html(self, search_term, limit):
        headers = {'User-Agent': random.choice(agents)}
        url = self.prepare_url(search_term, limit)
        async with aiohttp.ClientSession(headers=headers) as session:
            content = await get_content(url, session)
        if content:
            res = self.parse_html(content, limit)
            return self.key, {'result': res}
        return self.key, {'error': 'Search unavailable', 'result': []}

    @classmethod
    @abstractclassmethod
    def parse_html(cls, content, limit):
        """
        Получение результатов из html поисковой выдачи
        :param content: содержимое страницы
        :return: список ответов
        :param limit: количество результатов
        """

    @classmethod
    @abstractclassmethod
    def prepare_url(cls, search_term, limit):
        pass


class Google(SearchEngine):
    key = 'google'
    # # cookies = {'NID': '136=Tb7LJZLwmBfqL8iB0kg1vOzBCkiltvx31WOYnG2FmXEfVN6P30VHlcnfRDwv0u4g3tkOQ6gUa91nldrL0JCzj6D7AwU1kjuAi8Zmr8v6Z8sIefj0ugPT9TYCn31t1DZW'}
    cookies = {'NID': '136=afypCnUinBCSiu8MZYMfzFas-O2_4vr06swy8sJTgWG77CZ_2etufwZPJXsriDwaqcKCx1lUdtg7zY-qBTc-tk0gm8tNqOnOSwMjgLytblKd_jeew-JPBWFcaZBoAJ0cw8T-NNvIx9Lt'}

    async def search(self, search_term, limit):
        headers = {'User-Agent': random.choice(agents)}
        url = self.prepare_url(search_term, limit)
        async with aiohttp.ClientSession(headers=headers) as session:
            content = await get_content(url, session)
        if content:
            res = self.parse_html(content, limit)
            return self.key, {'result': res}
        return self.key, {'error': 'Search unavailable', 'result': []}

    @classmethod
    def prepare_url(cls, search_term, limit):
        query_str = urlencode({'q': search_term, 'num': limit})
        return 'https://www.google.com/search?{}'.format(query_str)

    @classmethod
    def parse_html(cls, content, limit) -> list:
        soup = BeautifulSoup(content, 'html.parser')
        answers = soup.find_all('div', attrs={'class': 'g'})
        res = []
        if answers:
            for one in answers[:limit]:
                title_elem = one.find('h3', attrs={'class': 'r'})
                link_elem = one.find('a', href=True)
                if link_elem and title_elem:
                    title = title_elem.text
                    link_query = urlparse(link_elem['href']).query
                    if link_query:
                        links = parse_qs(link_query).get('q')
                        if links:
                            link = links[0]
                            res.append({'link': link, 'title': title})
                    else:
                        res.append({'link': link_elem.get('href'), 'title': title})
        return res


class Yandex(SearchEngine):
    key = 'yandex'

    @classmethod
    def prepare_url(cls, search_term, limit):
        query_str = urlencode({'text': search_term, 'numdoc': limit})
        return 'https://yandex.ru/search/?{}'.format(query_str)

    @classmethod
    def parse_html(cls, content, limit) -> list:
        soup = BeautifulSoup(content, 'html.parser')
        answers = soup.find_all('div', attrs={'class': 'organic'})
        if answers:
            res = []
            for one in answers[:limit]:
                link_elem = one.find('a')
                if link_elem:
                    title = link_elem.text
                    link = one.find('a').get('href')
                    if link:
                        res.append({'link': link, 'title': title})
            return res
        return []


def run_search(search_term, limit):
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(SearchEngine.search_all(search_term, limit))
    return res

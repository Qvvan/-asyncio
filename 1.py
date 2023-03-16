import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
import xml.etree.ElementTree as xml


url_list = ['http://crawler-test.com/', 'http://google.com/', 'https://vk.com/', 'https://yandex.ru/', 'https://stackoverflow.com/']


headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729) '
                         'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


async def get_content(session, url):
    async with session.get(url, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), 'lxml')
        items = soup.find_all('a')

        root = xml.Element(url[url.find('/', 2) + 2: url.find('.')])

        for i in items:
            xml.SubElement(root, 'Link').text = i.get('href') if i.get('href').find('http') == 0 else url[:-1] + i.get('href')

        tree = xml.ElementTree(root)
        tree.write(url[url.find('/', 2) + 2: url.find('.')] + '.xml', encoding='UTF-8', xml_declaration=True)


async def get_html():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in url_list:
            task = asyncio.create_task(get_content(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)


t1 = time.time()
asyncio.run(get_html())
print(time.time() - t1)
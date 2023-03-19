import re
import tqdm
import typing
from collections import namedtuple

import requests
from flask import request
from lxml.etree import HTML, _Element

Tag = namedtuple('Tag', ['name', 'id'])
Card = namedtuple('Card', ['name', 'url', 'cover'])


def fetch_html(url: str) -> _Element:
    res = requests.get(
        url, headers={'User-Agent': request.headers['User-Agent']})
    assert res.status_code == 200
    return HTML(res.content.decode('gb2312', 'ignore'))  # type: ignore


def get_tags() -> list[Tag]:
    html = fetch_html('https://www.hh12345.cc/ku/tag/')

    tags: list[Tag] = []
    for item in html.xpath('//div[@class="jigou"]/ul/li'):
        tags.append(Tag(
            name=item.xpath('a/text()')[0],
            id=item.xpath('a/@href')[0].split('/')[-2]
        ))
    return tags


def get_cards(tag: typing.Any, page: typing.Any) -> tuple[str, int, list[Card]]:
    html = fetch_html(
        f'https://www.hh12345.cc/ku/{tag}/list_{tag}_{page}.html')
    name = html.xpath('//*[@id="size"]/div/h2/text()')[0]

    cards: list[Card] = []
    for item in html.xpath('//div[@class="piece"]'):
        cards.append(Card(
            name=item.xpath('h3/a/text()')[0],
            cover=item.xpath('div[@class="cover"]//img/@src')[0],
            url='/images/%s/%s'
            % tuple(item.xpath('div[@class="cover"]/a/@href')[0]
                        .removesuffix('.html')
                        .split('/')[-2:]))
        )
    return name, int(html.xpath('//span[@class="pageinfo"]/strong/text()')[0]), cards


def get_html_images(html: _Element) -> list[str]:
    return html.xpath('//div[@class="content"]/img/@src')


def get_images(tag: typing.Any, card: typing.Any) -> tuple[str, list[str]]:
    html = fetch_html(f'https://www.hh12345.cc/ku/{tag}/{card}.html')
    name = html.xpath('//*[@id="size"]/div/h2/text()')[0]
    count = int(re.findall(r'\d+', html.xpath(
        '//div[@class="page-list"]/ul/a/text()')[0])[0])
    images: list[str] = get_html_images(html)

    for i in tqdm.tqdm(range(2, count + 1)):
        images.extend(get_html_images(fetch_html(
            f'https://www.hh12345.cc/ku/{tag}/{card}_{i}.html')))

    return name, images

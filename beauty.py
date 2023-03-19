import typing
from collections import namedtuple

import requests
from lxml.etree import HTML, _Element
from flask import request

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

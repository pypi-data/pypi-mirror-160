# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/7/8 1:49
# __fileName__ : CrawlSpider splash.py
# __devIDE__ : PyCharm


import asyncio
from CrawlSpider.Utils.SpiderRequest import spiderRequest

async def get(url):
    res = await spiderRequest.get(
        url,
        isSplash=True
    )
    print(res)

if __name__ == '__main__':
    asyncio.run(get("http://httpbin.org/get"))









































































































# -*- coding: utf-8 -*-
import asyncio
import logging
import re
import datetime
from time import time

import aiohttp

from apps.common import ua


class Bilibili(object):

    def __init__(self, bv):
        self.base_url = f'http://www.bilibili.com/video/{bv}'
        self.video_url = 'http://api.bilibili.com/x/v2/reply'  # 设置请求地址
        self.comments = list()
        self.pages = 0
        self.oid = None
        self.bv_title = None
        self.header = {'User-Agent': ua.random}

    async def bv_to_oid(self):
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(self.base_url) as response:
                text = await response.text()
                oid = re.findall(r'https://www.bilibili.com/video/av(.*?)/.*?', text)
                bv_title = re.findall(r'<h1 title="(.*?)".*?</h1>', text)
                oid = oid[0] if oid else None
                return oid, bv_title

    async def get_sum_pages(self):
        video_url_params = {
            'jsonp': 'jsonp',
            'pn': 1,
            'type': 1,
            'oid': self.oid,  # 视频id
            'sort': 2,
        }
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.get(self.video_url, params=video_url_params) as response:
                response = await response.json()
                count = response['data']['page']['count']
                integer = count // 20
                residue = count % 20
                return integer + 1 if residue else integer

    async def get_comments(self, page):
        async with aiohttp.ClientSession(headers=self.header) as session:
            try:
                # 设置GET请求参数
                video_url_params = {
                    'jsonp': 'jsonp',
                    'pn': page,  # 页数从0开始的所以要+1
                    'type': 1,
                    'oid': self.oid,  # 视频id
                    'sort': 2,
                }
                # 获得评论列表
                async with session.get(self.video_url, params=video_url_params) as response:
                    repliesall = await response.json()
                    repliesall = repliesall['data']['replies']
                    for replies in repliesall:
                        pendant = replies['member']['user_sailing']['pendant']
                        user_face = replies['member']['avatar']
                        user_pendant = pendant.get('image', '') if pendant else ''
                        user_name = replies['member']['uname']
                        user_level = replies['member']['level_info']['current_level']
                        date_time = datetime.datetime.fromtimestamp(replies['ctime']).strftime("%Y-%m-%d %H:%M")
                        like = replies['like']
                        # 循环获得次视频下面的评论
                        text = replies['content']['message']
                        emote = replies['content'].get('emote', {})
                        if emote:
                            for k, v in emote.items():
                                text = text.replace(k, f'<img src="{v["url"]}" class="small" alt="{k}">')
                        self.comments.append({
                            'user_face': user_face if not user_face.endswith(
                                'gif') else 'http://i0.hdslb.com/bfs/face/member/noface.jpg',
                            'user_pendant': user_pendant,
                            'user_name': user_name,
                            'user_level': user_level,
                            'date_time': date_time,
                            'like': like,
                            'text': text,
                        })
            except Exception as e:
                logging.debug(e)
                logging.debug(f'==================get complete==================Page:{page}')

    def start_task(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.oid, self.bv_title = loop.run_until_complete(self.bv_to_oid())  # 通过bv获取av
        if not (self.oid or self.bv_title):
            return [], None
        self.pages = loop.run_until_complete(self.get_sum_pages())  # 获取总页数
        task = [self.get_comments(page) for page in range(1, self.pages + 1)]
        loop.run_until_complete(asyncio.wait(task))
        return self.comments, self.bv_title[0]


if __name__ == '__main__':
    s = time()
    b = Bilibili('BV1c5411s7sx')
    c, v = b.start_task()
    print(c)
    print(len(c))
    e = time()
    print(e - s)

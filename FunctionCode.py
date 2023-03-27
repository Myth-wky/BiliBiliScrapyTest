import requests
import time
import random


class ChangeCode(object):
    def dec(self, bv):
        global s, add, xor
        table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr = {}
        for i in range(58):  # bv转av
            tr[table[i]] = i
            s = [11, 10, 3, 8, 4, 6]
            xor = 177451812
            add = 8728348608
        r = 0
        for i in range(6):
            r += tr[bv[s[i]]] * 58 ** i
        return (r - add) ^ xor

    def enc(self, av):  # av-bv
        global xor, add, s
        table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
        tr = {}
        for i in range(58):
            tr[table[i]] = i
            s = [11, 10, 3, 8, 4, 6]
            xor = 177451812
            add = 8728348608
        av = (av ^ xor) + add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]] = table[av // 58 ** i % 58]
        return ''.join(r)
    # print(dec('BV17x411w7KC'))
    # print(dec('BV1Q541167Qg'))
    # print(dec('BV1mK4y1C7Bz'))
    # print(enc(170001))
    # print(enc(455017605))
    # print(enc(882584971))


class Tags(object):
    def __init__(self, aid):
        self.tags_list = []
        self.url = f'https://api.bilibili.com/x/tag/archive/tags?aid={aid}'
        # 若需要再使用 构建headers请求头 把ua伪造头通过random随机选取一个传进去
        # 测试得知Cookies是会影响推送的
        self.headers = {
            'Connection': 'close',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '0',
            'cookie': "Your Cookie",
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44'
        }

    def getTagsJson(self) -> object:  # 返回的是一个字符串，以, 做间隔
        time.sleep(random.uniform(7, 12))  # 延迟访问
        response = requests.get(url=self.url, headers=self.headers).json()
        return response

    def getTags(self) -> object:
        res = self.getTagsJson()
        # print(res['data'])  # test
        for i in res['data']:
            try:
                tag_name = i['tag_name']
                self.tags_list.append(tag_name)
                # print('tag_name:' + str(tag_name))
                # print(self.tags_list)
            except Exception as a:
                print("nothing!")
        print('tags:', end='')
        print(self.tags_list)
        return self.tags_list


class Comments(object):
    def __init__(self, bv):
        self.change_code = ChangeCode()
        av = self.change_code.dec(bv)
        pn = 1
        self.comment_url = f'https://api.bilibili.com/x/v2/reply?type=1&oid={av}&sort=1&pn={pn}'
        self.base_comment_url = f'https://api.bilibili.com/x/v2/reply?type=1&oid={av}&sort=1&pn='  # 方便后面修改Pn
        # 若需要再使用 构建headers请求头 把ua伪造头通过random随机选取一个传进去
        # 测试得知Cookies是会影响推送的
        self.headers = {
            'Connection': 'close',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '0',
            'cookie': "Your Cookie",
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44'
        }

    def getCommentJson(self) -> object:
        time.sleep(random.uniform(8, 12))  # 延迟访问
        response = requests.get(url=self.comment_url, headers=self.headers).json()
        return response

    def getCommentNumber(self):
        global count
        res = self.getCommentJson()
        try:
            count = str(((res['data'])['page'])['acount'])
            print('评论数:' + count)
        except Exception as a:
            print("Comment numbers is Wrong!")
        return count

    def getComment(self) -> object:
        pn = 1
        comment_list = []
        # 使用死循环直到reply为[] or None
        while True:
            time.sleep(random.uniform(8, 12))  # 延迟访问
            url = self.base_comment_url + str(pn)
            res = requests.get(url=url, headers=self.headers).json()
            # print(type(res))  # test
            try:
                if res['data'] is None or (res['data'])['replies'] == [] or (res['data'])['replies'] is None or pn >= 5:
                    print('该视频评论爬取完毕')
                    break
            except Exception as a:
                print("something wrong!")
            for i in (res['data'])['replies']:
                try:
                    comment = str((i['content'])['message'])
                    comment_list.append(comment)
                    # print(comment_list)
                except Exception as a:
                    print("Nothing!")
            pn += 1
        return comment_list

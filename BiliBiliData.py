import random
import time
import requests
import csv
from datetime import datetime

import FunctionCode
from FunctionCode import Tags


class BiliBiliData(object):
    # 定义初始化属性
    def __init__(self, num):
        # 访问的 url ，实现翻页功能在主程序入口， 到时候传参给num就能实现翻页功能
        self.url = f'https://api.bilibili.com/x/web-interface/popular?ps=20&pn={num}'  # num<=25
        # 若需要再使用 构建headers请求头 把ua伪造头通过random随机选取一个传进去
        # 测试得知Cookies是会影响推送的
        self.headers = {
            'Connection': 'close',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'content-length': '0',
            'cookie': "buvid3=2D1018A0-E2F7-0517-C601-D1AE90072E9D39168infoc; b_nut=1679404239; buvid4=72136907-9D5A-6AF7-EF4E-64492E1F4C2839168-023032121-7XDfT9HnZ76pdv5dhaSPnRVW74fij0RhyY+PYlxgGUr1++9bvG67iA==; innersign=0; i-wanna-go-back=-1; b_ut=7; b_lsid=1031E6366_187044B1297; _uuid=B5D495B1-B98A-DE1C-DCF9-5BD18E77BECB41565infoc; header_theme_version=CLOSE; home_feed_column=5; buvid_fp=fb26f5ade3d50acc5001fe7b00038e57",
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


    def getRankUrl(self):
        time.sleep(random.uniform(25, 35))  # 延迟访问
        response = requests.get(url=self.url, headers=self.headers).json()  # 用json数据保存
        # print(response)  # test
        # print(type(response))  # test
        return response  # 返回Json

    def getRankData(self):
        res = self.getRankUrl()
        # aid_list = []  # aid列表，每次函数调用进行储存以及传递到其他函数内使用
        with open(f"./{time_now}.csv", "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # writer.writerow(['aid', '视频分区', '是否原创', '视频标题', '视频简介', 'UP昵称', '视频观看', '视频回复', '视频收藏', '视频投币', '视频分享', '视频点赞', '视频链接', 'IP', 'BV号', '个性化推荐理由', 'Tags'])
            # print(res)  # 测试用
            # 数据是字典形式存在
            # print(res['data'])  # test
            # print(type(res['data']))  # test
            # print(type((res['data'])['list']))  # test
            # res的json中是一个大字典，在大字典里嵌套了个叫做data的小字典，小字典里有一个list列表。里面是更小的字典们

            for i in (res['data'])['list']:
                # 异常处理
                try:
                    aid = i['aid']
                    print('aid:' + str(aid))
                except Exception as a:
                    print("nothing!")
                # 传递到tags对应函数
                try:
                    title_name = i['tname']
                    print('视频分区:' + str(title_name))
                except Exception as a:
                    print("nothing!")
                # 视频分区
                try:
                    copyright = i['copyright']
                    if copyright == 1:
                        copyright = "自制"
                    else:
                        copyright = "转载"
                    print('是否原创:' + str(copyright))
                except Exception as a:
                    print("nothing!")
                # 是否自制，1是自制，2是转载
                try:
                    video_title = i['title']
                    print('视频标题:' + str(video_title))
                except Exception as a:
                    print("nothing!")
                # 视频标题
                try:
                    video_desc = i['desc']
                    print('视频简介:' + str(video_desc))
                except Exception as a:
                    print("nothing!")
                # 视频简介
                # 以下会出现嵌套的字典
                try:
                    owner = i['owner']
                    owner_name = str(owner['name'])
                    print('UP昵称:' + owner_name)
                except Exception as a:
                    print("nothing!")
                # UP昵称
                # 下列是重要视频数据，也是嵌套的字典
                try:
                    video_stat = i['stat']
                    video_views = str(video_stat['view'])
                    video_reply = str(video_stat['reply'])
                    video_favorite = str(video_stat['favorite'])  # 收藏
                    video_coins = str(video_stat['coin'])
                    video_share = str(video_stat['share'])
                    video_like = str(video_stat['like'])
                    print('视频观看:' + video_views + '\n' + '视频回复:' + video_reply + '\n' +
                          '视频收藏:' + video_favorite + '\n' + '视频投币:' + video_coins + '\n' +
                          '视频分享:' + video_share + '\n' + '视频点赞:' + video_like)
                except Exception as a:
                    print("nothing!")
                # 视频信息
                try:
                    video_link = i['short_link']
                    print('视频链接:' + video_link)
                except Exception as a:
                    print("nothing!")
                # 视频链接
                try:
                    location = i['pub_location']
                    print('IP:' + location)
                except Exception as a:
                    print("nothing!")
                # IP地址
                try:
                    bvid = i['bvid']
                    print('BV号:' + bvid)
                except Exception as a:
                    print("nothing!")
                # BV号
                # 下面的个性化comment需要判断是否是None
                try:
                    rcmd_reason = i['rcmd_reason']
                    rcmd_reason_content = ""
                    if rcmd_reason['content'] == "":
                        rcmd_reason_content = "None"
                    else:
                        rcmd_reason_content = rcmd_reason['content']
                    print('个性化推荐理由:' + rcmd_reason_content)
                except Exception as a:
                    print("nothing!")
                # 推荐理由
                # tags相关
                tags = Tags(aid=aid)
                video_tags = tags.getTags()  # 获取到列表，然后写入
                # 处理评论
                comment = FunctionCode.Comments(bvid)
                comment_count = comment.getCommentNumber()
                comment_list = comment.getComment()
                print(comment_list)

                print("____" * 15)  # 分割符
                # 下面是CSV的读写
                csv_list = [str(aid), title_name, copyright, video_title, video_desc, owner_name, video_views,
                            video_reply, video_favorite, video_coins, video_share, video_like, video_link, location,
                            bvid, rcmd_reason_content, video_tags, comment_count, comment_list]
                writer.writerow(csv_list)
        f.close()

    def run(self):
        self.getRankData()


if __name__ == '__main__':
    time_now = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
    start = datetime.now()
    print(start)
    # 循环外初始化写入列名
    with open(f"./{time_now}.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['aid', '视频分区', '是否原创', '视频标题', '视频简介', 'UP昵称', '视频观看', '视频回复', '视频收藏',
             '视频投币', '视频分享', '视频点赞', '视频链接', 'IP', 'BV号', '个性化推荐理由', 'Tags', '评论数',
             '评论详情（列表）'])
    f.close()
    for i in range(1, 26):  # 测试期间将26改成2
        run_test = BiliBiliData(i)
        run_test.run()
        print(f'第{i}页')
    end = datetime.now()
    print('Running time: %s Seconds' % (end - start))
    print('done!')

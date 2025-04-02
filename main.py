import requests
from lxml import etree
import time
import random
import csv
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
import os
from bs4 import BeautifulSoup
import re
import json
from pylab import mpl
from wordcloud import WordCloud

# 设置中文显示字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# 设置正常显示符号
mpl.rcParams["axes.unicode_minus"] = False

#搜索关键词视频基本数据爬取
def get_target(keyword, page,saveName):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    for ii in range(1, page + 1):

        url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&page={}'.format(keyword,ii)
        response = requests.get(url.format(1), headers=headers)

        # 检查是否请求成功
        if response.status_code != 200:
            print("请求失败，状态码：", response.status_code)

        # 使用BeautifulSoup解析HTML 返回类型为<class 'bs4.BeautifulSoup'>
        soup = BeautifulSoup(response.text, 'lxml')

        # 使用正则表达式找到包含视频信息的script标签

        # 获得视频信息（通过css选择器选择嵌套子元素，通过class定位）
        video_infos = soup.select('div.video.i_wrapper.search-all-list div.bili-video-card__wrap __scale-wrap')

        # 初始化一个列表来存储视频信息
        video_info_list = []


        for video_info in video_infos:

            video_info_left=video_info.find('div',class_='bili-video-card__stats--left')
            video_info_right=video_info.find('div',class_='bili-video-card__info--right')

            a = video_info_right.find('a', {'data-v-4caf9c8c': True})
            # 提取href属性
            href = a['href']
            # 提取title属性
            title = a.find('h3', class_='bili-video-card__info--tit').get('title')
            #提取作者信息
            author = video_info_right.find('span', class_='bili-video-card__info--author')
            author = author.get_text(strip=True) if author is not None else '未知作者'
            #提取日期信息
            date = video_info_right.find('span', class_='bili-video-card__info--date')
            date = date.get_text(strip=True) if date is not None else '未知日期'
            #提取播放量和弹幕信息
            video_items=video_info_left.select('span.bili-video-card__stats--item')
            view_num=video_items[0].get_text(strip=True)#这是去掉两头空白
            danmu=video_items[1].get_text(strip=True)
            


            # 将提取的信息存储到列表中
            info = {
                'href': href,
                'title': title,
                'author': author,
                'date': date
            }
            video_info_list.append(info)
        # 打印提取的视频信息
        print("总视频条数：", len(video_info_list))
        print('已经完成b站关于{}第 {} 页爬取'.format(keyword,i))

        result = pd.concat([result, df])

        for i in video_info_list:
            print(f"URL: {i['href']}")
            print(f"Title: {i['title']}")
            print(f"Author: {i['author']}")
            print(f"Date: {i['date']}")
            print('---')

    result = pd.DataFrame()

    for i in range(1, page + 1):
        headers = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

        url = 'https://search.bilibili.com/all?keyword={}&from_source=nav_suggest_new0&page={}'.format(keyword, i)
        html = requests.get(url.format(i), headers=headers)
        bs = etree.HTML(html.text)
        items = bs.xpath('//li[@class = "video-item matrix"]')
        for item in items:
            video_url = item.xpath('div[@class = "info"]/div/a/@href')[0].replace("//","")                   #每个视频的来源地址
            title = item.xpath('div[@class = "info"]/div/a/@title')[0]                  #每个视频的标题
            region = item.xpath('div[@class = "info"]/div[1]/span[1]/text()')[0].strip('\n        ')          #每个视频的分类版块如动画
            view_num = item.xpath('div[@class = "info"]/div[3]/span[1]/text()')[0].strip('\n        ')         #每个视频的播放量
            danmu = item.xpath('div[@class = "info"]/div[3]/span[2]/text()')[0].strip('\n        ')         #弹幕
            upload_time  = item.xpath('div[@class = "info"]/div[3]/span[3]/text()')[0].strip('\n        ')  # 上传日期
            up_author = item.xpath('div[@class = "info"]/div[3]/span[4]/a/text()')[0].strip('\n        ')          #up主

            df = pd.DataFrame({'region': [region],'title': [title], 'view_num': [view_num], 'danmu': [danmu], 'upload_time': [upload_time], 'up_author': [up_author], 'video_url': [video_url]})
            result = pd.concat([result, df])

        time.sleep(random.random() + 1)
        print('已经完成b站第 {} 页爬取'.format(i))
    saveName = saveName + ".csv"
    result.to_csv(saveName, encoding='utf-8-sig',index=False)  # 保存为csv格式的文件
    return result



url="https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1&web_location=333.934&w_rid=eb16f53ad6ae4e8b33c708c9ad8e"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'referer':'https://www.bilibili.com/v/popular/all/',
        'cookie':'buvid3=27CF278D-ED58-B7A3-0238-3D673CBD9D5F83108infoc; b_nut=1732535583; _uuid=F8344A8C-3277-3A69-4775-A25CA10C3112284769infoc; buvid_fp=7a1b3742eb46dccd8090d129221ed49d; buvid4=990313C9-95D8-0477-EF5F-10CF54B9476984595-024112511-jUMVQYaK40y9fqUgmGBkdLtF5fBeA7PeD6g1FyfUqiWnKpO%2F%2Brzz9OdKyjnT279K; enable_web_push=DISABLE; home_feed_column=4; header_theme_version=CLOSE; CURRENT_FNVAL=4048; b_lsid=19D1942E_1936B85308A; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzI5MzY1OTYsImlhdCI6MTczMjY3NzMzNiwicGx0IjotMX0.fS1N2eXfAy4n-lJAazzogVs5YCqtv-IkctHmR4EzuUw; bili_ticket_expires=1732936536; sid=4sqa8g03; rpdid=0z9ZwfQlId|GPup3bY|1ADq|3w1Tg91J; browser_resolution=1374-846'
}
'''
data={
    'ps': '20',
    'pn': '1',
    'web_location': '333.934',
    'w_rid': 'eb16f53ad6ae4e8b33c708c9ad8eb4bd',
    'wts': '1732679450'
}

data = urllib.parse.urlencode(data).encode('utf-8')
'''

#全局变量
video_infos_list = []

# 热门视频数据爬取
def get_popular_videoinfo_data(url):
    # 请求响应，返回request对象
    request = urllib.request.Request(url=url, headers=headers)

    response = urllib.request.urlopen(request)

    # 得到内容
    content = response.read().decode('utf8')

    video_infos = json.loads(content)
    video_infos = video_infos['data']['list']

    # 提取所需信息
    for video_info in video_infos:
        extracted_info = {
            'tname': video_info.get('tname'),
            'title': video_info.get('title'),
            'duration': video_info.get('duration'),
            'owner_name': video_info.get('owner', {}).get('name'),
            'view': video_info.get('stat', {}).get('view'),
            'danmaku': video_info.get('stat', {}).get('danmaku'),
            'reply': video_info.get('stat', {}).get('reply'),
            'favourite': video_info.get('stat', {}).get('favorite'),
            'coin': video_info.get('stat', {}).get('coin'),
            'share': video_info.get('stat', {}).get('share'),
            'like': video_info.get('stat', {}).get('like'),
            # 'dislike': video_info.get('stat', {}).get('dislike'),
            # 'rank': video_info.get('stat', {}).get('now_rank'),
            'pub_location': video_info.get('pub_location')
        }
        video_infos_list.append(extracted_info)


def print_csv(video_info_name):
    for info in video_infos_list:
        '''for key, value in info.items():
            print(f"{key}: {value}")
        print("-------------------")'''

        # 创建一个 CSV 文件并写入标题行
        with open(video_info_name+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = video_infos_list[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # 写入数据行
            for video_info in video_infos_list:
                writer.writerow(video_info)


def data_process():

    # 将列表字典转换为 DataFrame
    df = pd.DataFrame(video_infos_list)

    # 数据预处理
    # 计算每个分区的视频数量
    df['tname'] = df['tname'].astype('category')
    tname_counts = df['tname'].value_counts()

    # 计算每个分区的平均播放量、点赞量和投币量
    #df['duration'] = df['duration'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))  # 将时长转换为分钟
    avg_views = df.groupby('tname')['view'].mean()
    avg_likes = df.groupby('tname')['like'].mean()
    avg_coins = df.groupby('tname')['coin'].mean()

    # 绘制饼图 - 不同分区的视频数量
    plt.figure(figsize=(10, 6))
    tname_counts.plot.pie(autopct='%1.1f%%', startangle=140)
    plt.title('不同分区的视频数量')
    plt.show()

    # 绘制直方图 - 不同分区的平均播放量
    plt.figure(figsize=(10, 6))
    avg_views.plot.bar()
    plt.title('不同分区的平均播放量')
    plt.xlabel('分区')
    plt.ylabel('平均播放量')
    plt.show()

    # 绘制直方图 - 不同分区的平均点赞量
    plt.figure(figsize=(10, 6))
    avg_likes.plot.bar()
    plt.title('不同分区的平均点赞量')
    plt.xlabel('分区')
    plt.ylabel('平均点赞量')
    plt.show()

    # 绘制直方图 - 不同分区的平均投币量
    plt.figure(figsize=(10, 6))
    avg_coins.plot.bar()
    plt.title('不同分区的平均投币量')
    plt.xlabel('分区')
    plt.ylabel('平均投币量')
    plt.show()

    # 绘制直方图 - 视频时长与播放量、点赞量、投币数的关联
    # 这里需要对视频时长进行处理，例如转换为分钟，并计算每个时长的视频的播放量、点赞量和投币量
    # 然后绘制直方图
    # 由于这需要更具体的视频时长数据，这里仅提供概念性代码
    # df['duration_minutes'] = df['duration'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))
    # avg_views_by_duration = df.groupby('duration_minutes')['view'].mean()
    # avg_likes_by_duration = df.groupby('duration_minutes')['like'].mean()
    # avg_coins_by_duration = df.groupby('duration_minutes')['coin'].mean()
    # plt.figure(figsize=(10, 6))
    # avg_views_by_duration.plot.bar


def generate_wordcloud(text, output_file='wordcloud.png'):

    # 配置词云参数
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        font_path='simhei.ttf',
        max_words=200,
        colormap='viridis'
    ).generate(text)

    # 显示词云
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 不显示坐标轴
    plt.title("词云", fontsize=20)
    plt.show()

    # 保存词云图片
    wordcloud.to_file(output_file)
    print(f"词云已保存至 {output_file}")



def create_wordcloud_from_titles(video_infos_list):

    # 提取标题并拼接为字符串
    titles = " ".join(video['title'] for video in video_infos_list if 'title' in video)
    generate_wordcloud(titles, output_file='bilibili_titles_wordcloud.png')

if __name__ == "__main__":
    urls=['https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1&web_location=333.934&w_rid=eb16f53ad6ae4e8b33c708c9ad8eb4bd&wts=1732679450','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=2&web_location=333.934&w_rid=d64a82b4731b0eb3b78351706ae1da26&wts=1732682868','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=3&web_location=333.934&w_rid=d274360a8930ee47af183b23e3bed8d3&wts=1732682869','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=4&web_location=333.934&w_rid=3261f3ae22bf27ac611f809bcf81e076&wts=1732682870','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=5&web_location=333.934&w_rid=a54aed3c744f1c0804c6b923165218d3&wts=1732682931','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=6&web_location=333.934&w_rid=9915f988f7956467846eb4e597421c0b&wts=1732682931','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=7&web_location=333.934&w_rid=8ccd2cf051b9a0b31ee488ca5864e15a&wts=1732682932','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=8&web_location=333.934&w_rid=c37b92d4d15e6d8d146938ab6e555661&wts=1732682933','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=9&web_location=333.934&w_rid=5094b34169a8f0819703a895e363199b&wts=1732682933','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=10&web_location=333.934&w_rid=32fcfaefa291b4a9ab0f91e127416da&wts=1732682934','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=8&web_location=333.934&w_rid=c37b92d4d15e6d8d146938ab6e555661&wts=1732682933','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=9&web_location=333.934&w_rid=5094b34169a8f0819703a895e363199b&wts=1732682933','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=10&web_location=333.934&w_ri=32fcfaefa291b4a9ab0f91e127416da9&wts=1732682934','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=11&web_location=333.934&w_rid=6e92c92ae67fa197ab7087306e3975c3&wts=1732684609','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=12&web_location=333.934&w_rid=8c0581fc3fc1a77aa3d052ef875dfde1&wts=1732684610','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=13&web_location=333.934&w_rid=9b560117f5d03a867f90706c1a5ad405&wts=1732687653','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=14&web_location=333.934&w_rid=bcef71242268eb6725e739035ada236d&wts=1732687654','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=15&web_location=333.934&w_rid=4ef6bc1a39af910a41cfd57f5057f80b&wts=1732687655','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=16&web_location=333.934&w_rid=811bed0f57657ada0d89830c6a542056&wts=1732687655','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=17&web_location=333.934&w_rid=9bae351f3956e978b17e875d51f1acb6&wts=1732687656','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=18&web_location=333.934&w_rid=854d35eb073a2aca09370b340f747424&wts=1732687657','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=19&web_location=333.934&w_rid=9b851cfc82422ae72ba2b424b55f2ec7&wts=1732687663','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=20&web_location=333.934&w_rid=6e8ad648ec87d121e27c423d4046780b&wts=1732687664','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=21&web_location=333.934&w_rid=1bbeb6682b9b618cddee6932c69e4ddd&wts=1732687665','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=22&web_location=333.934&w_rid=ea0ac90a2bf7d8d06dfc0095b0be1829&wts=1732687666','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=23&web_location=333.934&w_rid=3f94ed1a52ad34479ce58214c9e86796&wts=1732687668','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=24&web_location=333.934&w_rid=0b372cc3377a72e0663a4b50ac0a3479&wts=1732687669','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=25&web_location=333.934&w_rid=a79bb92898cf1d0a29d2ed2c2a59dff0&wts=1732687669','https://api.bilibili.com/x/web-interface/popular?ps=20&pn=26&web_location=333.934&w_rid=ae6597c9999753ff98ea5cd280c95895&wts=1732687670']
    for url in urls:
        get_popular_videoinfo_data(url)

    #将数据导入excel文件
    #print_csv('pop_video_info')

    #数据分析
    #data_process()

    #词云生成
    create_wordcloud_from_titles(video_infos_list)


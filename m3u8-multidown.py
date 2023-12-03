import os
import random
import time
from lxml import etree
import requests
import threading
import re
import requests.adapters
import urllib3

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 50
T1 = time.time()
cnt = 0
MB = 1024 ** 2
Totalsize = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    # 'Cookie':'mx_style=white; Hm_lvt_0fb920eb3bc60ac56e445056e431d5e3=1701530828; showBtn=true; Hm_lpvt_0fb920eb3bc60ac56e445056e431d5e3=1701530837; mac_history_mxpro=%5B%7B%22vod_name%22%3A%22%E9%AD%94%E7%8E%8B%E5%AD%A6%E9%99%A2%E7%9A%84%E4%B8%8D%E9%80%82%E5%90%88%E8%80%85%20%E7%AC%AC%E4%BA%8C%E5%AD%A3%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.yinhuadm.cc%2Fp%2F10961-1-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%5D',

}
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 "
    "Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",

]

proxy_pool = [
    'http://61.190.161.172:49943',
    'http://182.45.64.157:24790',
    'http://125.83.115.151:26078',
    'http://120.34.14.1:31948',
    'http://221.202.130.253:37255',
    'http://117.83.16.3:29968',
    'http://114.231.8.68:23982',
    'http://59.60.142.69:46784',
    'http://27.156.194.144:26720',
    'http://114.231.46.130:28482',
]
proxy = {
    'http': 'http://114.231.46.130:28482'
}


def get_file_size(url: str, raise_error: bool = False) -> int:
    proxy['http'] = random.choice(proxy_pool)
    response = requests.head(url=url, headers=headers, verify=False, proxies=proxy)
    file_size = response.headers.get('Content-Length')
    if file_size is None:
        if raise_error is True:
            raise ValueError('该文件不支持多线程分段下载！')
        return 0
    return int(file_size)


def download(url, file_name):
    global cnt
    global Totalsize
    headers['User-Agent'] = random.choice(user_agent_list)
    time.sleep(random.random() / 10)
    with requests.get(url, headers=headers, stream=True, verify=False) as r:
        # r.raise_for_status()
        with open(f'./{comic_name}/' + file_name, 'wb') as f:
            Totalsize += get_file_size(url)
            # size = 0
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
                    # size += len(chunk)
                    # print('\r' + '%s [下载进度]:%s%.2f%%' % (
                    #     file_name, '>' * int(size * 50 / int(totalsize)), float(size / int(totalsize) * 100)), end=' ')
            size = int((cnt / len(urls) * 25))
            flo = float(cnt / len(urls))
            print('\r' + '[下载进度]:|' + ('■' * size) + (' ' * (25 - size)) + '|', str(flo * 100), end='')
            cnt += 1


def download_files(Urls, names, way, num_threads=5, ):
    threads = []
    for i in range(num_threads):
        for j in range(i, len(Urls), num_threads):
            if way == 1:
                url = Urls[j]
            else:
                url = base + Urls[j]
            file_name = url.split('/')[-1]
            if not os.path.exists(f'./{comic_name}/' + file_name):
                thread = threading.Thread(target=download, args=(url, file_name))
                thread.start()
                threads.append(thread)

    for thread in threads:
        thread.join()


def download_missed(start, lenth, names, way):
    missed = []
    for x in range(start, lenth):
        if not os.path.isfile(f'./{comic_name}/' + str(names[x])):
            missed.append(urls[x])
    if int(len(missed)) > 25:
        for i in range(25, len(missed), 25):
            download_files(missed[i - 25:i], way=way, names=names)
    else:
        download_files(missed, way=way, names=names)


def run():
    pass


def get_title():
    proxy['http'] = random.choice(proxy_pool)
    index = requests.get(url=input('输入动漫首页网址：'), headers=headers,proxies=proxy)
    content = index.content.decode('utf-8')
    tree = etree.HTML(content)
    txt = tree.xpath('//h3[@class="title"]/h1/a/text()')
    print('动漫名称为：' + txt[0])
    return txt[0]


if __name__ == '__main__':
    comic_name = input('动漫名称:')
    comic_num = input('集数：')
    way = int(input('类型：'))

    if not os.path.exists(comic_name):
        os.mkdir(comic_name)

    # fp = open('mixed.m3u8', 'w', encoding='utf-8')
    m3u8_url = str(input('输入m3u8地址：'))
    base = m3u8_url[0:len(m3u8_url) - len(m3u8_url.split('/')[-1])]
    content = requests.get(url=m3u8_url, headers=headers).content.decode('utf-8')
    # fp.close()
    urls = re.findall('.+ts', content)
    if way == 1:
        _names = [str(i).split('/')[-1] for i in urls]
    else:
        _names = urls
    for i in range(32, len(urls) - 32, 32):
        download_files(Urls=urls[i - 32:i], names=_names, num_threads=5, way=way)
    # 补缺
    download_missed(0, len(urls), names=_names, way=way)

    # 清空
    out = open(f'./{comic_name}/{comic_name} 第{comic_num}集.ts', 'wb')
    out.write(bytes(0))
    out.close()
    # 合并

    out = open(f'./{comic_name}/{comic_name} 第{comic_num}集.ts', 'ab+')
    for i in range(0, len(urls)):
        if not os.path.exists(f'./{comic_name}/' + str(_names[i])):
            download_missed(i, len(urls), names=_names, way=way)
        with open(f'./{comic_name}/' + str(_names[i]), 'rb') as fp:
            content = fp.read()
            out.write(content)
            print('Write ' + _names[i])
            fp.close()
        os.remove(f'./{comic_name}/' + str(_names[i]))
    out.close()
    T2 = time.time()
    print('程序运行时间:%s秒' % (T2 - T1))
    print('平均速度:%.2fMB/s' % ((Totalsize / MB) / (T2 - T1)))

import os
import random
import time

import requests
import threading

import requests.adapters
import urllib3
import warnings
warnings.filterwarnings("ignore")

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5
s = requests.session()
s.keep_alive = False
T1 = time.time()
cnt = 0
MB = 1024 ** 2
Totalsize = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    # 'Cookie':'mx_style=white; Hm_lvt_0fb920eb3bc60ac56e445056e431d5e3=1701530828; showBtn=true; Hm_lpvt_0fb920eb3bc60ac56e445056e431d5e3=1701530837; mac_history_mxpro=%5B%7B%22vod_name%22%3A%22%E9%AD%94%E7%8E%8B%E5%AD%A6%E9%99%A2%E7%9A%84%E4%B8%8D%E9%80%82%E5%90%88%E8%80%85%20%E7%AC%AC%E4%BA%8C%E5%AD%A3%22%2C%22vod_url%22%3A%22https%3A%2F%2Fwww.yinhuadm.cc%2Fp%2F10961-1-1.html%22%2C%22vod_part%22%3A%22%E7%AC%AC01%E9%9B%86%22%7D%5D',
    'Connection':'close',
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


def clear_others(ls):
    res = []
    for item in ls:
        if item.startswith("#") or item == '':
            continue
        res.append(item)
    return res


def judge_format(str):
    if str.startswith('http'):
        return True
    else:
        return False

def download_files(Urls, names, way, is_repair=False, num_threads=5, ):
    threads = []
    for i in range(0,len(Urls),num_threads):
        if i+num_threads > len(Urls)-1:
            tmp=len(Urls)
        else:
            tmp=i+num_threads
        for j in range(i, tmp):
            if way == 1:
                url = Urls[j]
            else:
                url = base + Urls[j]
            file_name = url.split('/')[-1]
            if not os.path.exists(download_path + '/'+file_name):
                thread = threading.Thread(target=download, args=(url, file_name, is_repair))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

def get_file_size(url: str, raise_error: bool = False) -> int:
    # proxy['http'] = random.choice(proxy_pool)
    response = requests.head(url=url, headers=headers, verify=False)
    file_size = response.headers.get('Content-Length')
    if file_size is None:
        if raise_error is True:
            raise ValueError('该文件不支持多线程分段下载！')
        return 0
    return int(file_size)

def download_missed(start, lenth, names, way):
    missed = []
    for x in range(start, lenth):
        if not os.path.isfile(download_path+'/' + str(names[x])):
            missed.append(content_list[x])
    if int(len(missed)) > 25:
        for i in range(25, len(missed), 25):
            download_files(missed[i - 25:i], way=way, names=names,is_repair=True )
    else:
        download_files(missed, way=way, names=names,is_repair=True )
    for x in range(start, lenth):
        if not os.path.isfile(download_path+'/' + str(names[x])):
            download_missed(0, lenth, names, way)

def download(url, file_name, is_repair=False):
    global cnt
    global Totalsize

    headers['User-Agent'] = random.choice(user_agent_list)
    time.sleep(random.random() / 10)
    with requests.get(url, headers=headers, stream=True, verify=False) as r:
        # r.raise_for_status()
        with open(download_path+'/' + file_name, 'wb') as f:
            Totalsize += get_file_size(url)
            # size = 0
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
                    # size += len(chunk)
                    # print('\r' + '%s [下载进度]:%s%.2f%%' % (
                    #     file_name, '>' * int(size * 50 / int(totalsize)), float(size / int(totalsize) * 100)), end=' ')
            size = int((cnt / len(content_list) * 25))
            flo = float(cnt / len(content_list))
            if is_repair is False:
                print('\r' + '[下载进度]:|' + ('■' * size) + (' ' * (25 - size)) + '|', str(round(flo * 100,3)), end='')
            else:
                print('\r' + '[修复进度]:|' + ('■' * size) + (' ' * (25 - size)) + '|', str(round(flo * 100,3)), end='')
            cnt += 1

def is_full_downloaded(start, length, names):
    for x in range(start, length):
        if not os.path.isfile(download_path+'/' + str(names[x])):
            return False
    return True

if __name__ == '__main__':
    T1=time.time()
    download_path = r'./downloads'
    if not os.path.exists('downloads'):
        os.mkdir('downloads')
    file_name = input("Input filename:")
    m3u8_url = str(input('输入m3u8地址：'))
    base = m3u8_url[0:len(m3u8_url) - len(m3u8_url.split('/')[-1])]
    content = requests.get(url=m3u8_url, headers=headers).content.decode('utf-8')
    content_list = content.split('\n')
    content_list = clear_others(content_list)
    if judge_format(content_list[0]):
        way = 1
        _names = [str(i).split('/')[-1] for i in content_list]
    else:
        way = 2
        _names = content_list
    # for i in range(50, len(content_list) - 50, 50):
    download_files(Urls=content_list, names=_names, num_threads=128, way=way)
    # 补缺
    download_missed(0, len(content_list), names=_names, way=way)
    # # 成功下载
    # if is_full_downloaded(0,len(content_list), names=_names):
    #     print("完整下载!")
    # else:
    #     print("注意:文件有缺漏,请重新下载!")
    # 合并
    out = open(download_path+'/'+file_name+'.ts', 'ab+')
    for i in range(0, len(content_list)):
        if not os.path.exists(download_path+'/' + str(_names[i])):
            download_missed(i, len(content_list), names=_names, way=way)
        with open(download_path+'/' + str(_names[i]), 'rb') as fp:
            content = fp.read()
            out.write(content)
            # print('Write ' + _names[i])
            fp.close()
        os.remove(download_path+'/' + str(_names[i]))
    out.close()
    T2 = time.time()
    print('\n程序运行时间:%s秒' % (T2 - T1))
    print('平均速度:%.2fMB/s' % ((Totalsize / MB) / (T2 - T1)))
    os.system('pause')
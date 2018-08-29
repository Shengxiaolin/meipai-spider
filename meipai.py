import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging

channel_urls = [
    'http://www.meipai.com/squares/new_timeline?page={}&count=24&tid=474',  # 高颜值
    'http://www.meipai.com/topics/hot_timeline?page={}&count=24&tid=5872239354896137479',  # 舞蹈
    'http://www.meipai.com/topics/hot_timeline?page={}&count=24&tid=5871155236525660080',  # 音乐
    'http://www.meipai.com/topics/hot_timeline?page={}&count=24&tid=6204189999771523532',  # 穿秀
    'http://www.meipai.com/squares/new_timeline?page={}&count=24&tid=27',  # 美妆
    'http://www.meipai.com/squares/new_timeline?page={}&count=24&tid=16',  # 爱豆
    'http://www.meipai.com/topics/hot_timeline?page={}&count=24&tid=5872639793429995335',  # 运动
    'http://www.meipai.com/topics/hot_timeline?page={}&count=24&tid=6161763227134314911',  # 吃秀
    'http://www.meipai.com/squares/new_timeline?page={}&count=24&tid=13',  # 搞笑
    'http://www.meipai.com/squares/new_timeline?page={}&count=24&tid=488',  # 精选
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(filename)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='meipai.log',
    filemode='w'
)

console = logging.StreamHandler()
logging.getLogger().addHandler(console)

chrome_options = Options()
# chrome_options.add_argument('window-size=1920x3000') # 指定浏览器分辨率
chrome_options.add_argument('--disable-gpu')  # 规避BUG
chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条
chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片
chrome_options.add_argument('--headless')  # 不提供可视化页面

driver = webdriver.Chrome(chrome_options=chrome_options)


def video_url(page_url):

    driver.get(page_url)

    player_bs = BeautifulSoup(driver.page_source, 'lxml')
    player = player_bs.find('div', attrs={'class': 'mp-h5-player-layer-video'}) # bs.finaAll() return a list
    video_bs = BeautifulSoup(str(player), 'lxml')
    url = video_bs.find('video')['src']

    return url


if __name__ == '__main__':

    for channel in channel_urls:
        logging.info('Start crawl channel:{}'.format(channel))
        page = 0
        while True:
            page += 1
            logging.info('Crawl page:{}'.format(page))
            html_json = requests.get(channel.format(page)).json()
            medias = html_json['medias']
            if medias == []:
                break
            for video in medias:
                page_url = video['url']
                try:
                    play_url = video_url(page_url).split('?')[0]
                    print('video url:{}'.format(play_url))
                except TypeError:
                    logging.info('TypeError.')
                    continue
                except WebDriverException:
                    logging.info('Page url format error.')
                    continue
    driver.close()
    logging.info('Task done.')
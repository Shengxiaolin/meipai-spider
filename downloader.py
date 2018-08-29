# -*- coding: UTF-8 -*-
import requests
from contextlib import closing


class ProgressBar(object):
    def __init__(self, title, count=0.0, run_status=None, fin_status=None, total=100.0, unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "[%s] %s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # [名称] 状态 进度 单位 分割线 总数 单位
        _info = self.info % (
        self.title, self.status, self.count / self.chunk_size, self.unit, self.seq, self.total / self.chunk_size,
        self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str, )


if __name__ == '__main__':

    print('*' * 100)
    print('\t\t\t\t欢迎使用文件下载小助手')
    print('作者:Jack-Cui\n博客:http://blog.csdn.net/c406495762')
    print('*' * 100)

    url = 'http://mvvideo10.meitudata.com/5b0e5e34c1a5e3132_H264_20.mp4?k=cbf954dc005ffab0613b89f5c9376229&t=5b74e077'
    filename = url.split('/')[-1].split('?')[0] # meipai video name format

    with closing(requests.get(url, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            print('文件大小:%0.2f KB' % (content_size / chunk_size))
            progress = ProgressBar("%s下载进度" % filename
                                   , total=content_size
                                   , unit="KB"
                                   , chunk_size=chunk_size
                                   , run_status="正在下载"
                                   , fin_status="下载完成")

            with open(filename, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data))
        else:
            print('链接异常')
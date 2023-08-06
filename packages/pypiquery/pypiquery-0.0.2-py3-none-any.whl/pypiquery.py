#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""通过 pypi 项目管理网站搜索软件包

由于 pip search 服务关闭，无法通过命令行搜索 pypi 软件包。本软件通过命令行模拟浏览器搜索，并展现搜索结果，解决命令行搜索问题。

@update 2022.7.23

Usage :
    pypiquery <project_name>

    -- or --

    ppq <project_name>

Hotkeys :
    n   : 下一页（Next page）。
    k   : 上一页（Prev page）。
    esc : 退出（Quit）。
"""

__author__ = 'do0ob'
__version__ = '0.0.2'

import keyboard
import requests
import sys

from bs4 import BeautifulSoup

class pypiQuery():
    """pypi 项目页面搜索类
    """

    def __init__(self):
        self.__pypi_url = 'https://pypi.org/'
        self.__pypi_query_url = 'https://pypi.org/search/'
        self.__pages = 0
        self.__current_page = 0
        self.__keyword = ''
        self.__libs = []
    
    def __analyseResultPage(self, __html):
        """分析页面脚本并获取页面中的软件包信息

        Args :
            __html : pypi 搜索结果页面 HTML 脚本。
        
        Return :
            搜索结果列表，列表中每一项是一个 (项目名称, 版本, 说明) 结构的元组。
        """
        _result = BeautifulSoup(__html, 'html.parser').find('ul', attrs={'aria-label': 'Search results'}).find_all('li')
        _libs = []
        for i in _result:
            _libs.append((i.select('.package-snippet__name')[0].string, i.select('.package-snippet__version')[0].string, i.select('.package-snippet__description')[0].string))
        
        # 获取结果页面数
        if self.__pages == 0:
            try:
                _page = BeautifulSoup(__html, 'html.parser').select('.button-group--pagination > a')[-2].text
                self.__pages = int(_page)
            except IndexError:
                pass

        # 缓存当前页面结果
        self.__libs = _libs
        return _libs

    @property
    def currentpage(self):
        """当前页码

        Args :
            None
        
        Return :
            当前页码。
        """
        return self.__current_page

    @property
    def pages(self):
        """结果页面总数

        Arg :
            None

        Return :
            结果页面总数。
        """
        return self.__pages

    def get(self, __keyword, __page = 1):
        """从 pypi 项目管理网站获取指定软件包搜索结果

        Args :
            __keyword : 搜索内容。
            __page    : 结果页面索引号。必须是 >= 1 的整数，默认值是 1。

        Return :
            搜索结果列表。
        """
        if not isinstance(__page, int):
            raise TypeError
        elif __page <= 0:
            raise ValueError
        
        if __page == 1:
            _search_param = ''.join((self.__pypi_query_url, '?q=', str(__keyword)))
        else:
            _search_param = ''.join((self.__pypi_query_url, '?q=', str(__keyword), '&page=', str(__page)))
        self.__current_page = __page
        self.__keyword = __keyword
        reqs = requests.get(_search_param)
        return self.__analyseResultPage(reqs.text)
    
    def prev(self):
        """获取上一个结果页面

        Args :
            None

        Return :
            搜索结果列表。
        """
        if self.__current_page > 1:
            self.__current_page -= 1
            return self.get(self.__keyword, self.__current_page)
        else:
            raise IndexError

    def next(self):
        """获取下一个结果页面

        Args :
            None

        Return :
            搜索结果列表。
        """
        if self.__current_page + 1 <= self.__pages:
            self.__current_page += 1
            return self.get(self.__keyword, self.__current_page)
        else:
            raise EOFError
    
    def print(self, format = 0):
        """打印搜索结果
        
        Args :
            format : 输出格式。0 简洁格式（默认值）；1 详细格式。

        Return :
            None
        """
        if format == 0:
            for i in self.__libs:
                print('{0} : {1}'.format(i[0], i[2]))
        else:
            for i in self.__libs:
                print('{0} ({1}) : {2}'.format(i[0], i[1], i[2]))

def print_more(__obj, __direct):
    try:
        if __direct == 0:
            __obj.prev()
        else:
            __obj.next()
        
        __obj.print()
        print('-- ( {0} / {1} ) More --'.format(__obj.currentpage, __obj.pages))
    except IndexError:
        pass
    except EOFError:
        pass

def main():
    _args = ' '.join(sys.argv[1:])
    _libs = pypiQuery()
    _libs.get(_args)
    _libs.print()
    if _libs.pages > 1:
        print('-- ( {0} / {1} ) More --'.format(_libs.currentpage, _libs.pages))
        keyboard.add_hotkey('n', print_more, args=(_libs, 1))
        keyboard.add_hotkey('k', print_more, args=(_libs, 0))
        _rec = keyboard.record(until='esc')

if __name__ == '__main__':
    main()
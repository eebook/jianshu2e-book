# -*- coding: utf-8 -*-
import json


from src.tools.controler import Control
from src.tools.debug import Debug
from src.tools.http import Http
from src.tools.match import Match
from src.tools.db import DB

from src.lib.jianshu_parser.jianshuparser import JianshuParser
from src.lib.jianshu_parser.tools.parser_tools import ParserTools
from bs4 import BeautifulSoup


class PageWorker(object):
    def __init__(self, task_list):
        self.task_set = set(task_list)
        self.task_complete_set = set()
        self.work_set = set()            # 待抓取网址池
        self.work_complete_set = set()   # 已完成网址池
        self.content_list = []           # 用于存放已抓取的内容

        self.answer_list = []            # 存放文章的列表, 如果是jianshu的话, 对应的表是jianshu_article
        self.question_list = []          # 博客信息的list, 如果是jianshu的话, 对应的表是jianshu_info

        self.info_list = []
        self.extra_index_list = []
        self.info_url_set = self.task_set.copy()
        self.info_url_complete_set = set()

        self.add_property()  # 添加扩展属性

    def add_property(self):

        return

    @staticmethod
    def parse_max_page(content):
        u"""
        :param content: 博客目录的页面内容
        :return:
        """
        max_page = 1
        try:
            floor = content.index('">下一页</a>')
            floor = content.rfind('</a>', 0, floor)
            cell = content.rfind('>', 0, floor)
            max_page = int(content[cell + 1:floor])
            Debug.logger.info(u'答案列表共计{}页'.format(max_page))
        except:
            Debug.logger.info(u'答案列表共计1页')
        finally:
            return max_page

    @staticmethod
    def parse_blog_link_from_article_list(content):
        u"""
        :param content: 某一页博客目录的内容
        :return:
        """

    def create_save_config(self):    # TODO
        config = {'Answer': self.answer_list, 'Question': self.question_list, }
        return config

    def clear_index(self):
        u"""
        用于在collection/topic中清除原有缓存
        """
        return

    def save(self):         # TODO
        self.clear_index()
        save_config = self.create_save_config()
        for key in save_config:
            for item in save_config[key]:
                if item:
                    DB.save(item, key)
        DB.commit()
        return

    def start(self):
        self.start_catch_info()
        self.start_create_work_list()
        self.start_worker()
        # print "answer_list!!!!!!!:" + str(self.answer_list)
        self.save()  # bug??
        return

    def create_work_set(self, target_url):
        if target_url in self.task_complete_set:
            return
        content = Http.get_content(target_url + '?nr=1&sort=created')
        if not content:
            return
        self.task_complete_set.add(target_url)
        max_page = self.parse_max_page(content)
        for page in range(max_page):
            url = '{}?nr=1&sort=created&page={}'.format(target_url, page + 1)
            self.work_set.add(url)
        return

    def clear_work_set(self):
        self.work_set = set()
        return

    def start_create_work_list(self):
        self.clear_work_set()
        argv = {'func': self.create_work_set, 'iterable': self.task_set, }
        Control.control_center(argv, self.task_set)
        return

    def worker(self, target_url):
        if target_url in self.work_complete_set:
            # 自动跳过已抓取成功的网址
            return

        Debug.logger.info(u'开始抓取{}的内容'.format(target_url))
        content = Http.get_content(target_url)
        if not content:
            return
        content = Match.fix_html(content)  # 需要修正其中的<br>标签，避免爆栈
        self.content_list.append(content)
        Debug.logger.debug(u'{}的内容抓取完成'.format(target_url))
        self.work_complete_set.add(target_url)
        return

    def parse_content(self, content):     # SinaBlogWorker重载了
        return

    def start_worker(self):
        u"""
        work_set是所有的需要抓取的页面
        :return:
        """
        a = list(self.work_set)
        a.sort()
        argv = {'func': self.worker,  # 所有待存入数据库中的数据都应当是list
                'iterable': a, }
        Control.control_center(argv, self.work_set)
        Debug.logger.info(u"所有内容抓取完毕，开始对页面进行解析")
        i = 0
        for content in self.content_list:
            i += 1
            Debug.print_in_single_line(u"正在解析第{}/{}张页面".format(i, self.content_list.__len__()))
            self.parse_content(content)
        Debug.logger.info(u"网页内容解析完毕")
        return

    def catch_info(self, target_url):
        return

    def start_catch_info(self):
        argv = {'func': self.catch_info, 'iterable': self.info_url_set, }
        Control.control_center(argv, self.info_url_set)
        return


class JianshuAuthorWorker(PageWorker):
    pass


class JianshuWorker(PageWorker):
    u"""
    简书的worker
    """
    def create_save_config(self):         # TODO
        config = {
            'jianshu_article': self.answer_list,
            'jianshu_info': self.question_list
        }
        return config

    def parse_content(self, content):
        Debug.logger.debug(u"解析文章内容")
        parser = JianshuParser(content)
        self.answer_list += parser.get_answer_list()

    @staticmethod
    def parse_get_article_list(article_list_content):
        u"""
        获得每一篇博客的链接组成的列表
        :param article_list_content: 有博文目录的href的页面
        :return:
        """
        soup = BeautifulSoup(article_list_content, "lxml")
        article_href_list = []

        article_list = soup.select('h4.title a')
        for item in range(len(article_list)):
            article_href = 'http://www.jianshu.com' + str(ParserTools.get_attr(article_list[item], 'href'))
            article_href_list.append(article_href)
        return article_href_list

    def create_work_set(self, target_url):
        u"""
        根据target_url(例:http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles)的内容,
        先获得creator_id, 再根据文章的数目, 获得页面数, 依次打开每个页面, 将文章的地址放入work_set中
        :param target_url:
        :return:
        """
        # Debug.logger.debug(u"target_url是???" + str(target_url))
        if target_url in self.task_complete_set:
            return
        id_result = Match.jianshu(target_url)
        jianshu_id = id_result.group('jianshu_id')
        Debug.logger.debug(u"jianshu_id是???" + str(jianshu_id))

        # ############下面这部分应该是JianshuAuthorInfo的内容, 完成jianshu_info中的内容,暂时写在这, 以后再优化
        content_profile = Http.get_content(target_url)

        parser = JianshuParser(content_profile)
        self.question_list += parser.get_jianshu_info_list()
        Debug.logger.debug(u"create_work_set中的question_list是什么??" + str(self.question_list))
        # #############上面这部分应该是JianshuAuthorInfo的内容, 完成jianshu_info中的内容,暂时写在这, 以后再优化

        self.task_complete_set.add(target_url)
        article_num = self.question_list[0]['article_num']    # 这样的话, 一行只能写一个地址  TODO
        Debug.logger.debug(u"article_num" + str(article_num))

        if article_num % 9 != 0:
            page_num = article_num/9 + 1      # 博客目录页面, 1页放50个博客链接
        else:
            page_num = article_num / 9
        Debug.logger.debug(u"page_num????" + str(page_num))

        article_list = self.parse_get_article_list(content_profile)
        for item in article_list:
            self.work_set.add(item)
        for page in range(page_num-1):          # 第一页是不需要打开的
            url = 'http://www.jianshu.com/users/{}/latest_articles?page={}'.format(jianshu_id, page+2)
            content_article_list = Http.get_content(url)
            article_list = self.parse_get_article_list(content_article_list)
            for item in article_list:
                self.work_set.add(item)
        return





def worker_factory(task):
    type_list = {
        'jianshu': JianshuWorker, 'jianshuAuthor': JianshuAuthorWorker
    }
    for key in task:
        worker = type_list[key](task[key])
        worker.start()

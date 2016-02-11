# -*- coding: utf-8 -*-

from src.container.image import ImageContainer
from src.tools.config import Config
from src.tools.db import DB
from src.tools.match import Match
from src.tools.type import Type
from src.tools.debug import Debug


class InitialBook(object):
    u"""
        ->kind
        ->author_id
        ->sql ->class sql
                ->info
                ->article
                ->info_extra
                ->article_extra
        ->epub ->class Epub
                    ->article_count
                    ->char_count
                    ->title
                    ->id
                    ->split_index
                    ->prefix
        ->info
        ->article_list
        ->page_list
        ->prefix
    """
    class Sql(object):
        def __init__(self):
            self.info = ''
            self.article = ''
            self.info_extra = ''
            self.article_extra = ''      # 用来扩展的????
            return

        def get_article_sql(self):
            return self.article_extra + Config.sql_extend_answer_filter

    class Epub(object):
        def __init__(self):
            self.article_count = 0
            self.char_count = 0

            self.title = ''
            self.id = ''
            self.split_index = 0
            self.prefix = ''
            return

    def __init__(self):
        self.kind = 'balabala'
        self.author_id = 0
        self.sql = InitialBook.Sql()
        self.epub = InitialBook.Epub()
        self.info = {}
        self.article_list = []
        self.page_list = []
        self.prefix = ''
        return

    def catch_data(self):
        u"""
        从数据库中获取数据
        :return:
        """
        self.catch_info()      # 获取博客信息
        self.get_jianshu_list()         # 获取文章所有信息
        # self.__sort()       TODO
        return self

    def catch_info(self):
        u"""
        获得博客的信息, 将info作为参数传给set_info
        :return:
        """
        info = {}
        if self.sql.info:
            if self.kind == Type.jianshu:
                info = self.catch_jianshu_book_info()
        self.set_info(info)           # TODO   暂时还没有其他种类
        Debug.logger.info(u"catch_info中的info为:" + str(info))
        return

    def catch_jianshu_book_info(self):
        u"""

        :param
        :return: info
        """
        info_list = DB.cursor.execute(self.sql.info).fetchall()
        info_list = [DB.wrap(Type.jianshu_info, item) for item in info_list]
        info = {}
        info['creator_name'] = '_'.join([str(item['creator_name']) for item in info_list])  # 可以是多个博客组合在一起
        info['creator_id'] = '_'.join([str(item['creator_id']) for item in info_list])
        Debug.logger.info(u"catch_jianshu_book_info中的info:" + str(info))
        return info

    def set_info(self, info):
        self.info.update(info)
        if self.kind == Type.jianshu:              # 该博客所有的博文
            self.epub.title = u'简书_{}({})'.format(info['creator_name'], info['creator_id'])
            print (u"self.epub.title没有设置???" + str(self.epub.title))
            self.epub.id = info['creator_id']
        elif self.kind == Type.jianshu_article:    # 单篇博文 TODO
            self.epub.title = u'简书博文集锦({})'.format(info['title'])
            self.epub.id = info['id']       # TODO

    def get_jianshu_list(self):
        if self.kind in Type.jianshu:      # TODO 目前只有一种情况
            article_list = self.__get_jianshu_list()
        self.set_article_list(article_list)     # 原因如上
        return

    def __get_jianshu_list(self):
        jianshu_list = [DB.wrap('jianshu_info', x) for x in DB.get_result_list(self.sql.info)]
        jianshu_article_list = [DB.wrap('jianshu_article', x) for x in DB.get_result_list(self.sql.article)]


        # Debug.logger.info(u"在__get_SinaBlog_list中, SinaBlog_list:" + str(SinaBlog_list))
        # Debug.logger.info(u"在__get_SinaBlog_list中, SinaBlog_article_list[0]:" + str(SinaBlog_article_list[0]))

        def merge_article_into_jianshu():
            jianshu_dict = {item['creator_id']: {'jianshu': item.copy(), 'jianshu_article_list': [], }
                             for item in jianshu_list}

            for jianshu_article in jianshu_article_list:
                jianshu_dict[jianshu_article['author_id']]['jianshu_article_list'].append(jianshu_article)
            return jianshu_dict.values()

        def add_property(jianshu):
            char_count = 0
            # TODO comment_count
            for jianshu_article in jianshu['jianshu_article_list']:
                jianshu_article['char_count'] = len(jianshu_article['content'])
                jianshu_article['update_date'] = jianshu_article['publish_date']
                char_count += jianshu_article['char_count']
            jianshu['article_count'] = len(jianshu['jianshu_article_list'])
            jianshu['char_count'] = char_count
            return jianshu
        article_list = [add_property(x) for x in merge_article_into_jianshu() if len(x['jianshu_article_list'])]
        return article_list

    def set_article_list(self, article_list):
        self.clear_property()
        for article in article_list:
            self.epub.article_count += article['article_count']
            self.epub.char_count += article['char_count']
        # self.epub.article_count = len(article_list)     # 不然,一个博客就是一个article_count
        self.article_list = article_list
        return

    def clear_property(self):
        # self.epub.title = ''
        # self.epub.prefix = ''
        self.epub.article_count = 0
        self.epub.char_count = 0
        return


class HtmlBookPackage(object):
    def __init__(self):
        self.book_list = []
        self.image_list = []
        self.image_container = ImageContainer()
        return

    def get_title(self):
        title = ''.join([book.epub.title for book in self.book_list])
        title = Match.fix_filename(title)    # 移除特殊字符
        return title


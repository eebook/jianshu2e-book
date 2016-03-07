# -*- coding: utf-8 -*-

from src.tools.type import Type
from src.container.initialbook import InitialBook


class Spider(object):
    def __init__(self):
        self.href_latest_articles = ''
        return


class SingleTask(object):
    u"""
    任务信息以对象属性方式进行存储

    """
    def __init__(self):
        self.kind = ''
        self.spider = Spider()
        self.book = InitialBook()
        return


class TaskPackage(object):
    u"""
    work_list: kind->single_task.href_index
    book_list: kind->single_task.book
    """
    def __init__(self):
        self.work_list = {}
        self.book_list = {}
        return

    def add_task(self, single_task=SingleTask()):
        if single_task.kind not in self.work_list:
            self.work_list[single_task.kind] = []
        self.work_list[single_task.kind].append(single_task.spider.href_latest_articles)

        if single_task.kind not in self.book_list:
            self.book_list[single_task.kind] = []
        self.book_list[single_task.kind].append(single_task.book)
        return

    def get_task(self):
        if Type.jianshu in self.book_list:
            self.merge_article_book_list(Type.jianshu)
        return self

    def merge_article_book_list(self, book_type):
        book_list = self.book_list[Type.jianshu]
        book = InitialBook()
        info_extra = [item.sql.info_extra for item in book_list]
        article_extra = [item.sql.article_extra for item in book_list]
        book.kind = book_type
        book.author_id = book_list[0].author_id
        book.sql.info = 'select * from jianshu_info where ({})'.format(' or '.join(info_extra))
        book.sql.article = 'select * from jianshu_article where ({})'.format(' or '.join(article_extra))
        book.sql.answer = 'select * from jianshu_article where ({})'.format(' or '.join(article_extra))
        self.book_list[book_type] = [book]
        return

    def is_work_list_empty(self):
        for kind in Type.type_list:             # 目前只有latest_article一种
            if self.work_list.get(kind):
                return False
        return True

    def is_book_list_empty(self):
        for kind in Type.type_list:
            if self.book_list.get(kind):
                return False
        return True
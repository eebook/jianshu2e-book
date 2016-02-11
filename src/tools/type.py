# -*- coding: utf-8 -*-


class Type(object):
    jianshu_article = 'jianshu_article'     # 类型是单篇的文章   TODO
    jianshu = 'jianshu'                     # 类型是简书文章的集锦

    jianshu_info = 'jianshu_info'

    jianshu_article_type_list = ['jianshu']

    info_table = {
        'jianshu_info': jianshu_info
    }

    type_list = [
        'jianshu',          # TODO, 目前只有latest_articles一种, 还可以写collections, notebook等等
    ]
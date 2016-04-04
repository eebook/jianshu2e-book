# -*- coding: utf-8 -*-
import json
import os

from src.tools.path import Path


class Config(object):
    u"""
    用于储存、获取设置值、全局变量值
    """
    # 全局变量
    update_time = '2016-01-01'  # 更新日期, TODO: 暂时没用到

    debug = True

    max_thread = 10         # 最大线程数
    picture_quality = 1     # 图片质量（0/1/2，无图/标清/原图）   TODO:暂时没有用到
    max_blog = 10           # 每本电子书中最多可以放多少个博客     TODO:暂时没有用到
    max_answer = 600        # 每本电子书中最多可以放多少篇文章

    max_try = 5             # 最大尝试次数
    timeout_download_picture = 10
    timeout_download_html = 5
    sql_extend_answer_filter = ''  # 附加到answer_sql语句后，用于对answer进行进一步的筛选（示例: and(agree > 5) ）

    article_order_by_desc = True     # 若为True, 最新的一篇排在第一

    @staticmethod
    def _save():
        with open(Path.config_path, 'w') as f:
            data = dict((
                (key, Config.__dict__[key]) for key in Config.__dict__ if '_' not in key[:2]
            ))
            json.dump(data, f, indent=4)
        return

    @staticmethod
    def _load():
        if not os.path.isfile(Path.config_path):
            return
        with open(Path.config_path) as f:
            config = json.load(f)
            if not config.get('remember_account'):
                return
        for (key, value) in config.items():
            setattr(Config, key, value)
        return
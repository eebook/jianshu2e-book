# -*- coding: utf-8 -*-

import urllib2
import re

from src.tools.match import Match
from bs4 import BeautifulSoup



import sys
reload(sys)
sys.setdefaultencoding("utf8")



def get_attr(dom, attr, defaultValue=""):
    u"""
    获取bs中tag.content的指定属性
    若content为空或者没有指定属性则返回默认值
    """
    if dom is None:
        return defaultValue
    return dom.get(attr, defaultValue)


def fix_html(content=''):
    content = content.replace('</br>', '').replace('</img>', '')
    content = content.replace('<br>', '<br/>')
    content = content.replace('href="//link.zhihu.com', 'href="https://link.zhihu.com')  # 修复跳转链接
    for item in re.findall(r'\<noscript\>.*?\</noscript\>', content, re.S):
        content = content.replace(item, '')
    return content

def get_tag_content(tag):
    u"""
    用于提取bs中tag.contents的内容
    需要对<br>进行预处理，将<br>换成<br/>,否则会爆栈，参考http://palydawn.blog.163.com/blog/static/1829690562012112285248753/
    """
    return "".join([unicode(x) for x in tag.contents])


jianshu_author_id = 'b1dd2b2c87a8'


article_href = 'http://www.jianshu.com/users/{}/latest_articles'.format(jianshu_author_id)
article_single_href = 'http://www.jianshu.com/p/4149a394ef88'

html = urllib2.urlopen(article_single_href)
content = html.read()
# print "content" + str(content)
soup = BeautifulSoup(content, "lxml")

content = soup.find("div", class_="preview")        # 这里需要改进, article_title没有用上, 需要改html模板
print content

# title = soup.find("title").get_text()
# print title

# article_id = str(soup.find("div", class_="share-group"))
# print article_id
# result = Match.jianshu_article_id(article_id)
# article_id = result.group('jianshu_article_id')
# print "now article_id???" + str(article_id)

# author_name = str(soup.find("a", class_="author-name").span.get_text())
# print author_name

# creator_id = str(soup.find("div", class_="author-info").find("a", class_="avatar")['href'][7:]) #.h3.a['href'][7:])
# print creator_id


# article_href_list = []
# article_list = soup.select('h4.title a')
# for item in range(len(article_list)):
#     article_href = 'http://www.jianshu.com' + str(get_attr(article_list[item], 'href'))
#     article_href_list.append(article_href)
#
# print u"article_href_list为???" + str(article_href_list)

# article_num = soup.select('ul.clearfix li b')
# if not article_num:
#     print u"没有找到文章的数量"
# article_num = article_num[2].get_text()      # 第3个是文章数量
# print article_num

# descirption = soup.select('p.intro')
# if not descirption:
#     print u"没有找到博主的描述"
# descirption = descirption[0].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
# print u"descirption为:" + str(descirption)

# creator_name = soup.select('div.basic-info h3 a')
# # print u"creator_name???" + str(creator_name)
# if not creator_name:
#     print (u"没有找到博主姓名")
# creator_name = creator_name[0].get_text().replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', '')
# print "creator_name为:" + str(creator_name)

# creator_id = str(soup.find("div", class_="basic-info").h3.a['href'][7:])
# # creator_id = get_attr(creator_id[0], 'data-user-slug')
# print creator_id
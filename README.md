# jianshu2e-book

## 简介
爬取[简书](http://www.jianshu.com)上的文章，制作成Epub格式的电子书（同时生成html格式文件）  
</br>
例如，将[王垠](http://www.jianshu.com/users/b1dd2b2c87a8/latest_articles)在简书上的所有文章爬取下来制作电子书：
![wangyinepub](http://7xi5vu.com1.z0.glb.clouddn.com/jianshuepub_wangyin.png?imageView/2/w/619/q/90)

网页版：   

![wangyinweb](http://7xi5vu.com1.z0.glb.clouddn.com/jianshujianshuarticle.png?imageView/2/w/619/q/90)

## 开发环境
Mac 10.11   
Python 2.7.11    
BeautifulSoup 4    
PyCharm CE 5.0.3  
目前完成度不高，bug还比较多，Win，Linux平台下还没有测试过，有可能存在问题。

## 使用说明 
1. 将简书博主地址放入项目文件夹目录的ReadList.txt中，例如：  
![readlist](http://7xi5vu.com1.z0.glb.clouddn.com/jianshureadlist.png?imageView/2/w/619/q/90)

2. 执行：  
```shell
$ python jianshu2e-book.py
```

稍等片刻，html和Epub格式的电子书会生成在「生成的电子书」文件夹中。

## 依赖
 * [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)(已经放在项目目录中，不需要下载)
 * [lxml](http://lxml.de/)     
  
 ```shell
$ pip install lxml
```  

## 项目说明
**该项目只是[ZhihuHelp](https://github.com/YaoZeyuan/ZhihuHelp)的简书版本，目前大量用到[ZhihuHelp](https://github.com/YaoZeyuan/ZhihuHelp)项目的代码，再次表示感谢。也请大家多多支持该项目作者[姚泽源](https://github.com/YaoZeyuan)同学。**

## TODO list  

0. 支持简书的「专题」,「文集」爬取 
1. 效率问题，程序还需要优化
2. 页面的样式还需要改进（如：封面，简介，标题，博主logo等）  
3. 博文评论的数量  
4. 博文更新时间    
5. 图形界面
6. 程序接口  
7. 分卷制作电子书， 多个博主的文章放在同一本书中
8. ....

## License
[MIT](http://opensource.org/licenses/MIT)
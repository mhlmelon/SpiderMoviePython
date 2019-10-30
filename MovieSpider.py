# encoding: utf-8
import urllib2,re
from DBUtil import MysqldbHelper
url = 'http://www.dygang.com/ys/index.htm'
def gethtml(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    html = response.read()
    html = html.decode('gbk').encode('utf-8')
    return html

def getMovieDetail(content):
    detil_list = re.findall('<a href="(.*?)" target="_blank" class="classlinkclass">.*?</a>', content)
    db = MysqldbHelper()
    for m in detil_list:
        print m
        movieDetailContent = gethtml(m)
        # print movieDetailContent
        #电影名称
        movieName_list = re.findall('<a href="%s"><strong>《(.*?)》下载</strong></a>' % m, movieDetailContent)
        # 图片
        image_list1 = re.findall('<img alt="" src="(.*?)" />', movieDetailContent)
        # 下载地址
        cili_downloadUrl_list = re.findall('磁力：<a href="(.*?)">', movieDetailContent)
        dianlv_downloadUrl_list = re.findall('电驴：<a href="(.*?)">', movieDetailContent)
        #简介
        introduction_list1 = re.findall('◎简　　介&nbsp;</p>(.*?)</p>">', movieDetailContent)
        introduction_list2 = re.findall('◎简　　介&nbsp;</p>.*?<p>(.*?)</p>">', movieDetailContent)
        introduction_list3 = re.findall('◎简　　介<br />(.*?)</p>">', movieDetailContent)
        introduction_list4 = re.findall('简介<br />(.*?)</p>">', movieDetailContent)
        introduction_list5 = re.findall('◎简　　介　<br />(.*?)</p>">', movieDetailContent)

        name = ''
        imageUrl = ''
        downloadUrl = ''
        introduction = ''
        detailUrl = ''
        if len(movieName_list) > 0 :
            name = movieName_list[0];
        if len(image_list1) > 0:
            imageUrl = image_list1[0]

        if len(cili_downloadUrl_list) > 0:
            downloadUrl = '磁力链接:%s' % cili_downloadUrl_list[0]
        if len(dianlv_downloadUrl_list) > 0:
            downloadUrl = '%s\r\n电驴链接:%s' % (downloadUrl,dianlv_downloadUrl_list[0])

        if len(introduction_list1) > 0:
            introduction = introduction_list1[0]
        if len(introduction_list2) > 0:
            introduction = introduction_list2[0]
        if len(introduction_list3) > 0:
            introduction = introduction_list3[0]
        if len(introduction_list4) > 0:
            introduction = introduction_list4[0]
        if len(introduction_list5) > 0:
            introduction = introduction_list5[0]

        detailUrl = m

        print '电影名称:%s' % name
        print '电影详情:%s' % detailUrl
        print '图片介绍:%s' % imageUrl
        print '磁力链接:%s' % downloadUrl
        print '简介:%s' % introduction

        if len(name) > 0:
            #插入数据库
            sql = "insert into movie(`title`, `pic_url`, `target_url`, `introduction`, `download_url`, `create_time`) values(%s,%s,%s,%s, %s,now())"
            params = (name, imageUrl, detailUrl, introduction, downloadUrl)
            count = db.updateByParam(sql, params)
            if count > 0:
                print '数据库插入成功'


for i in range(1, 2):
    if i > 1:
        url = "http://www.dygang.com/ys/index_%d.htm" % (i)
    print "正在爬取当前第%d页数据..." % i
    # print url
    content = gethtml(url)
    getMovieDetail(content)
    # print (content)



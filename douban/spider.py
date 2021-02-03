# -*- coding:utf-8 -*-
# @Time:
# @Author:zzh
# @File:.py
# @MobilePhone:18186149507

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定url，获取网页数据
import xlwt  # 进行Excel操作
import pymysql  # 进行MySQL数据库操作
import urllib  # 一般使用这个包进行网页爬取


def main():
    baseurl = "https://movie.douban.com/top250?start="
    askUrl(baseurl)
    datalist = getData(baseurl)
    print(datalist)
    savepath=".\\豆瓣电影Top250.xls"
    saveData(datalist,savepath)

#创建正则表达式
findLink=re.compile(r'<a href="(.*?)">')  #影片链接
findTitle=re.compile(r'<span class="title">(.*?)</span>')  #电影名
findScore=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')  #评分
findSeveralNumber=re.compile((r'<span>(\d*)人评价</span>'))  #评价数
findInq=re.compile(r'<span class="inq">(.*)</span>')  #概况
findBd=re.compile(r'<p class="">(.*?)</p>',re.S)  #影片相关内容,re.S:让换行符包含在字符中


# 数据解析
def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 总共需要获取十次
        url = baseurl + str(i * 25)  # 一次获取25条
        html = askUrl(url)

        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            data=[] #包含一部电影的所有信息
            item=str(item)
            link=re.findall(findLink,item)  #筛选符合规定的字符串
            data.append(link)  #添加电影链接
            title=re.findall(findTitle,item)[0]
            data.append(title)  #添加电影名称
            score=re.findall(findScore,item)[0]
            data.append(score)  #添加电影评分
            SeveralNumber=re.findall(findSeveralNumber,item)[0]
            data.append(SeveralNumber)  #添加电影评论人数
            inq=re.findall(findInq,item)
            data.append(inq)  #添加电影概述
            bd=re.findall(findBd,item)[0]
            bd=re.sub('<br(\s+)?/>(\s+)?'," ",bd) #去掉<br/>
            bd=re.sub('&nbsp;'," ",bd)  #去掉&nbsp;
            data.append(bd.strip())#去掉前后空格，添加电影相关信息

            datalist.append(data);  #把处理好的一部电影信息放入datalist

    return datalist

# 保存数据
def saveData(datalist,savepath):
    workbook=xlwt.Workbook(encoding="utf-8",style_compression=0)
    worksheet=workbook.add_sheet("豆瓣电影Top250",cell_overwrite_ok=True)
    col=("影片链接","名称","评分","评论人数","概况","相关内容");
    for i in range(0,6):
        worksheet.write(0,i,col[i]);  #第一列列名
    for i in range(0,250):
        print("第%d条"%(i+1));
        data=datalist[i]
        for j in range(0,6):
            worksheet.write(i+1,j,data[j])
    workbook.save("豆瓣电影Top250.xls")
# 得到一个指定url的网页内容
def askUrl(url):
    # 请求头，相当于披上一层衣服，告诉豆瓣服务器请求的是一个常规浏览器而不是Python程序
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
        return html
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)


if __name__ == "__main__":  # 当程序执行时候
    # 调用函数
    main()
    print("爬取完毕")

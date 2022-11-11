# 对wiki文件的格式转换

from gensim.corpora.wikicorpus import extract_pages,filter_wiki
import bz2file
import re
from tqdm import tqdm
from CommonTools.JsonTool import *
from CommonTools.TextTool import ConvertChineseSimplified
from MailAutoSend.EmailTool import send_email
def save_promote(s):
    """
    仅保留[[]]或[]的格式
    将繁体转化成简体
    """
    s = re.sub(':*{\|[\s\S]*?\|}', '', s)
    s = re.sub('<gallery>[\s\S]*?</gallery>', '', s)
    s = re.sub('(.){{([^{}\n]*?\|[^{}\n]*?)}}', '\\1[[\\2]]', s)
    s = filter_wiki(s,promote_remaining=False)
    s = re.sub('\* *\n|\'{2,}', '', s)
    s = re.sub('\n+', '\n', s)
    s = re.sub('\n[:;]|\n +', '\n', s)
    s = re.sub('\n==', '\n\n==', s)
    return s

def process_wiki_page(s):
    """
    截取网页的五项
    结构：
        infobox
        简介
        其他文段：用 == 主题 == 分割
        所属分类:列表
        重定向：如果有的话
    """
    item=dict()

    # 添加重定向
    redirect=re.findall("{{redirect.*?}}",s,re.I)
    if redirect!=[]:
        redirect=redirect[0][2:-2].split("|")[1:]
        item["redirect"]=redirect

    
    page=s
    s=re.split("==.*==", s)
    head=s[0]
    tail=s[-1]
    item["summary"]=save_promote(head)
    infobox=re.search("\{\{Infobox[\s\S]*\}\}",head)
    
    if infobox:
        infobox=infobox.group()
        bihuan=1
        for i in range(2,len(infobox)-2):
            if infobox[i:i+2]=="{{":bihuan+=1
            elif infobox[i:i+2]=="}}":bihuan-=1
            if bihuan==0:
                infobox=infobox[:i+2]
        item["infobox"]=infobox
    category=re.findall("\[\[Category.*?\]\]",tail)
    item["category"]=category
    para=page.replace(head,"")
    item["para"]=save_promote(para)
    return item

def wiki_process(bz2_file,json_file):

    # 该工具用来遍历wiki文件，不用全部打开文件再操作
    wiki = extract_pages(bz2file.open(bz2_file))
    w = tqdm(wiki, desc=u'已获取0篇文章')
    cs=ConvertChineseSimplified()
    count=0
    data=[]
    for item in w:
        if not re.findall('^[a-zA-Z]+:', item[0]) and item[0] and not re.findall(u'^#', item[1]):   # 一处解释性页面
            title=item[0]               # item[0]表示标题
            page=item[1]                # item[1]表示文本内容
            # 转换成简体
            title=cs.A2B(title)
            page=cs.A2B(page)
            # 转换页面格式
            page_info=process_wiki_page(page)
            page_info["name"]=title
            data.append(page_info)
            # 计数
            count+=1
            w.set_description(u'已获取%s篇文章'%count)
    save_json(data,json_file)

    return u'已获取%s篇文章'%count


def build_country_vocab(filename):
    """建立国家的重定向字典"""


    data=load_json(filename)
    country_vocab=dict()
    for key,values in data.items():
        for value in values:
            # 含有中英文即可，不包括数字和其他字符
            if re.search("[\u4e00-\u9fa5a-zA-Z]",value):
                country_vocab[value]=key
    save_json(country_vocab,"data/country_vocab.json")

def find_country(filename):
    """找到国家的英文缩写"""
    """
    共找到36个
    
    不全的原因：
        有一个专门的重定向网页连接到国家网页，而不是存储在国家网页的redirect条目下,例如 https://zh.wikipedia.org/wiki/FRA
        而这写重定向网页能在连接节点里面找到，这需要手动的消歧

        先不考虑国家与国家之间消歧的问题，先把没有建立连接的redirect条目建立起来

        数据很少，完全可以手写,bu

    """
    data=load_json(filename)

    country_data=dict()

    for item in tqdm(data):
        if "infobox" in item:
            infobox=item["infobox"]
            if re.findall("country",infobox[:30],re.I)!=[]:
                if "redirect" in item:
                    country_data[item["name"]]=item["redirect"]
    save_json(country_data,"data/country_data.json")



if __name__=="__main__":

    info=wiki_process(bz2_file="data/zhwiki-20220801-pages-articles-multistream.xml.bz2",json_file="data/wiki_page.json")
    send_email(info)
    # find_country("data/wiki_page.json"）)
    # build_country_vocab("data/country_data.json")

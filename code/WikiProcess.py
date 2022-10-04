
# Description : 抽取出wiki页面的四项，保存到新文件中

from gensim.corpora.wikicorpus import extract_pages,filter_wiki
import bz2file
import re
from tqdm import tqdm
from .CommonTools.TextTool import ConvertChineseSimplified
from .CommonTools.JsonTool import *
def save_promote(s):
    """仅保留[[]]或[]的格式"""
    s = re.sub(':*{\|[\s\S]*?\|}', '', s)
    s = re.sub('<gallery>[\s\S]*?</gallery>', '', s)
    s = re.sub('(.){{([^{}\n]*?\|[^{}\n]*?)}}', '\\1[[\\2]]', s)
    s = filter_wiki(s,promote_remaining=False)
    s = re.sub('\* *\n|\'{2,}', '', s)
    s = re.sub('\n+', '\n', s)
    s = re.sub('\n[:;]|\n +', '\n', s)
    s = re.sub('\n==', '\n\n==', s)
    s=ConvertChineseSimplified.A2B(s)  #繁体转简体，需要有Opencc库
    return s

def process_wiki_page(s):
    """
    结构：
        infobox
        简介
        其他文段：用 == 主题 == 分割
        所属分类:列表
    """
    item=dict()
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

def extract_4_item_of_wiki_bz2_file(bz2_file,des_file):
    json_file="data/wiki_page_1.json"
    "data/zhwiki-20220801-pages-articles-multistream.xml.bz2"
    wiki = extract_pages(bz2file.open(bz2_file))
    w = tqdm(wiki, desc=u'已获取0篇文章')
    count=0
    data=[]
    for item in w:
        if not re.findall('^[a-zA-Z]+:', item[0]) and item[0] and not re.findall(u'^#', item[1]):
            title=item[0]               # item[0]表示标题
            page=item[1]                # item[1]表示文本内容
            count+=1
            page_info=process_wiki_page(page)
            page_info["name"]=title
            data.append(page_info)
            w.set_description(u'已获取%s篇文章'%count)
    save_json(data,des_file)

if __name__=="__main__":
    extract_4_item_of_wiki_bz2_file("data/zhwiki-20220801-pages-articles-multistream.xml.bz2","data/wiki_page_4_item.json")

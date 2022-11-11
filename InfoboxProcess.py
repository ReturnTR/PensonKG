# coding=utf-8
# Time : 2022/10/5 13:54
# Description : 将infobox内容格式化，变成字典的形式

from CommonTools.FileStreamTool import *
from CommonTools.JsonTool import *

def item_fun_infobox(item):
    """infobox格式化函数"""

    def process_infobox(s):#, templete):
        """
        目标：
            类型：
            {
                属性名称：对应中文属性名称
            }

        :param s:
        :return:
        """
        templete_dict = dict()

        new_infobox = dict()
        s = re.sub("<!--.*?-->", "", s)
        s = re.sub("<ref>.*?</ref>", "", s)
        s = s.replace("\n*", "")
        s = s.split("\n")
        s = [i.strip() for i in s]
        s = [i for i in s if i]
        for item in s:
            if item[0] == "|":  # 是一个项
                item = item[1:]
                item = item.split("=")
                if len(item) > 2: item = [item[0], "=".join(item[1:])]
                item = [i.strip() for i in item]
                item = [i for i in item if i]
                if len(item) < 2: continue
                # 只将templete里面的属性值包含在内？不，进行特殊标记

                flag = True
                # for t in templete:
                #     if item[0] in templete[t]["trigger"] or item[0] == t:
                #         flag = False
                #         new_infobox["__" + item[0]] = item[1]
                if flag:
                    new_infobox[item[0]] = item[1]
        return new_infobox

    global templete
    item["infobox"]=process_infobox(item["infobox"]) #,templete)
    return item


def infobox_process(person_page,infobox_dir):
    templete = load_json("data/statistics_data/infobox_templete.json")
    FileStream.json_stream(person_page,infobox_dir,item_fun_infobox)




if __name__=="__main__":
    infobox_process("data/temp_data/person_page.json","data/temp_data/person_infobox.json")
    print("done")
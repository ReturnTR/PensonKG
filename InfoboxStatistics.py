# coding=utf-8
# Time : 2022/10/5 13:54
# Description : 统计infobox的信息


from CommonTools.BasicTool import *
from CommonTools.TextTool import *


def infobox_process(s):
    new_s = []
    s = s.split("\n")
    for item in s:
        if item:
            if "{{{" in item:
                if item[:2] == "[[":
                    continue
                item = item.replace("{{{", " ").replace("}}}", " ").strip()
                item = item.split(" ")
                item = [i for i in item if i]
                new_s.append(item)
            elif item[0]=="|":
                item = item[1:]
                item = item.split("=")
                item = [i.strip() for i in item]
                item = [i for i in item if i]
                # if len(item)>1:
                #     if len(item)>2:item=[item[0],"=".join(item[1:])]
                #     item[1]=item[1][4:-3]
                #     item[1]=re.sub("（.*?）","",item[1])
                #     format=re.search("\{\{.*?}}",item[1])
                #     if format:
                #         format=format.group()
                #         item[1]=item[1].replace(format,"")
                #         item.append(format)
                new_s.append(item)
            elif " " in item:
                item=item.split()
                if len(item)==2:
                    if GetPartialOnly.English_letter_and_underline(item[1])==item[1] and GetPartialOnly.Chinese(item[0])==item[0]:
                        new_s.append(item)

    return new_s



def main():

    data=load_excel("data/人物图谱Schema.xlsx","infobox模板")
    data=data[:2]
    infoboxes_up=[]
    infoboxes_down=[]
    down_infobox_two = []
    infobox_dict=DictCount()
    for i in range(len(data[0])):
        up_infobox=data[0][i]
        down_infobox=data[1][i]
        up_infobox=infobox_process(up_infobox)
        if down_infobox is not None and down_infobox:
            down_infobox=infobox_process(down_infobox)
            if down_infobox is not None and down_infobox:
                for i in down_infobox:
                    if len(i) == 2:
                        if GetPartialOnly.Chinese(i[0]) == i[0] and GetPartialOnly.English_letter_and_underline(i[1])==i[1]:
                            down_infobox_two.append(i)
        infoboxes_up.append(up_infobox)
        infoboxes_down.append(down_infobox)
        for i in up_infobox:
            if isinstance(i,list):
                i=i[0]
                infobox_dict.add(i)


    infobox_dict=infobox_dict.get()

    print(len(infobox_dict))

    save_json(infobox_dict,"data/attributes.json")
    # 两个infobox对照看才能有用
    # 第二行只保留有效的中文信息 还有数字信息

    # save_json(infoboxes_up,"data/infoboxes_up.json")
    #
    # save_json(infoboxes_down,"data/infoboxes_down.json")
    #
    # save_json(down_infobox_two,"data/infoboxes_down_two.json")

    # 总结

    res=dict()
    alias2name=dict() # 描述归一属性的字典
    for item in down_infobox_two:
        if item[1] not in alias2name:
            alias2name[item[1]]=set()
            alias2name[item[1]].add(item[0])
            alias2name[item[1]].add(item[1])

        else:
            alias2name[item[1]].add(item[0])
    print("有双重含义的数量：",len(alias2name))
    not_in_alias_list=[]

    for i in range(len(infoboxes_up)):
        up_infobox=infoboxes_up[i]
        down_infobox=infoboxes_down[i]

        for j in up_infobox:
            if GetPartialOnly.English_letter_and_underline(j[0]):
                if j[0] in res:
                    res[j[0]]["count"]+=1
                else:
                    res[j[0]]={"trigger":set(),"count":1,"explain":""}
                    if j[0] in alias2name:
                        res[j[0]]["trigger"]=alias2name[j[0]]
                    else:

                        not_in_alias_list.append(j[0])
                if len(j) > 1:
                    res[j[0]]["explain"] += j[1]

            elif GetPartialOnly.Chinese(j[0]):
                flag=1
                for attribute in alias2name:
                    if j[0] in alias2name[attribute]:
                        flag=0
                        if attribute in res:
                            res[attribute]["count"]+=1
                            if len(j) > 1:res[attribute]["explain"] += j[1]
                        else:
                            res[attribute]={"trigger":alias2name[attribute],"count":1,"explain":""}
                            if len(j) > 1: res[attribute]["explain"] += j[1]
                if flag:
                    not_in_alias_list.append(j[0])
                    if j[0] in res:
                        res[j[0]]["count"]+=1
                    else:
                        res[j[0]]={"trigger":set(),"count":1,"explain":""}
                    if len(j) > 1: res[j[0]]["explain"] += j[1]
    print(len(count_list(not_in_alias_list)))
    for i in res:
        res[i]["trigger"]=list(res[i]["trigger"])

    res={k: v for k, v in sorted(res.items(), key=lambda item: item[1]["count"], reverse=True)}
    save_json(res,"res.json")




get_infobox_statistics("data/person_infobox_1.json","data/person_key_count.json")
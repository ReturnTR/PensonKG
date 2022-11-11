# coding=utf-8
# Time : 2022/10/31 13:25
# Description : 抽出重名实体


"""
目标
找出所有重名的实体，并表明有几个分支

流程
1.找到含有额外信息名字，例如姚明（篮球协会主席）,该名字可能成为重名实体
2.将这些实体的名字归类，变成一个集合字典，键为全体名称，值为所有的细分名称
{
    "刘雯":["刘雯 (模特)","刘雯 (主持人)"]
}
"""
from CommonTools.JsonTool import *
from tqdm import tqdm
from CommonTools.BasicTool import count_dict_list,print_dict
from CommonTools.FileStreamTool import FileStream

def get_duplicated_name_dict(filename,save_filename):
    """
    以括号为标志，寻找带有infobox的重名实体
    :param filename:
    :return:
    """
    def del_label(name):
        """去掉额外信息"""
        name=name.replace(" ","")
        name=name.split("(")[0]
        return name
    data=load_json(filename)
    data=[i["name"] for i in data]
    duplicated_names_dict=dict()
    for name in tqdm(data):
        if "(" in name:
            no_label_name=del_label(name)
            if no_label_name in duplicated_names_dict:
                duplicated_names_dict[no_label_name].append(name)
            else:
                duplicated_names_dict[no_label_name]=[name]
    save_json(duplicated_names_dict,save_filename)

def expand_duplicated_name(duplicated_name_dict_file,expand_file,max_len):
    """
    同样用括号匹配
    :param duplicated_name_dict_file:
    :param expand_file:
    :param max_len: 匹配最大长度
    :return:
    """
    duplicated_name_dict=load_json(duplicated_name_dict_file)
    duplicated_name_set=set(duplicated_name_dict.keys())
    expand_data=load_json(expand_file)
    expand_data=[i["name"] for i in expand_data]
    for name in tqdm(expand_data):
        if "(" in name:
            sub_name=name.replace(" ","").split("(")[0]
        elif "（" in name:
            sub_name = name.replace(" ", "").split("（")[0]
        else:
            sub_name=name
        if sub_name in duplicated_name_set:
            if name not in duplicated_name_dict[sub_name]:
                duplicated_name_dict[sub_name].append(name)

    save_json_list_in_line(duplicated_name_dict,"data/duplicated_names_dict_expand.json")


def fun_get_redirect(item):
    if "redirect" in item:
        res=[item["name"]]
        res.extend(item["redirect"])
        return res



if __name__ == "__main__":
    # get_duplicated_name_dict("data/kg_data/wiki_page.json","data/temp_data/wiki_page_duplicated.json")
    # expand_duplicated_name("data/duplicated_names_dict.json","data/wiki_page_1294978.json",6)
    # print_dict(count_dict_list(load_json("data/duplicated_names_dict.json")))

    FileStream.json_stream("data/kg_data/wiki_page.json","data/temp_data/wiki_page_redirect.json",fun_get_redirect)


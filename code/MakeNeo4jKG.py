# coding=utf-8
# Time : 2022/10/24 14:16
# Description : 构建neo4j图谱
from CommonTools.Neo4jTool import *
from CommonTools.JsonTool import *
from CommonTools.CSVTool import *
from tqdm import tqdm

def json_file_2_csv(filename):
    """
    为所有实体创造csv文件，便于导入到数据库
    :param filename: json文件
    :return: csv文件
    在建立好CSV文件后，将其放入到Neo4j项目下的import文件夹下，然后输入如下命令：
    `:auto USING PERIODIC COMMIT 300 LOAD CSV FROM "file:///filename.csv" AS line`
    """
    def change(s):
        if isinstance(s,list):s="**".join(s)
        s=s.replace('"',"“").replace("\\","\\\\").replace("\n","\\n")
        s='"'+s+'"'
        return s

    data=load_json(filename)
    csv_file=[]
    attributes=["name","infobox","category","summary","para"]

    csv_file.append(attributes)

    for item in tqdm(data):
        temp_values=[]
        for attribute in attributes:
            if attribute in item:
                value=change(item[attribute])
                if value=="":print(item)
                temp_values.append(value)
            else:
                temp_values.append('""')
        csv_file.append(temp_values)

    save_csv(csv_file,filename[:-5]+".csv")

def put_person_into_kg(filename):
    """
    将所有抽取后的人物进行导入
    包括确定任务标签，扩充人物属性
    :param filename:人物json文件
    :return: 导入

    注：再导入前需要将节点的name属性添加索引，以便快速查找，代码为 `CREATE INDEX ON : Person (name)`
    """

    data=load_json(filename)
    db=Neo4jDB('http://127.0.0.1:7474',"neo4j", "zyliu")
    for item in tqdm(data):
        if "'" in item["name"]:continue
        if "infobox" in item:
            db.add_attribute_value(item["name"],item["infobox"])
        db.add_label(item["name"],"person")

def add_person_relation_into_kg(filename):

    db=Neo4jDB('http://127.0.0.1:7474',"neo4j", "zyliu")
    def process_tail(s):
        if "|" in s:
            s=s.split("|")[0]
        return s
    data=load_json(filename)
    for item in tqdm(data):
        if "relations" in item and item["relations"]!={}:
            for attribute,value in item["relations"].items():
                if isinstance(value,list):
                    for tail in value:
                        db.add_relation(item["name"],process_tail(tail),attribute)
                else:
                    db.add_relation(item["name"], process_tail(value), attribute)



if __name__=="__main__":

    pass

    # 构建流程

    # 添加所有节点
    json_file_2_csv("data/wiki_page_1294978.json")
    # 添加人物及其属性
    put_person_into_kg("data/person_infobox_1.json")
    # 添加关系
    add_person_relation_into_kg("data/person_infobox_with_relation.json")
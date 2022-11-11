# coding=utf-8
# Time : 2022/11/4 13:43
# Description : 构建图谱的代码

"""
流程：
    1. 导入Wiki中所有的128万个节点，属性值包括 name，infobox，summary，para，category，redirect（有的话）这些属性值不能被改变，尤其是name，不能被属性值里面的name替换
        包括：
            - 建立索引unknown和person
            - 将节点导入，类型设置为unknown

    2. 直接导入配置好的人物文件进行人物图谱的构建
        包括：
            - 添加属性值
            - 建立人物关系
            - 建立非人物实体，并于该实体建立关系（若存在的话直接建立）

"""



from CommonTools.JsonTool import *
from tqdm import tqdm
from CommonTools.Neo4jTool import *
import pdb


def add_relation_labels(filename,unknown_label="unkuown"):
    data=load_json(filename)
    neo4j = Neo4jDB('http://127.0.0.1:7474', "neo4j", "zyliu")
    for item in tqdm(data[8708:]) :
        if "'" in item["name"]: continue  # 过滤无效名字
        if item["relations"]!=[]:
            # [关系名,实体类型,属性值]
            for relation in item["relations"]:
                relation_name=relation[0]
                tail_label=relation[1]
                tail_name=relation[2]
                if "\\" not in tail_name and tail_name!="" and "'" not in tail_name:
                    neo4j.add_label_CQL(unknown_label,tail_name,tail_label)


def add_page_into_kg(filename, labels,kg_name="personkg"):
    """
    导入文件数据
    :param filename: 字典列表
    :param labels: 标签
    :return:
    """
    neo4j = Neo4jDB('http://127.0.0.1:11004', "neo4j", "zyliu")
    # neo4j.execute_CQL(":use {}".format(kg_name))
    for label in labels:
        neo4j.execute_CQL("CREATE INDEX ON :{}(name)".format(label))
    data=load_json(filename)
    for item in tqdm(data):
        neo4j.add_node(neo4j.create_node(labels, item))

def construct(filename,unknown_label="unkuown",country_vocab_file="data/country_vocab.json"):
    data=load_json(filename)
    country_vocab=load_json(country_vocab_file)
    neo4j = Neo4jDB('http://127.0.0.1:7474', "neo4j", "zyliu")

    """
    :use personkg
    CREATE INDEX ON :{}(name)'.format("unknown")
    CREATE INDEX ON :{}(name)'.format("person")
    """

    for item in tqdm(data):
        if "'" in item["name"]: continue  # 过滤无效名字

        neo4j.add_attribute_value(unknown_label,item["name"],item["infobox"])
        node = neo4j.search_node_by_name(unknown_label, item["name"])
        # 添加人物标签
        # node.add_label("person")

        for key, value in item["infobox"].items():
            if not isinstance(value,list):value = value.replace("'", "").replace('"', "")
            key = key.replace("-", "_").replace("(", "_").replace(")", "_")

            # 添加人物属性
            node[key]=value
        neo4j.update_node(node,unknown_label)
        node=neo4j.add_label(node,"person")

        # 添加人物与非人物的关系，没有标签的添加标签

        if item["relations"]!=[]:
            # [关系名,实体类型,属性值]
            for relation in item["relations"]:
                relation_name=relation[0]
                tail_label=relation[1]
                tail_name=relation[2]

                # 为国家特殊查找结点名称
                if tail_label=="国家":
                    if tail_name in country_vocab:
                        tail_name=country_vocab[tail_name]

                # 先查找该节点是否存在
                tail_node = neo4j.search_node_by_name(unknown_label, tail_name)
                if tail_node and tail_node is not None:

                    # 添加标签
                    tail_node.add_label(tail_label)
                    neo4j.update_node(tail_node, unknown_label)
                    # 进建立关系
                    relation_node = Relationship(node, relation_name, tail_node)
                    neo4j.add_relation(relation_node)













if __name__ == "__main__":
    add_page_into_kg("data/wiki_page_1_redirect.json",labels=["unknown"],kg_name="personkg")

    # add_relation_labels("data/person_infobox_2_modify.json")

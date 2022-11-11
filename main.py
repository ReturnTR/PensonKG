
from CommonTools.JsonTool import get_infobox_statistics

# 全部流程
from WikiProcess import wiki_process
from GetPersonViaInfobox import get_person_via_infobox
from InfoboxProcess import infobox_process
from AttributeFilter import modify_infobox
from KG import *

if __name__=="__main__":


    wiki_process(bz2_file="data/zhwiki-20220801-pages-articles-multistream.xml.bz2",json_file="data/kg_data/wiki_page.json") # 2h
    print("get_person_via_infobox")
    get_person_via_infobox("data/kg_data/wiki_page.json", "data/temp_data/person_page.json") # 2m 20s
    print("infobox_process")
    infobox_process("data/temp_data/person_page.json","data/temp_data/person_infobox.json") # 5s
    print("modify_infobox")
    modify_infobox("data/hand_made_data/Schema.xlsx","data/temp_data/person_infobox.json","data/kg_data/person_page.json") # 1m 33s

    # get_infobox_statistics("data/temp_data/person_infobox.json","data/person_key_count.json")

    # get_infobox_statistics("data/kg_data/person_page.json","data/person_key_count.json")



# 未完成
"""
统计信息
重名实体
国家节点关系建立
"""





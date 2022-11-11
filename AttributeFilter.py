# coding:utf-8
from CommonTools.TextTool import *
from CommonTools.JsonTool import *
from CommonTools.ExcelTool import *
from CommonTools.Neo4jTool import *
from CommonTools.BasicTool import DictCount,sort_dict
from CommonTools.DrawTool import Draw
import re
from tqdm import tqdm

cs = ConvertChineseSimplified()

# 对所有属性进行修改
# 流程
"""
输入：初步抽取的infobox
输出：图谱

对每一个人物
对于每一个预定义属性

"""


def attribute_name_process(name):
    """对属性名称的统一修改"""
    return cs.A2B(name.lower())  # 小写+简体

def attribute_value_process(value):
    """对属性值进行统一的修改"""
    return value.replace('"',"'")

def load_attribute_config(excel_file):
    data = load_excel(excel_file)
    # 0.名称 1.别名	2.实体名称	3.是否为人物关系	4.抽取方法	5.数量占比	6.中文名

    # 先对名字进行字符串格式修改
    for item in data:
        if item[0] is None: continue
        item[0] = attribute_name_process(item[0])
        if item[1] is not None:
            item[1] = attribute_name_process(item[1])

    trigger2name = dict()
    name2info = dict()  # 把数据换成可以索引的字典

    for item in data:
        if item[0] is None: continue
        if item[1] is not None:
            item[1] = item[1].split(",")


        # 将名称更换为中文名（如果有的话）
        if item[6] is not None:
            if item[1] is not None:
                item[1].append(item[0])
            else:
                item[1] = [item[0]]
            item[0] = item[6]

        # 将列表变成字典，以便索引，
        name2info[item[0]] = {"entity": item[2], "relation": item[3], "fun": item[4]}

        # 同时将触发词与键连接起来
        if item[1] is not None:
            for i in item[1]: trigger2name[i] = item[0]
        else:
            trigger2name[item[0]] = item[0]

    return trigger2name, name2info


def modify_infobox(excel_file, person_filename,save_filename):
    trigger2name, name2info = load_attribute_config(excel_file)
    trigger_set = set(trigger2name.keys())
    data = load_json(person_filename)
    af=AttributeFilter()
    for item in tqdm(data):  # 对item进行原地修改

        # 关系 添加[关系名,实体类型,属性值]
        item["relations"] = []

        new_infobox = {}  # 更新infobox
        for key, value in item["infobox"].items():  # 对infobox里的每一个属性进行检查
            key = attribute_name_process(key)  # 标准处理
            if key[:2]=="__":key=key[2:]
            key=re.sub("[0-9]","",key)
            if key in trigger_set:
                name = trigger2name[key]
                info = name2info[trigger2name[key]]
                if info["fun"] is not None:
                    value=attribute_value_process(value)

                    value = af.call(info["fun"], value)  # 属性值处理

                """
                支持多个属性的添加，需要限定：
                    属性值：字符串，一维列表，None，有列表的属性必须一开始就是列表，空列表也可以
                    关系：列表（可以为空，但不能有None）
                """

                # 跳过空的情况
                if value is None or value == [] or value== "":continue

                # 处理实体
                if info["entity"]:
                    for i in value:
                        item["relations"].append([name, info["entity"], i])
                # 处理关系
                elif info["relation"]:
                    for i in value:
                        item["relations"].append([name, "person", i])
                # 处理属性
                else:
                    name="__"+name
                    if name in new_infobox:
                        try:
                            if isinstance(new_infobox[name],list): new_infobox[name].extend(value)
                            else:new_infobox[name]+=value
                        except TypeError:
                            print(name,new_infobox[name],value)
                    else:
                        new_infobox[name] = value
            else:
                new_infobox[key] = value

        item["infobox"] = new_infobox

    save_json(data, save_filename)


"""
名称：修改程序的入口函数名
"""

class AttributeFilter():


    class WikiLabels():
        """
        针对特定的标签所做的事
        一次只能处理一个标签
        标签类型：{{xxxx}}
        """

        def process(self, s):

            # 识别特定标识，连接句柄
            cmd = [
                ["hlist", None],  # {{hlist|工程师|教授}}, 表示普通的列表
                ["link-ja", None],  # 该标签表示为一个日本wiki标签  {{link-ja|黑澤久雄|黒澤久雄}}
                ["Plainlist", None],  # 一个列表，中间没有"|"分割，用的是"\n*", 不过这个已经被截取infobox的操作消除了
                ["flagicon", self.flag_icon]
            ]

            for item in cmd:
                if item[0] in s:
                    s = s[2:-2]  # 去掉前后的括号,开始接下来的操作
                    if item[1] is not None:
                        # 自定义方法
                        s = item[1](s)
                        return s

                    else:
                        s = s.replace(item[0], "").replace("|", "、")
                        # s = s.split("|")
                        # s = [i for i in s if i]
                        return s

            return s

        def match_process(self, matched):
            s = matched.group()
            s = self.process(s)
            return s

        def flag_icon(self, s):
            return s

    @staticmethod
    def br_split(s):
        s = re.split("<(br|BR)[ ]*/*>", s)
        s = [i for i in s if i and i not in ["br", "BR"]]
        return s

    @staticmethod
    def get_big_brackets(s, tirgger=""):
        a = re.findall("\{\{.*?" + tirgger + ".*?\}\}", s)
        if a != []: return a

    @staticmethod
    def get_square_brackets(s):
        a = re.findall("\[\[.*?\]\]", s)
        if a != []:
            a = [i[2:-2] for i in a]
            return a

    @staticmethod
    def get_square_brackets_only(s):
        """返回有标记的人物"""
        # 将注释标签去除
        brackets=re.findall("(\(.*?\)|（.*?）)",s)
        for bracket in brackets:
            if "[[" in bracket:
                s.replace(bracket,"")

        s=re.findall("\[\[.*?\]\]",s)

        s=[i[2:-2].split("|")[0] for i in s]

        return s

    @staticmethod
    def del_ref(s):
        # 去掉ref标签
        s = re.sub("\<ref.*?\>.*?\<[ ]*/[ ]*ref[ ]*\>", "", s)
        s = re.sub("\<[ ]*ref.*?\>", "", s)
        return s

    def value_split(self,s):
        # 删除ref标签，否则会抽取错误信息

        # 添加一些其他信息，比如逗号分隔

        # 标签是有优先级大小的，最小的是[[]]，其次是{{}}，其中{{}}可能包含[[]]
        # {{}}标签也可能包含{{}}本身的标签
        # 优先级
        #

        # 对没有意义的标签进行替换
        wiki_labels = self.WikiLabels()
        s = re.sub("\{\{.*?\}\}", wiki_labels.match_process, s)  # 对有意义的标签进行替换

        s = self.del_ref(s)
        # 对br标签，大括号标签，中括号标签进行分割
        s=re.split("(<br[ ]*/*>|\[\[.*?\]\]|\{\{.*?\}\})",s,flags=re.I)
        # 去掉空项，去掉br标签
        s = [i for i in s if i and i[0] != "<"]
        s = [i.strip() for i in s]

        # 去掉每一项的标签标志，变成纯文本，将其标志存到另一个列表里
        s = [i for i in s if i not in ",，、 "]

        label = [0] * len(s)
        for i in range(len(s)):
            if len(s[i]) > 1:
                if s[i][:2] == "{{":
                    s[i] = s[i][2:-2]
                    label[i] = 2
                elif s[i][:2] == "[[":
                    label[i] = 1
                    s[i] = s[i][2:-2]

        # 继续分割
        # for i in range(len(s)):
        #     if "、" in s[i]:
        #         s[i] = s[i].split("、")
        #         s[i] = [j for j in s[i] if j]

        return s, label

    def remove_brackets(self,s):
        remove_str="[]{}"
        for i in remove_str:
            s=s.replace(i,"")
        return s

    def call(self,fun_name, value):
        if fun_name=="common":
            return self.value_split(value)[0]

        else:
            s='self.{}("{}")'.format(fun_name,value)
            return eval(s)

    # 以下为各种属性的抽取方案

    def name(self,s):
        """用br分割一下"""
        s=re.split("<br[ ]*>",s,flags=re.I)
        if len(s)==1:s=s[0]
        return s


    def date(self,s):
        s = self.del_ref(s)
        chinese_and_number = GetPartialOnly.Chinese_and_numbers(s)
        chinese = GetPartialOnly.Chinese(s)
        s_split, label = self.value_split(s)
        for i in range(len(s_split)):
            if label[i] == 2:
                patterns = [
                    "year=[0-9]{1,4}\|month=[0-9]{1,2}\|day=[0-9]{1,2}",
                    "[0-9]{1,4}\|[0-9]{1,2}\|[0-9]{1,2}"
                ]
                pattern = get_first_pattern(patterns, s_split[i])
                if pattern and pattern is not None:
                    pattern = pattern.split("|")
                    if chinese: pattern = [chinese] + pattern
                    return pattern
                else:
                    return chinese_and_number
        return chinese_and_number

    def place(self,s):
        s=del_chars(s)
        s_split,label=self.value_split(s)
        new_s_split=[]
        for i in range(len(label)):
            if label[i]==2:
                if "flag" in s_split[i] or "Flag" in s_split[i]:
                    s_split[i] = s_split[i].split("|")[1]
                else:
                    s_split[i] = s_split[i].split("|")[0]
                new_s_split.append(s_split[i])
            elif label[i]==1:
                new_s_split.append(s_split[i])
        s_split=new_s_split
        s_split = [i for i in s_split if "px" not in i and "file" not in i and "File" not in i]
        s_split=[i.split("|")[0] for i in s_split]

        return s_split

    def nationality(self,s):
        s=re.sub("（.*?）","",s)
        s,label=self.value_split(s)
        new_s=[]
        for i in range(len(label)):
            if label[i]!=0:
                new_s.append(s[i])
        for i in range(len(new_s)):
            if "flag" in new_s[i] or "Flag" in new_s[i]:
                new_s[i]=new_s[i].split("|")[1]
            else:
                new_s[i] = new_s[i].split("|")[0]
        new_s=[i for i in new_s if "px" not in i and "file" not in i and "File" not in i]
        return new_s

    def person(self,s):
        """返回有标记的人物"""

        return self.get_square_brackets_only(s)

    def spouse(self,s):
        res = []
        s = self.del_ref(s)
        # 识别marriage模块
        m = self.get_big_brackets(s, "marriage")
        if m:
            for item in m:
                item = item[2:-2]
                p = re.search("\{\{.*\}\}", item)
                if p:
                    person = p.group()
                    item = re.sub("\{\{.*\}\}", "person", item)
                    item = item.split("|")
                else:
                    item = item.split("|")
                    person = item[1]
                if len(s) > 4:
                    # 以离异
                    res.append([person, "ex"])
                else:
                    res.append([person, "now"])

        else:
            s = self.br_split(s)
            for item in s:
                res.append(item)
        return res

    def children(self,s):
        ss = self.get_square_brackets(s)
        if ss:
            return ss
        else:
            return s

    def position(self,s):
        return self.remove_brackets(s)

    def height(self,s):
        """
        没有返回null

        :param s:
        :return:
        """
        patterns=[
            "[012]\.[0-9]*",    #米
            "[12][0-9][0-9]",   #厘米
            "(ft|feet)=[0-9]*\|(in|inch)=[0-9]*",   #英尺
            "[0-9]*英尺[0-9]*英寸",
            "[0-9]*\|(ft|feet)\|[0-9]*\|(in)"
        ]

        s=get_first_pattern(patterns,s)

        return s

    def education(self,s):
        """
        学历没有单独的框，需要同学校一起抽取
        :param s:
        :return:
        """

        def degree(s):
            patterns = [
                "(博士|本科|大专|硕士研究生|中专|学士|博士后|专科|EMBA|高中|初中|大本|中学|小学)",
                "(大学|硕士|研究生|MBA)",
                "(案首|监生|生员|禀生|贡生|举人|解元|进士|探花|榜眼|状元)",  # 古代学历
                "(工学|理学)"
            ]
            res=get_first_pattern(s)
            return res

        def single_school_filter(s):
            # 有先后识别顺序
            """
            学校可能有多个
            无法识别的情况
            1.学校简称：麻省理工 上海复旦 哈佛 南京中医药 县立北高 长影 上海二医 江南水师 长安县立第五高小
            2.似学校非学校：嵩山少林寺 南宁市体工队 中国人民银行研究生部 北京电影制片厂 中国美术家协会培训中心
            3.非学校：苏黎世综合技术联盟 天主教
            :param s:
            :return:
            """
            patterns = [
                ".+(分校|学院|研究所)",  # 防止二级院校名丢失
                ".+(学校|学院|学堂|学园|大学|院校|研究所|实验室)",
                ".+(女中|初中|高中|附中|[0-9一二三四五六七八九十]+中|[0-9一二三四五六七八九十]+小)",
                ".+(院|校)",  # 小学|中学|
                ".+(大|专|师范|医科|班|堂|团|医药)"  # 研究院|书院|剧院|中科院|美术院|
                # 卫校|分校|军校|艺校|党校
                # 初中|高中|附中
                # 医科大 北大
            ]
            ret = None
            for pattern in patterns:
                ret = re.search(pattern, s)
                if ret:
                    s = ret.group()
                    if s[:3] == "毕业于": s = s[3:]
                    if s[:2] == "毕业": s = s[2:]
                    return s
            if not ret: return None

        def school(s):
            s=self.person(s)
            s=[single_school_filter(i) for i in s]
            s=[i for i in s if i is not None]
            return s

        s=s.replace("學","学")

        return school(s)

    def awards(self,s):
        """只取中文"""
        return self.get_square_brackets_only(s)

    def religion(self,s):

        return self.get_square_brackets_only(s)

    def event(self,s):
        return self.remove_brackets(s)

    def weight(self,s):

        patterns=[
            "kg=[0-9\.]+",
            "lb=[0-9\.]+",
            "[0-9\.]+\|kg",
            "[0-9\.]+\|lb",
            "[0-9\.]+[ ]*(磅|公斤|斤|kg)"
        ]

        return get_first_pattern(patterns,s)

    def sex(self,s):
        """有男有女的就不识别"""
        if "男" in s:
            if "女" not in s:return "男"
        elif "女" in s:
            return "女"

    def genre(self,s):
        return self.remove_brackets(s)

    def succession(self,s):
        return self.get_square_brackets_only(s)


def find_attribute_in_db(attribute):
    """获取属性名称的属性值，并保存"""
    a=AttributeFilter()
    db = Neo4jDB(url='http://localhost:7474', username="neo4j", password="zyliu")
    if db:print("连接成功！")
    res=db.search_attribute(attribute,limit=200)
    res=[attribute_value_process(i) for i in res]
    save_json(res, filename="temp_data/{}.json".format(attribute), list_in_line=True)
    res=[a.call("place",i) for i in res]
    save_json(res,filename="temp_data/{}_split.json".format(attribute),list_in_line=False)

def get_person_statistics(filename,save_dir):
    """
    统计数据(包含infobox)

    包括：
        属性的数量分布
        关系的数量分布
        实体的数量分布
    :param filename:
    :return:
    """

    data=load_json(filename)

    # 属性类型出现计数
    attribute_name_count=DictCount()
    # 人物关系类型出现次数
    person_relation_type_count=DictCount()
    # 非人物关系出现次数
    non_person_relation_type_count=DictCount()
    # 非人物实体出现次数 非人物类型：非人物实体：实体数量
    non_person_entity_count=dict()
    # 非人物实体类型出现次数
    non_person_entity_type_count=DictCount()
    # 人物出现次数
    person_count=DictCount()

    # 该类型实体的数量（不是出现次数）

    for item in tqdm(data):
        for attribute in item["infobox"].keys():
            attribute_name_count.add(attribute)
        for relation in item["relations"]:
            relation_type=relation[0]
            entity_type=relation[1]
            entity=relation[2]
            if entity_type=="person":
                person_relation_type_count.add(relation_type)
                person_count.add(entity)
                person_count.add(item["name"])
            else:
                if entity_type not in non_person_entity_count:
                    non_person_entity_count[entity_type]=DictCount()
                non_person_entity_count[entity_type].add(entity)
                non_person_entity_type_count.add(entity_type)
                non_person_relation_type_count.add(relation_type)


    attribute_name_count=attribute_name_count.get()
    person_relation_type_count=person_relation_type_count.get()
    non_person_relation_type_count=non_person_relation_type_count.get()
    non_person_entity_type_count=non_person_entity_type_count.get()
    person_count = person_count.get()
    non_person_entity_count = {key: value.get() for key, value in non_person_entity_count.items()}
    # 每个非人物类型实体的数量
    non_person_entity_type_num=sort_dict({key:len(value.keys()) for key,value in non_person_entity_count.items()})

    # 所有有关系的人物数量
    all_person_num=len(person_count.keys())
    print(all_person_num)
    # 所有关系的出现次数
    relation_type_count=dict(**non_person_relation_type_count, **person_relation_type_count)
    # 所有非人物实体的类型数量


    draw=Draw(is_show=False)
    draw.configure(save_dir=save_dir+"relation_type_count.png")
    draw.histogram(relation_type_count,is_vertical=False)
    draw.configure(save_dir=save_dir+"non_person_entity_type_count.png")
    draw.histogram(non_person_entity_type_count,is_vertical=False)
    draw.configure(save_dir=save_dir+"non_person_entity_type_num.png")
    draw.histogram(non_person_entity_type_num, is_vertical=False)











if __name__=="__main__":
    # find_attribute_in_db("weight")

    # modify_infobox("data/hand_made_data/Schema.xlsx","data/temp_data/person_infobox.json","data/kg_data/person_page.json")

    get_person_statistics("data/kg_data/person_page.json",save_dir="data/statistics_data/")
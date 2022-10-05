# coding:utf-8
from .CommonTools.TextTool import *
import re
from tools import *
from .CommonTools.JsonTool import *




class AttributeInterface():
    """
    属性工具的接口，包含所有特定属性用到的功能
    """

    def __init__(self):
        self.statistics = {
            "识别出该属性数量": 0,
            "无效属性值数量": 0,
            "属性值在summary数量": 0,
            "属性值在para数量": 0,
            "多属性值数量": 0,
            "文中直接抽出属性值数量": 0
        }

    # 必需重写的方法
    def get_name(self):
        """返回属性的标准名称"""
        pass

    # 默认方法，若采用默认抽取，则将他们补全
    def get_extract_patterns(self) -> list:
        """
        返回属性特征模式的正则表达式列表
        若不用extract默认函数功能可不重写
        """
        return None

    def get_filter_patterns(self) -> list:
        """
        返回属性过滤模式的正则表达式列表
        若不用filter默认函数功能可不重写
        :return:
        """
        return None

    def get_name_patterns(self) -> list:
        """
        返回识别属性名称的正则表达式列表
        正则表达式列表具有先后顺序
        """
        return None

    # 自定义方法
    def get_name_in_infobox(self, attributes):
        """
        寻找infobox属性名称列表中是否有该属性，是则返回该属性，不是返回None
        限定每个属性值对应infobox中的一个
        可自定义，默认为该方法
        """
        patterns = self.get_name_patterns()
        if patterns is None:
            for attribute in attributes:
                if self.get_name() in attribute: return attribute
        else:
            for pattern in patterns:
                for attribute in attributes:
                    if re.search(pattern, attribute): return attribute

    def filter(self, s):
        """
        依照模式对属性值过滤
        :param s: 属性值字符串
        :return: 若识别出多个属性值，则返回列表，若只有一个属性值，则返回字符串，没有则返回None
        例：
            身高为167cm。 ——> 167cm
        """

        if s:
            if self.get_filter_patterns():
                return get_first_pattern(self.get_filter_patterns(), s)
            else:
                return s

    def extract(self, s):
        """
        从一句话中抽出符合该属性特征的属性值，用于增加infobox
        先抽出模式，在进行过滤
        不考虑多个属性值，只抽一个属性值
        :param s: 句子
        :return: 属性值 或 None
        例：身高
            东京都出身，身长149cm，体重39kg，血型AB型 ——>身长149cm ——> 149cm

        在识别之前要全角转半角以防出现模式下识别错误
        """
        if not s: return None
        if self.get_extract_patterns():
            for pattern in self.get_extract_patterns():
                ret = re.search(pattern, s)
                if ret:
                    ret = self.filter(ret.group())
                    if ret: return ret

    def normalize(self, value_list):
        """对属性值列表做归一化，默认返回出现次数最多的"""
        return max(value_list, key=value_list.count)

    def equal(self, value1, value2):
        """判断两个属性值是否相等"""
        #  return value1==value2
        if value1 in value2: return True
        if value2 in value1: return True
        return False

    def print_statistics(self):
        """
        打印统计数据
        """
        print("属性：", self.get_name())
        print("统计结果：")
        print(self.statistics)


    # 要考虑每一个属性的衔接
    def get_attribute_value_pair(self,item):
        if "infobox" in item:
            infobox=item["infobox"]
            attribute_name=self.get_name_in_infobox(infobox.keys())
            if attribute_name is not None:
                value=self.filter(infobox[attribute_name])
                print("name:",item["name"],"\t\tattribute:",attribute_name,"\t\tvalue:",value)

    def remote_supervision(self, item):
        """
        远程监督，详细介绍如下
        :param item:人物网页抽出来的4项
        :return:
            (属性值,属性值所在句子)，若句子为简介，则标识句子为"summary"，若没有，则返回None
            若属性值有多个，则返回元组列表
        """

        def search_value(self, value, item):
            """
            对属性值value进行搜索，范围为所有有效信息
            :param value: 属性值
            :param item: 4项
            :return: (属性值,属性值所在句子)，若句子为简介，则标识句子为"summary"，若没有，则返回None
            """
            if item["summary"] and value in item["summary"]:
                self.statistics["属性值在summary数量"] += 1
                return (value, "summary")
            else:
                if "para" in item.keys():
                    for i in item["para"]:
                        if value == i or len(i) < 3: continue
                        if value in i:
                            if self.get_name() + "：" != i[:len(self.get_name() + "：")]:
                                self.statistics["属性值在para数量"] += 1
                                return (value, i)

        attribute_name = self.get_name_in_infobox(item["infobox"].keys())
        if attribute_name:
            self.statistics["识别出该属性数量"] += 1
            value = item["infobox"][attribute_name]
            value = self.filter(value)
            if value is None or value == "":
                self.statistics["无效属性值数量"] += 1
            elif isinstance(value, list):
                self.statistics["多属性值数量"] += 1
                result = []
                for i in value:
                    search_pair = search_value(self, i, item)
                    if search_pair: result.append(search_pair)
                if result: return result
            else:
                res = search_value(self, value, item)
                if res: return res

        # 添加extract
        # if "summary" in item.keys():
        #     res=self.extract(item["summary"])
        #     if res:
        #         self.statistics["文中直接抽出属性值数量"]+=1
        #         self.statistics["属性值在summary数量"] += 1
        #         return (res, "summary")
        # if "para" in item.keys():
        #     for i in item["para"]:
        #         res = self.extract(i)
        #         if res and self.get_name()+"："!=i[:len(self.get_name()+"：")]:
        #             self.statistics["文中直接抽出属性值数量"] += 1
        #             self.statistics["属性值在para数量"] += 1
        #             return (res, i)


class spouse:
    pass

class name(AttributeInterface):

    def get_name(self):
        return "姓名"

    def get_name_patterns(self):
        pattern=["姓名", "名称","name"]

    def filter(self,s):


        return s


class BirthDate(AttributeInterface):
    def get_name(self):
        return "出生日期"

    def get_name_patterns(self):
        pattern = ["出生", "出生日期", "birth_date"]
        return pattern

    def filter(self,s):
        s=del_ref(s)
        chinese_and_number= GetPartialOnly.Chinese_and_numbers(s)
        chinese=GetPartialOnly.Chinese(s)
        s_split,label=value_split(s)
        for i in range(len(s_split)):
            if label[i]==2:
                patterns=[
                    "year=[0-9]{1,4}\|month=[0-9]{1,2}\|day=[0-9]{1,2}",
                    "[0-9]{1,4}\|[0-9]{1,2}\|[0-9]{1,2}"
                ]
                pattern=get_first_pattern(patterns,s_split[i])
                if pattern and pattern is not None:
                    pattern = pattern.split("|")
                    if chinese:pattern=[chinese]+pattern
                    return pattern
                else:
                    return chinese_and_number
        return chinese_and_number

class BirthPlace(AttributeInterface):

    def get_name(self):
        return "出生地"

    def get_name_patterns(self) -> list:
        return ["birth_place","出生地"]

    def filter(self, s):
        s=del_chars(s)
        s_split,label=value_split(s)
        return s_split


class Occupation(AttributeInterface):
    
    def get_name(self):return "职业"

    def get_name_patterns(self) -> list:
        return ["职业","occupation"]

    def filter(self, s):
        s= value_split(s)
        return s

class Nationality(AttributeInterface):
    def get_name(self):return "国籍"
    def get_name_patterns(self) -> list:
        return [
            "国籍","nationality","國籍"
        ]
    def filter(self, s):
        return value_split(s)



def test_infobox(filename,attribute_object):
    # 对每一个属性进行测试
    data=load_json(filename)
    for item in data:
        attribute_object.get_attribute_value_pair(item)





if __name__=="__main__":
    attribute=Nationality()
    test_infobox("data/person_infobox.json",attribute)

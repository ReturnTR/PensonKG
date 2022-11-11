人物知识图谱构建
=========
本文档描述人物知识图谱构建的详细流程，目前以Wiki作为数据集

目录
=======

<!-- TOC -->

- [人物知识图谱构建](#%E4%BA%BA%E7%89%A9%E7%9F%A5%E8%AF%86%E5%9B%BE%E8%B0%B1%E6%9E%84%E5%BB%BA)
- [目录](#%E7%9B%AE%E5%BD%95)
- [Wiki原始语料获取](#wiki%E5%8E%9F%E5%A7%8B%E8%AF%AD%E6%96%99%E8%8E%B7%E5%8F%96)
- [数据分析与处理](#%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E5%A4%84%E7%90%86)
    - [1. Wikidumpxml数据格式分析](#1-wikidumpxml%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E5%88%86%E6%9E%90)
    - [2. 网页内容（<text>标签内容）格式分析](#2-%E7%BD%91%E9%A1%B5%E5%86%85%E5%AE%B9text%E6%A0%87%E7%AD%BE%E5%86%85%E5%AE%B9%E6%A0%BC%E5%BC%8F%E5%88%86%E6%9E%90)
    - [3. 页面初步格式化抽取出上面提到的的4项](#3-%E9%A1%B5%E9%9D%A2%E5%88%9D%E6%AD%A5%E6%A0%BC%E5%BC%8F%E5%8C%96%E6%8A%BD%E5%8F%96%E5%87%BA%E4%B8%8A%E9%9D%A2%E6%8F%90%E5%88%B0%E7%9A%84%E7%9A%844%E9%A1%B9)
    - [4. 选取人物页面](#4-%E9%80%89%E5%8F%96%E4%BA%BA%E7%89%A9%E9%A1%B5%E9%9D%A2)
    - [5. 对人物页面的Infobox进行格式化](#5-%E5%AF%B9%E4%BA%BA%E7%89%A9%E9%A1%B5%E9%9D%A2%E7%9A%84infobox%E8%BF%9B%E8%A1%8C%E6%A0%BC%E5%BC%8F%E5%8C%96)
- [针对人物Infobox的规则抽取](#%E9%92%88%E5%AF%B9%E4%BA%BA%E7%89%A9infobox%E7%9A%84%E8%A7%84%E5%88%99%E6%8A%BD%E5%8F%96)
    - [1. 获取人物的全部属性名称](#1-%E8%8E%B7%E5%8F%96%E4%BA%BA%E7%89%A9%E7%9A%84%E5%85%A8%E9%83%A8%E5%B1%9E%E6%80%A7%E5%90%8D%E7%A7%B0)
    - [2. 属性与关系的定义（Schema构建）](#2-%E5%B1%9E%E6%80%A7%E4%B8%8E%E5%85%B3%E7%B3%BB%E7%9A%84%E5%AE%9A%E4%B9%89schema%E6%9E%84%E5%BB%BA)
    - [3. 编写抽取规则](#3-%E7%BC%96%E5%86%99%E6%8A%BD%E5%8F%96%E8%A7%84%E5%88%99)
- [构建图谱](#%E6%9E%84%E5%BB%BA%E5%9B%BE%E8%B0%B1)
    - [1. 初步构建](#1-%E5%88%9D%E6%AD%A5%E6%9E%84%E5%BB%BA)
    - [2. 构建重名实体信息](#2-%E6%9E%84%E5%BB%BA%E9%87%8D%E5%90%8D%E5%AE%9E%E4%BD%93%E4%BF%A1%E6%81%AF)
    - [3. 根据wiki的重定向信息扩充人物关系](#3-%E6%A0%B9%E6%8D%AEwiki%E7%9A%84%E9%87%8D%E5%AE%9A%E5%90%91%E4%BF%A1%E6%81%AF%E6%89%A9%E5%85%85%E4%BA%BA%E7%89%A9%E5%85%B3%E7%B3%BB)

<!-- /TOC -->


# Wiki原始语料获取

wiki数据源自wikidump

[Wikidump下载链接](https://dumps.wikimedia.org/zhwiki/latest/)

进入网页后选取`zhwiki-20220801-pages-articles-multistream.xml.bz2`

# 数据分析与处理

## Wikidump`xml`数据格式分析
原始文件XML数据格式如下
```xml
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="zh">
    <!--一个page表示一个网页，数据由1294978个page组成-->
    <page>
        <title><!--网页标题，可用作实体名称--></title>
        <id><!--网页唯一ID，用数字表示--></id>
        <parentid>57201542</parentid>
        <timestamp>2020-01-24T01:31:16Z</timestamp>
        <model>wikitext</model>
        <contributor>
        <username>InternetArchiveBot</username>
        <comment><!--网页曾经新的修改信息--></comment>
        <format>text/x-wiki</format>
        <id>2383178</id>
      	</contributor>
        <text bytes="网页大小" xml:space="preserve">
            <!--网页内容-->
        </text>
    </page>
</mediawiki>
```
可以发现该文件有多个`<page>`（页面）标签组成

原始数据大小2.7个G，解压后有11个G，共有1294948个page

## 网页内容（`<text>`标签内容）格式分析

经过分析，每个page可分为5个部分

| 网页部分 |             描述             |                   识别标志                   |
| :------: | :--------------------------: | :------------------------------------------: |
| Infobox  | 网页实体的属性表，贴在网页的 |    以`{{}}`为标志，在网页的开头，可能没有    |
| summary  |        网页实体的简介       |     在infobox和para之间，的一个简短文本      |
|   para   |    实体各个方面的详细介绍    | 以`==xx==`为标志，遇到的第一个就是para的开始 |
| category |      实体属于的类别链接      |  以`[[Category:xx]]`为标志，在网页的末尾  |
| redirect |      链接重定向页面         |  以`[[Category:xx]]`为标志，在网页的末尾  |

以一个网页为例子

```XML
{{Automatic taxobox
| taxon = Pseudomugilidae
| image = 
| image_caption = 
| authority = 
| subdivision_ranks = [[屬]]
| subdivision =
見內文
}}

'''似鯔銀漢魚科'''為[[輻鰭魚綱]][[銀漢魚目]]的其中一[[科]]。

==分布==
本鱼广泛澳洲东部之溪流域，最南可达到雪梨。

==特征==
本鱼体适度延长，侧扁；嘴小，略垂直；前主上腭之后部齿较长，于口闭合时会外露；第一背鳍起点在胸鳍末端以前，具3至6棘；第二背鳍具1棘棘6至10枚软条；臀鳍之起点在第一背鳍末端之下方，具1棘及9至12枚软条；胸鳍尖形，尾鳍开叉；无侧线，一纵列鳞具25至31枚。雌雄异形，雄鱼背鳍、臀鳍及腹鳍之前方各鳍条成丝状延长；在春夏之繁殖季节，体色会变成鲜艳之黄色。雄鱼体长可达7公分。

[[Category:鯔銀漢魚科|*]]
[[Category:银汉鱼目|Z]]
```

![image](https://github.com/ReturnTR/PensonKG/blob/main/images/wiki_数据实例.png)

## 页面初步格式化(抽取出上面提到的的4项)

根据前面分析的四项，通过特定的规则将他们抽取出来，同时尽量保留原有信息

- 简介和正文繁体转简体
- 在正文和简介中，除了[[]]标签和[]标签，去掉所有的其他标签，只保留文字与标点符号
- 保留infobox与category的全部内容

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/WikiProcess.py)

## 选取人物页面

目标是人物图谱，所以需要将人物页面截取过来，本方案通过infobox里面的标识识别出部分的人物

该方案不能将没有infobox的人物识别出来

方法：
- 找到全部的infobox人物模板标识，Wiki提供了人物infobox的标识，见[人物信息框模板](https://zh.wikipedia.org/wiki/Category:人物信息框模板)（在wiki中infobox被称为信息框）
- 在页面中匹配人物标识



例如

```xml
{{Infobox NBA Player
| name = 姚明<br/>Yao Ming
| image = YaoMingonoffense2.jpg
| height_ft   = 7
| height_in   = 5
| weight_lb   = 310
| nationality = {{PRC}}
| birth_date = {{Birth date and age|1980|9|12}}
| birth_place = {{CHN}}[[上海市]][[徐匯區]]
...
}}
```

其中`Infobox NBA Player`为infobox的开头，表示页面的类型，而该类型出来在上述的人物信息框模板中，因此该页面被认为是人物的页面

为此，我们需要将该网页下所有的模板记录在列表中，然后对每一个页面的infobox开头进行匹配，匹配成功则将其归类到人物页面中

[抽取代码和模板列表](https://github.com/ReturnTR/PensonKG/blob/main/GetPersonViaInfobox.py)

共抽取出88404个人物页面，相关数据如下：

|全部数量 | 有infobox的数量 | 有infobox的人物数量|
| :------: | :---: | :---:|
|1294948 | 466181 | 88404 |

## 对人物页面的Infobox进行格式化
由于人物页面的Infobox是字符串信息，并不是`{属性:属性值}`这样的格式化标识，因此需要对其转换，以上面提到的模板为例，我们需要：
- 确定{属性:属性值}的标志
- 删除多余的信息，例如`<ref>`标签

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/InfoboxProcess.py)


# 针对人物Infobox的规则抽取
即抽取Infobox的信息来构建图谱，分为属性抽取与关系抽取，为此，我们需要知道人物都有哪些属性和关系

## 获取人物的全部属性名称
这里的属性也包括关系

获取方法有两种，包括：

1. 人物信息框模板
人物信息框模板的网页中的部分任务定义了该类人物可能有的属性值，并进行了一定程度上的解释，例如属性的中文名和属性的含义
我们把所有相关的模板截取下来，放到[人物信息框模板](https://github.com/ReturnTR/PensonKG/blob/main/InfoboxProcess.py)文件中

2. 格式化的Infobox页面

在上一步我们已经得到了格式化后的Infobox页面，直接对里面是属性统计即可
需要说明的是，Infobox中的属性名称并不是统一的，它非常繁杂，有英文有中文，有的属性只有在通过查看部分属性值的情况下才能确定属性名称的含义，例如`rank`属性在Infobox里面的含义是军衔，与想象的不太一样
我们抽取了所有的属性，并依照出现次数进行排序，以便后续的过滤操作

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/InfoboxStatistics.py)

[抽取结果](https://github.com/ReturnTR/PensonKG/blob/main/data/statistics_data/person_key_count.json)


## 属性与关系的定义（Schema构建）

我们需要将前面总结所有的属性整合起来，形成一个大的，整体的抽取模板

总结的工作包括：
1. 属性名称标准化，对于每一个属性，我们要确定属性的标准名称，以方便图谱的查找
2. 对属性名称进行归一化，例如`gender`与`性别` 视为一个属性
3. 有的模板书会添加对属性的解释，我们需要将解释记录下来方便下一步的工作
4. 对所有模板那中出现属性的次数进行计数，用来排序
5. 标记该属性是否为人物关系
6. 由于人物与其他实体之间的关系会增加图谱的关联性，我们有必要将其它类型的属性表记为实体，例如`出生地`,`毕业院校`等
7. 该属性/关系的抽取方法

该工作需要大量的人工操作，包括查看大量属性值，属性名称，将信息手动添加进模板

最终构建出[Schema](https://github.com/ReturnTR/PensonKG/blob/main/data/statistics_data/Schema.xlsx)文件，文件格式如下（上列表示属性的栏目，下列为解释）：
名称	别名	实体名称	是否为人物关系	抽取方法	数量占比	中文名

|名称 | 别名 | 实体名称| 是否为人物关系 | 抽取方法 | 数量占比 | 中文名 |
| :------: | :---: | :---:| :---:| :---:| :---:| :---:| 
|属性的标准化名称 | 属性在Infobox的其他名称，用逗号分隔，用于归一化 | 如果是实体，则写实体名称，如不是则空着 | 是就填是，不是可以空着| 抽取方法的名称，在程序中进行调用 | 该属性在出现全部人物页面中的次数 | 如果该项不为空，则该项视为属性标准名称，并将第一栏加入到别名栏中 |


## 编写抽取规则

以Schema文件和人物的Infobox作为输入，直接抽取出人物的属性和关系


抽取分类：

- 通用抽取（抽取方法为common）

- 特殊抽取（抽取方法为空）

- 不抽取（抽取方法为其他字符）


[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/AttributeFilter.py)

统计信息

![image](https://github.com/ReturnTR/PensonKG/blob/main/data/statistics_data/non_person_entity_type_count.png)
![image](https://github.com/ReturnTR/PensonKG/blob/main/data/statistics_data/non_person_entity_type_num.png)
![image](https://github.com/ReturnTR/PensonKG/blob/main/data/statistics_data/relation_type_count.png)



# 构建图谱

采用Neo4j构建


## 初步构建

流程：
1. 导入Wiki中所有的128万个节点，属性值包括 name，infobox，summary，para，category，redirect（有的话）这些属性值不能被改变，尤其是name，不能被属性值里面的name替换
    包括：
    - 建立索引unknown和person
    - 将节点导入，类型设置为unknown

2. 直接导入配置好的人物文件进行人物图谱的构建
    包括：
    - 添加属性值
    - 建立人物关系（先查找图谱中有无该实体，若有的话首先为该实体添加实体类型标签，然后在建立关系）

整理过的属性加符号进行区分

[构建代码](https://github.com/ReturnTR/PensonKG/blob/main/KG.py)




## 构建重名实体信息

从wiki页面中找出所有可能重名的标识页面，并把名称用字典的形式表示出来

Wiki页面中大都使用"()"来表示该人物的额外信息，用此可以添加人物的重名信息

例：

```json
"王凤朝": ["王凤朝 (1965年)","王凤朝 (京剧鼓师)","王凤朝","王凤朝 (1954年)"]
```

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/DuplicateNameExtraction.py)

[抽取结果](https://github.com/ReturnTR/PensonKG/blob/main/data/temp_data/wiki_page_duplicated.json)

## 根据wiki的重定向信息扩充人物关系

由于以下原因导致有些关系里没有建立，以国家为例：

   -  姚明实体的`国籍`属性是`PRC`但是`PRC`没有出现在wiki页面中`name`属性中，这导致该关系无法建立

但我们在wiki中输出`PRC`是直接可以进入name属性为`中华人民共和国`的页面中，这是因为wiki页面中有重定向信息，中华人名共和国的重定向信息中含有`PRC`

因此我们需要将重定向信息与页面连接起来

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/DuplicateNameExtraction.py)
[重定向信息](https://github.com/ReturnTR/PensonKG/blob/main/data/temp_data/wiki_page_redirect.json)


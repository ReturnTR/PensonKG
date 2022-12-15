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
- [模型扩充图谱](#%E6%A8%A1%E5%9E%8B%E6%89%A9%E5%85%85%E5%9B%BE%E8%B0%B1)
    - [1. 扩充人物实体](#1-%E6%89%A9%E5%85%85%E4%BA%BA%E7%89%A9%E5%AE%9E%E4%BD%93)
    - [2. 属性抽取与关系抽取](#2-%E5%B1%9E%E6%80%A7%E6%8A%BD%E5%8F%96%E4%B8%8E%E5%85%B3%E7%B3%BB%E6%8A%BD%E5%8F%96)
        - [2.1. 属性抽取：](#21-%E5%B1%9E%E6%80%A7%E6%8A%BD%E5%8F%96)
        - [2.2. 关系抽取](#22-%E5%85%B3%E7%B3%BB%E6%8A%BD%E5%8F%96)
            - [2.2.1. 训练语料构造](#221-%E8%AE%AD%E7%BB%83%E8%AF%AD%E6%96%99%E6%9E%84%E9%80%A0)
    - [3. 通过百度百科增加数据量](#3-%E9%80%9A%E8%BF%87%E7%99%BE%E5%BA%A6%E7%99%BE%E7%A7%91%E5%A2%9E%E5%8A%A0%E6%95%B0%E6%8D%AE%E9%87%8F)
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

继续补全图谱，即补全Schema
扩充人物关系
添加实体连接数据
尽可能利用其他信息，例如infobox，category，summary

infobox的信息进行调整

category的有用信息：
    后面的字符
infobox有用的信息：
    属性名称，不是属性值
    找出人物独有的属性，或者接近人的属性
summary有用的信息：
    越在前面的越有用


排序要比设置阈值好多了

# 模型扩充图谱

## 扩充人物实体
前面的工作是根据infobox来判断是否为人物实体，这样会漏掉很多人物，即没有infobox但是是人物的实体

任务模型：分类模型

给定一个半结构化数据，来判断该数据所属的类型
如何利用所有的信息来推理出它的类型
信息熵要尽可能地大，差异化明显

需要的文件：
    非人物的:（有infobox但不是人物）
        category
        summary
        infobox
    人物的：
        category
        summary
        infobox
        para
    统计信息：
        非人物infobox属性值占比


通过bert分类器对summary进行分类，结果如下：
 'p': 0.9896, 'r': 0.9520, 'f': 0.9705

将该模型对未标注的所有没有infobox的页面进行识别，结果见no_infobox_summary_dev


对该数据的前200例进行检查，
人物基本上都被识别（300例里面都为人物），
识别所有含有infobox的，有人物的占0.9928633695589004
但是有是别错的，占的比例很大

发现出如下类型的识别错误的例子：
```json
[
    ["男高音","女高音女低音男高音男低音在音乐，男高音（tenor）是一名音域占c－c2共15度的歌唱家。他们按音质、音色、音区等不同特点分为：抒情花腔男高音（lirico-Leggero tenor）、抒情男高音（lyric tenor）、英雄男高音（heldentenor）和戏剧男高音（dramatic tenor）。柴可夫斯基的歌剧《黑桃皇后》中的男主人公格尔曼，就是典型的戏剧男高音。"],
    ["男低音","女高音女低音男高音男低音在音乐，男低音（bass）是一名唱音域E2－E4共16度的歌唱家，音色低沉、浑厚、老成、持重。柴可夫斯基的歌剧《叶甫根尼·奥涅金》中的格列敏咏叹调“爱情能征服所有的人们”就是一首男低音独唱曲。"],
    ["庞德 (消歧义)","庞德可以指：* 庞德，中国东汉末年武将* 艾兹拉·庞德，20世纪美国诗人* 罗斯科·庞德，20世纪美国法学家* 詹姆斯·邦德，电影剧集007系列的男主角"],
    ["李治 (消歧义)","李治可以是下列人物：* 唐高宗，名李治，唐朝皇帝。* 李冶 (数学家)，原名李治，字仁卿，号敬斋。真定染城（今属河北）人。中国金代、元代文学家、数学家。* 李治 (少将)，江西省永新县人，中国人民解放军开国少将。"],
    ["2003年逝世人物列表","下面是2003年逝世的知名人士列表。"],
    ["心理学家列表","本条目按字母顺序列举显著的心理学家。"],
    ["1769年","."],
    ["1930年代","File:1930s decade montage.png|从左至右: 美国记者多萝西·兰格拍摄的无家可归者佛罗伦斯·欧文斯·汤普森；由于极端干旱，农场变得干燥，沙尘暴遍及美国。中国抗日战争中的广州战役 ； Amelia Earhart成为美国的飞行偶像；德国独裁者阿道夫·希特勒和纳粹党试图在欧洲建立一个绝对的纳粹德国霸权新秩序，德国1939年入侵波兰，导致第二次世界大战爆发..."],
    ["舒曼","舒曼可以指：* 罗伯特·舒曼，德国音乐家。* 罗贝尔·舒曼，法国政治家。* 钟舒漫，原名钟舒曼，香港女歌手。"],
    ["天皇 (消歧义)","天皇可以指："],
    ["选帝侯","卢森堡伯爵亨利为罗马人民国王的选帝侯。由左至右：科隆总教区总主教、美因茨总教区总主教、特里尔总教区总主教、莱茵-普法尔茨伯爵、萨克森-维滕贝格公爵、勃兰登堡藩侯与波希米亚国王。选帝侯（Kurfürst，复数为Kurfürsten'，\"kur\"意为“选择”，\"Fürst\"意为“诸侯”），简称选侯，意指拥有选举罗马人民的国王的权利的德意志诸侯，原本有七人，即科隆总教区总主教、美因茨总教区总主教、特里尔总教区总主教、莱茵-普法尔茨伯爵、萨克森-维滕贝格公爵、勃兰登堡藩侯与波希米亚国王。拥有选举皇帝权力的教区与国家称为选侯国。选举出的国王经教宗加冕即可称为神圣罗马帝国皇帝。神圣罗马帝国灭亡后，选帝侯封号仍为德意志帝国所使用，但已无实权。"],
    ["天皇 (消歧义)","天皇可以指："],
    ["尼克松 (消歧义)","尼克逊是美国第37任总统——理查德·尼克松，也可以是：*尼克松 (安大略州)*尼克松 (内华达州)*尼克松 (新泽西州)*尼克松 (宾夕凡尼亚州)*尼克松 (德萨斯州)*尼克松湖：在明尼苏达州。*尼克松 (电影)，1995年上映的美国电影"],
    ["女子十二乐坊","女子十二乐坊是中国一个以流行音乐形式来演奏中国民乐的乐团。由经纪人王晓京于2001年6月18日创立，为北京世纪星碟文化传播有限公司旗下艺人组合。"],
     ["H.O.T.","H.O.T.（韩语：에이치오티），韩国第一代偶像团体，韩流的开山鼻祖。有元祖偶像、韩国歌谣界的五名战士、青少年的代言人、KPOP世界的传奇、偶像们的偶像等美誉。他们成为日后许多团体的营销典范，是现今韩国偶像产业的发展起点，也是他们首先打开了国际市场。成员为队长文熙俊、张佑赫、Tony An、Kangta、李在元，1996年出道，2001年解散。曾获得韩国金唱片奖、首尔歌谣大赏、MTV音乐录影带大奖、Mnet亚洲音乐大奖等主要奖项。团名H.O.T.本身是缩写，全写是High-five Of Teenagers..."],
    ["2005年逝世人物列表","下面是2005年逝世的知名人士列表。"],
    ["音乐形式列表","本表列举音乐形式。"],
    ["1959年","请参看：* 1959年电影* 1959年文学* 1959年音乐* 1959年体育* 1959年电视"],
    ["张衡 (消歧义)","张衡可以是下列人物：* 张衡（78年—139年）：中国东汉科学家、文学家、政治家和画家。* 张衡 (道教)：五斗米道的第二代传人。* 张衡 (隋)：隋朝人，文帝时御史大夫，协助杨广登基。* 张衡 (洪武进士)：明朝洪武年间政治人物。* 张衡 (顺治进士)，清朝顺治十八年进士，政治人物。"],
    ["1962年","请参看：* 1962年电影* 1962年文学* 1962年音乐* 1962年体育* 1962年电视"],
    ["400年"," "],
    ["668年","【】"],
    ["1498年","yearTOC|1498|明弘治十一年；越南景统元年；日本明应七年"],
    ["1515年","yearTOC|1515|明正德十年；越南洪顺七年；日本永正十二年"],
    ["1548年","ĀyearTOC|1548|明嘉靖二十七年（2月10日始）；越南莫朝永定二年，景历元年，后黎朝元和十六年；日本天文十七年"],
    ["1728年","yearTOC|1728|清雍正六年；越南保泰九年；日本享保十三年"],
]

```

思路，可以在此基础上进一步的过滤，可以用规则也可以用模型，例如名字不能有数字，不能为消歧义等

需要的文件：
- 有infobox和没有infobox的wiki_page，处理后的summary为空的全部舍弃，剩下的全部保留
    - wiki_page_infobox.json
    - wiki_page_no_infobox.json

- 将其转化为训练语料库，只保留summary，后面的标签设为0
    - wiki_page_infobox_dev.json
    - wiki_page_no_infobox_dev.json

- 模型抽取后的结果
    - wiki_page_infobox_dev_label.json
    - wiki_page_no_infobox_dev_label.json

- 将抽取结果与全部数据对齐的人物文件,包含全部数据
    - wiki_page_infobox_dev_label_person.json
    - wiki_page_no_infobox_dev_label_person.json


相对的，category也一样，结果如下：
'p': 0.97826548171896, 'r': 0.9718735362997658, 'f': 0.9750590336109775


在summary抽出的数据中category模型的效果不太好。P值接近1，R值只有0.51%，即标上的都是人物，但是有很多没标上的

用规则对简介模型进行了过滤，添加了4类规则（名字中不能包含特定字符串，不能含有数字，不能含有重定向，分类项不能为空），在该抽取结果中随机抽取了200例，有7例是不是人物，看起来效果很好

用该方法对已经是人物的进行验证，正确率99%


总结：用summary分类模型+规则过滤的方式已经可以准确识别几乎全部的实体
在没有infobox的页面中共抽出186787条人物页面，在加上之前的8万条，共有近27万条人物(279141),保存在all_person_list.json中

## 属性抽取与关系抽取

该任务对summary和para信息（有可能有category）通过模型抽取出关系和属性

### 属性抽取：
用之前抽的预料进行训练，然后对其进行标注
代码已改完，对这近20万条的数据进行抽取
抽取结果很多都对不上，不过我有属性值的过滤规则，能过滤掉大部分无意义的属性值
抽取+过滤的结果如下：
{'出生地': 84254, '国籍': 80570, '运动项目': 22049, '学历': 10570, '性别': 9280, '信仰': 9240, '作品': 8020, '民族': 7984, '毕业院校': 7383, '所属运动队': 4789, '场上位置': 4457, '逝世日期': 2619, '政治面貌': 2045, '出生日期': 1401, '外文名': 1146, '身高': 555, '体重': 275, '星座': 135}
如果这些属性都正确的话，我大概能建立20多万条三元组，用来扩充人物的infobox

由于没有标好的数据，因此只能一例一例看来看看正确率
经观察，模型对现代人物的识别率很好，对于古代人物的识别率很低，这可能是因为古代人物的训练数据很少

手标数据，结果如下
国籍 {'gold_count': 155, 'predict_count': 126, 'right_count': 65, 'exist_count': 102, 'P': '41.93%', 'R': '51.58%', 'R2': '63.72%', 'F': '46.26%', 'F2': '50.58%'}
性别 {'gold_count': 48, 'predict_count': 7, 'right_count': 7, 'exist_count': 7, 'P': '14.58%', 'R': '100.0%', 'R2': '100.0%', 'F': '25.45%', 'F2': '25.45%'}
身高 {'gold_count': 1, 'predict_count': 0, 'right_count': 0, 'exist_count': 0, 'P': -1, 'R': -1, 'F': -1}
体重 {'gold_count': 0, 'predict_count': 0, 'right_count': 0, 'exist_count': 0, 'P': -1, 'R': -1, 'F': -1}
民族 {'gold_count': 11, 'predict_count': 3, 'right_count': 2, 'exist_count': 2, 'P': '18.18%', 'R': '66.66%', 'R2': '100.0%', 'F': '28.57%', 'F2': '30.76%'}
学历 {'gold_count': 10, 'predict_count': 7, 'right_count': 5, 'exist_count': 5, 'P': '50.0%', 'R': '71.42%', 'R2': '100.0%', 'F': '58.82%', 'F2': '66.66%'}
毕业院校 {'gold_count': 49, 'predict_count': 16, 'right_count': 14, 'exist_count': 15, 'P': '28.57%', 'R': '87.5%', 'R2': '93.33%', 'F': '43.07%', 'F2': '43.74%'}
出生地 {'gold_count': 144, 'predict_count': 82, 'right_count': 50, 'exist_count': 69, 'P': '34.72%', 'R': '60.97%', 'R2': '72.46%', 'F': '44.24%', 'F2': '46.94%'}
出生日期 {'gold_count': 9, 'predict_count': 3, 'right_count': 3, 'exist_count': 3, 'P': '33.33%', 'R': '100.0%', 'R2': '100.0%', 'F': '50.0%', 'F2': '50.0%'}
逝世日期 {'gold_count': 12, 'predict_count': 4, 'right_count': 4, 'exist_count': 4, 'P': '33.33%', 'R': '100.0%', 'R2': '100.0%', 'F': '50.0%', 'F2': '50.0%'}
姓名 {'gold_count': 0, 'predict_count': 0, 'right_count': 0, 'exist_count': 0, 'P': -1, 'R': -1, 'F': -1}
外文名 {'gold_count': 0, 'predict_count': 0, 'right_count': 0, 'exist_count': 0, 'P': -1, 'R': -1, 'F': -1}
运动项目 {'gold_count': 2, 'predict_count': 2, 'right_count': 1, 'exist_count': 1, 'P': '50.0%', 'R': '50.0%', 'R2': '100.0%', 'F': '50.0%', 'F2': '66.66%'}
所属运动队 {'gold_count': 3, 'predict_count': 2, 'right_count': 2, 'exist_count': 2, 'P': '66.66%', 'R': '100.0%', 'R2': '100.0%', 'F': '80.0%', 'F2': '80.0%'}
信仰 {'gold_count': 11, 'predict_count': 10, 'right_count': 3, 'exist_count': 3, 'P': '27.27%', 'R': '30.0%', 'R2': '100.0%', 'F': '28.57%', 'F2': '42.85%'}
场上位置 {'gold_count': 0, 'predict_count': 0, 'right_count': 0, 'exist_count': 0, 'P': -1, 'R': -1, 'F': -1}

Process finished with exit code 0
### 错误分析
   1. 位置问题明显
   2. 远程监督问题出现的漏标与错标
   3. 长实体问题

### 关系抽取
数据构造：把人物的summary和para中含有人物的实体标出来，作为标注信息


#### 训练语料构造

方法：
- 建立人物词典，把所有的人物放在里面
- 对para和summary进行标注

结果：
共有23876个关系
{'前任者': 5869, '继任者': 4040, '配偶': 3920, '子女': 2615, '亲属': 2313, '父母': 1771, '父亲': 1644, '奖项': 1040, '母亲': 520, '受影响于': 144}





模型：序列标注


问题：
    [[]]标的不全，无所谓，在关系中过滤出即可
    有的句子没有体现出关系，但是存在
        {
        "sentence": "应黎元洪的请求，袁召集了武昌起义首义者之一，被尊为共和元勋的[[张振武]]和[[方维]]，以“图谋不轨”于8月16日在北京杀害，引发临时参议院和黄兴的言辞责问",
        "relations": [
            ["袁世凯","黎元洪","继任者"]        
        ]
    },
    {
        "sentence": "尽管他在遗嘱中说“余之死骸勿付国葬，由袁家自行料理”，继任者[[黎元洪]]则以“民国肇建，……（袁）奠定大局，苦心擘画，昕夕勤劳，天不假年……所有丧葬典礼……务极优隆，用符国家崇德报功之至意”命国务院为袁世凯举办一场集古今中外皇庶官民新旧典章于一举的国葬",
        "relations": [
            ["袁世凯","黎元洪","继任者"]
        ]
    }

两种关系的：7113句话

太少，怎么办，在用规则构建数据

模型：R-BERT

目标：高质量数据


para里面也有格式化数据
```json
家庭
妻
原配妻子叶淑英，1922年6月奉父母之命在苏州结婚，次年因难产过世。第二任妻子刘期纯，1924年12月14日在上海结婚，结婚长度达70年[25]，两人育有五儿四女。

子女
长子严隽荣，上海商业储蓄银行董事。
次子严隽森，美籍华人，美东华人学术联谊会第四届会长（1979年－1981年）。
三子严隽同，美籍华人，千橡中文学校、康谷华协创办人之一。
四子严隽泰，曾任唐荣公司总经理、中华工程创办人和前董事长，2016年获蔡英文总统聘任为中华民国总统府国策顾问。
五子严隽建，曾投稿于科学月刊杂志社。
长女严隽华，上海复旦大学毕业。
次女严隽菊（Nora），嫁给维吉尼亚大学已故政治学教授冷绍烇，冷绍烇生前是维大康普顿讲座教授，亦做过蒋经国国际交流基金会咨询委员
三女严隽芸，台大农化系毕业。
四女严隽荃，嫁给东海大学经济系博士、前美国花旗银行副董事长贾培源。因思念亡妻严隽荃，贾培源先生特别在东海大学女生宿舍打造荃园，捐建一座雅致花园，将一首诗镌刻在斜躺水道的石版上（因六十多年前，他常在东海大学女生宿舍门口站岗[26]。）
孙
三子育有一女
族侄女
严隽琪、原上海市副市长、全国人大常委会副委员长、中国民主促进会主席。

```

para特点：
- 通过板块介绍，板块标题为主要内容，板块标题的结构分布
- 有的板块内容为半结构化数据，并非全是非结构化文本


通过百度百科增加数据量

对该人物添加其百度百科网页，注：如果有重定向则要全部添加

对每个网页进行抽取

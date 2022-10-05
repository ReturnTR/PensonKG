人物知识图谱构建
=========
本文档描述人物指知识图谱构建的详细流程，目前以Wiki作为数据集

目录
=======
<!-- TOC -->
- [Wiki原始语料获取](#wiki%E5%8E%9F%E5%A7%8B%E8%AF%AD%E6%96%99%E8%8E%B7%E5%8F%96)
- [数据分析与处理](#%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90%E4%B8%8E%E5%A4%84%E7%90%86)
    - [1. Wikidumpxml数据格式分析](#1-wikidumpxml%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E5%88%86%E6%9E%90)
    - [2. 网页内容（<text>标签内容）格式分析](#2-%E7%BD%91%E9%A1%B5%E5%86%85%E5%AE%B9text%E6%A0%87%E7%AD%BE%E5%86%85%E5%AE%B9%E6%A0%BC%E5%BC%8F%E5%88%86%E6%9E%90)
    - [3. 页面初步格式化抽取出上面提到的的4项](#3-%E9%A1%B5%E9%9D%A2%E5%88%9D%E6%AD%A5%E6%A0%BC%E5%BC%8F%E5%8C%96%E6%8A%BD%E5%8F%96%E5%87%BA%E4%B8%8A%E9%9D%A2%E6%8F%90%E5%88%B0%E7%9A%84%E7%9A%844%E9%A1%B9)
    - [4. 选取人物页面](#4-%E9%80%89%E5%8F%96%E4%BA%BA%E7%89%A9%E9%A1%B5%E9%9D%A2)
    - [5. 对人物Infobox进行属性抽取](#5-%E5%AF%B9%E4%BA%BA%E7%89%A9infobox%E8%BF%9B%E8%A1%8C%E5%B1%9E%E6%80%A7%E6%8A%BD%E5%8F%96)
        - [5.1. 属性的定义（抽取什么属性）](#51-%E5%B1%9E%E6%80%A7%E7%9A%84%E5%AE%9A%E4%B9%89%E6%8A%BD%E5%8F%96%E4%BB%80%E4%B9%88%E5%B1%9E%E6%80%A7)
        - [5.2. 编写抽取规则](#52-%E7%BC%96%E5%86%99%E6%8A%BD%E5%8F%96%E8%A7%84%E5%88%99)

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

经过分析，每个page可分为4个部分

| 网页部分 |             描述             |                   识别标志                   |
| :------: | :--------------------------: | :------------------------------------------: |
| Infobox  | 网页实体的属性表，贴在网页的 |    以`{{}}`为标志，在网页的开头，可能没有    |
| summary  |        网页实体的简介        |     在infobox和para之间，的一个简短文本      |
|   para   |    实体各个方面的详细介绍    | 以`==xx==`为标志，遇到的第一个就是para的开始 |
| category |      实体属于的类别链接      |  以`[[Category:xx]]`为标志，在网页的末尾  |

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

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/code/WikiProcess.py)

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

[抽取代码和模板列表](https://github.com/ReturnTR/PensonKG/blob/main/code/GetPersonViaInfobox.py)

## 对人物Infobox进行属性抽取

我们需要抽取出人物的基本属性，为此我们需要确定**属性的定义**以及**属性的抽取方法**

### 属性的定义（抽取什么属性）
由于属性在人物信息框模板里本来就定义好了，因此我们只需要将总结所有模板的属性，即将多个模板合起来形成一个大的，整体的模板

总结的工作包括：
1. 每个英文的属性一般有中文和它对应，我们需要找到对应的中英文对应的属性，例如`gender`与`性别`
2. 有的模板书会添加对属性的解释，我们需要将解释记录下来方便下一步的工作
3. 对所有模板那中出现属性的次数进行计数，用来排序
   
最后形成如下的数据形式：

```python
{
   "属性名称":{					# 英文为属性名称比较好
       "trigger":("中文","英文"),	        # 与该属性
       "count":0,       			# 在模板中出现的次数
       "explain":""				# 对该属性的解释
   }
}
```

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/code/GetBigInfobox.py)

该方案共抽出1100个属性

[抽取结果](https://github.com/ReturnTR/PensonKG/blob/main/data/infobox_templete.json)



### 编写抽取规则

查看每个属性的解释说明，编写规则进行抽取

为了规范抽取方式，采用接口进行抽取，包括：




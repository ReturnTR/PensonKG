[toc]





# Wiki原始语料获取

wiki数据源自wikidump

[Wikidump下载链接](https://dumps.wikimedia.org/zhwiki/latest/)

进入网页后选取`zhwiki-20220801-pages-articles-multistream.xml.bz2`

# 数据分析与处理

## Wikidump`xml`数据格式分析：

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

原始数据大小2.7个G，解压后有11个G，共有1294948个页面

## 网页内容（`<text>`标签内容）格式分析

经过分析，网页可分为4个部分

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

## 初步格式化(抽取出上面提到的的4项)

根据前面分析的四项，通过特定的规则将他们抽取出来，同时尽量保留原有信息

- 简介和正文繁体转简体
- 在正文和简介中，除了[[]]标签和[]标签，去掉所有的其他标签，只保留文字与标点符号
- 保留infobox与category的全部内容

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/code/WikiProcess.py)

## 抽取出有infobox的人物页面

目标是人物图谱，所以需要将人物页面截取过来，由于判断是否是人物的方法很复杂，因此先通过infobox里面的标识识别出部分的人物

为此需要先找到全部的infobox人物模板标识，Wiki提供了人物 infobox 的标识，见[分类:人物信息框模板 - 维基百科，自由的百科全书 (wikipedia.org)](https://zh.wikipedia.org/wiki/Category:人物信息框模板)（在wiki中infobox被称为信息框），例如

```xml
{{Infobox sportsperson\n| honorific_prefix = \n| name = 高敏\n| honorific_suffix = \n| image = \n....}}
```

其中`Infobox sportsperson`为infobox的开头，表示页面的类型，而该类型出来在上述的人物信息框模板中，因此该页面被认为是人物的页面

为此，我们需要将该网页下所有的模板记录在案，然后对每一个页面的infobox开头进行匹配，匹配成功则将其归类到人物页面中



代码











模板（templete）抽取

由杂乱到有序


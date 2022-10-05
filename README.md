Table of Contents
=================

Header: Strict-Transport-Security=max-age=31536000; includeSubdomains; preload
Header: X-Xss-Protection=0
Header: Vary=Accept
Header: X-Ratelimit-Reset=1664958091
Header: X-Ratelimit-Resource=core
Header: Etag=W/"7e846b8981055c5bb19271218edeb297b78cb1e08b2e589dad735bb059ec2533"
Header: X-Github-Media-Type=github.v3; format=json
Header: X-Ratelimit-Remaining=43
Header: X-Ratelimit-Used=17
Header: Access-Control-Allow-Origin=*
Header: Date=Wed, 05 Oct 2022 07:56:35 GMT
Header: Content-Type=text/html;charset=utf-8
Header: Cache-Control=public, max-age=60, s-maxage=60
Header: X-Github-Request-Id=E222:0C92:11B83C7:1283BAF:633D38B3
Header: X-Content-Type-Options=nosniff
Header: Referrer-Policy=origin-when-cross-origin, strict-origin-when-cross-origin
Header: Content-Security-Policy=default-src 'none'
Header: Server=GitHub.com
Header: Access-Control-Expose-Headers=ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateL
imit-Resource, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, X-GitHub-SSO, X-GitHub-Request-Id, Deprec
ation, Sunset
Header: X-Commonmarker-Version=0.23.6
Header: X-Ratelimit-Limit=60
Header: X-Frame-Options=deny


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

为此需要先找到全部的infobox人物模板标识，Wiki提供了人物 infobox 的标识，见[分类:人物信息框模板 - 维基百科，自由的百科全书 (wikipedia.org)](https://zh.wikipedia.org/wiki/Category:人物信息框模板)（在wiki中infobox被称为信息框）

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

为此，我们需要将该网页下所有的模板记录在案，然后对每一个页面的infobox开头进行匹配，匹配成功则将其归类到人物页面中

[抽取代码](https://github.com/ReturnTR/PensonKG/blob/main/code/GetPersonViaInfobox.py)

## 对人物Infobox进行属性抽取

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
| high_school = 
| college = [[上海交通大学安泰经济与管理学院]]<ref>{{cite web | language = zh-hans | publisher = 网易网> 教育频道>正文 | title = 姚明正式就读上海交通大学经济类本科(组图) | url = http://edu.163.com/11/1107/22/7I9RATJI00293L7F.html | author = 本文来源：新华网；责任编辑：王晓易 | date = 2011年11月7日 | accessdate = 2011年11月7日 | archive-date = 2017年8月7日 | archive-url = https://web.archive.org/web/20170807152231/http://edu.163.com/11/1107/22/7I9RATJI00293L7F.html | dead-url = no }}</ref><!-- [[香港大学]]荣誉社会科学博士<ref>{{cite web | language = zh-hans | publisher = 网易网>教育频道>考研>最新资讯>正文 | title = 姚明获颁港大名誉博士学位 梁振英亲自颁授 | url = http://edu.163.com/12/1128/13/8HDCIQSL00293NU2.html | author = 本文来源：中国新闻网；责任编辑：王晓易 | date = 2012年11月28日 | accessdate = 2012年11月28日 | archive-url = https://web.archive.org/web/20121130141208/http://edu.163.com/12/1128/13/8HDCIQSL00293NU2.html | archive-date = 2012年11月30日 | dead-url = yes }}</ref>  -->
| position    = 第六任主席
| draft_round = 1
| draft_pick = 1
| draft_team = [[休士頓火箭]]
| draft_year = 2002
| career_position = [[中鋒 (籃球)|中鋒]]
| career_start    = 1997年
| career_end      = 2011年
| career_number   = 11
| years1          = 1997－2002
| team1           = [[上海大鯊魚籃球俱樂部|上海大鯊魚]] 
| years2          = {{nbay|2002|start}}－{{nbay|2010|end}}
| team2           = [[休士頓火箭]]
| awards =
<div>
* 8×[[NBA全明星賽]]（2003－2009、2011）
* 2×[[NBA最佳陣容|NBA年度第二隊]]（2007、2009）
* 3×[[NBA最佳陣容|NBA年度第三隊]]（2004、2006、2008）
* [[NBA最佳新秀陣容|NBA最佳新秀陣容第一隊]](2003)
* 11号[[球衣]]为[[休士頓火箭]]所[[退役]]
* [[中國男子籃球職業聯賽|CBA總冠軍]]（2002）
* [[中国男子篮球职业联赛常规赛最有价值球员|CBA常规赛最有价值球员]]（2001）<ref name="联赛MVP">{{Cite web|title=CBA历届冠亚军及总决赛MVP回顾：广东八一争霸_体育频道_凤凰网|url=http://sports.ifeng.com/lanqiu/special/2013cba-finals/content-4/detail_2013_03/21/23352673_0.shtml|work=sports.ifeng.com|accessdate=2019-02-12|archive-url=https://web.archive.org/web/20190213005531/http://sports.ifeng.com/lanqiu/special/2013cba-finals/content-4/detail_2013_03/21/23352673_0.shtml|archive-date=2019-02-13|dead-url=yes}}</ref>
* 3×[[中国男子篮球职业联赛篮板王|CBA篮板王]]（2000、2001、2002）
* 3×[[中国男子篮球职业联赛盖帽王|CBA盖帽王]]（2000、2001、2002）
* 2×[[中国男子篮球职业联赛扣篮王|CBA扣篮王]]（2000、2001）
* 15号球衣被上海大鲨鱼退役
* [[勞倫斯世界體育獎#年度最佳新人獎|勞倫斯世界體育獎-年度最佳新人]]（2003）
* [[ESPN]]全球最有潛力運動員（2000）
*[[上海市]]第十一屆[[全國政協委員]](2008)
*[[上海市]]第十一屆[[全國政協委員|全國政協委員會常務委員]](2008)
*[[上海市]]第十二屆[[全國政協委員]](2013-2017)
*[[上海市]]第十三屆[[全國政協委員]](2017－)
*[[劳伦斯世界体育奖#年度体育精神奖|劳伦斯世界体育奖-年度体育精神奖]]（2015）
* 3×[[亞洲盃籃球賽]]MVP（2001、2003、{{tsl|en|2005 FIBA Asia Championship|2005}}）
|stats_league = NBA
|stat1label = [[得分]]
|stat1value = 9,247（場均19.0分）
|stat2label = [[籃板]]
|stat2value = 4,494（場均9.2個）
|stat3label = [[助攻]]
|stat3value = 920（場均1.9次）
|letter = m
|bbr = mingya01
|HOF_player=yao-ming
|medaltemplates = 
{{MedalCountry|{{CHN-1949}}}}
{{MedalSport|男子篮球}}
{{MedalCompetition|亞洲青年籃球錦標賽}}
{{MedalGold|1998年印度西孟加拉邦加爾各答|}}
{{MedalCompetition|東亞運動會}}
{{MedalGold|2001年日本大阪府|}}
{{MedalCompetition|[[亚洲篮球锦标赛]]}}
{{MedalGold|{{tsl|en|2001 ABC Championship|2001年中國上海市}}|}}
{{MedalGold|{{tsl|en|2003 ABC Championship|2003年中國黑龍江省哈爾濱市}}|}}
{{MedalGold|{{tsl|en|2005 FIBA Asia Championship|2005年卡達杜哈}}|}}
{{MedalCompetition|夏季世界大學生運動會}}
{{MedalSilver|2001年中國北京市|}}
{{MedalCompetition|亞洲運動會}}
{{MedalSilver|[[2002年亞洲運動會|2002年韓國釜山廣域市]]|}}
}}
```

我们需要抽取出人物的基本属性，为此我们需要确定属性的含义以及属性的抽取方法

步骤：

1. 将模板的属性表全部列出，形成一个大的，整体的模板，包括：

1. 1. 对每个infobox模板拆分，这时一个属性的内容有：中文，英文，额外格式信息
   2. 将重复的放在一起，并计数，重复的包括英文和中文

   最后形成如下的结构：

   ```python
   {
       "属性名称":{					# 英文为属性名称比较好
           "trigger":("中文","英文"),	# 与该属性
           "count":0,       			# 在模板中出现的次数
           "explain":""				# 对该属性的解释
       }
   }
   ```

2. 分析模板中的属性值，设计抽取规则



模









模板（templete）抽取

由杂乱到有序


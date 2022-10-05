import re

# 保留原格式信息
# 前提：大括号里不能包含方括号


def value_split(s):
    # 删除ref标签，否则会抽取错误信息

    # 添加一些其他信息，比如逗号分隔


    # 标签是有优先级大小的，最小的是[[]]，其次是{{}}，其中{{}}可能包含[[]]
    # {{}}标签也可能包含{{}}本身的标签
    # 优先级
    #

    # 对没有意义的标签进行替换
    wiki_labels = WikiLabels()
    s=re.sub("\{\{.*?\}\}",wiki_labels.match_process,s) # 对有意义的标签进行替换

    s=del_ref(s)
    # 对br标签，大括号标签，中括号标签进行分割
    s=re.split("(<br[ ]*/*>|\[\[.*?\]\]|\{\{.*?\}\})",s)
    # 去掉空项，去掉br标签
    s=[i.strip() for i in s]
    s=[i for i in s if i and i[0]!="<"]
    # 去掉每一项的标签标志，变成纯文本，将其标志存到另一个列表里
    s = [i for i in s if i not in ",，、 "]


    label=[0]*len(s)
    for i in range(len(s)):
        if len(s[i])>1:
            if s[i][:2]=="{{":
                s[i]=s[i][2:-2]
                label[i]=2
            elif s[i][:2]=="[[":
                label[i] = 1
                s[i] = s[i][2:-2]

    for i in range(len(s)):
        if "、" in s[i]:
            s[i]=s[i].split("、")
            s[i]=[j for j in s[i] if j]

    return s,label


def del_ref(s):
    # 去掉ref标签
    return re.sub("\<ref.*?\>.*?\<[ ]*/[ ]*ref[ ]*\>","",s)




class WikiLabels():
    """
    针对特定的标签所做的事
    一次只能处理一个标签
    标签类型：{{xxxx}}
    """
    def process(self,s):

        # 识别特定标识，连接句柄
        cmd=[
            ["hlist",None],   # {{hlist|工程师|教授}}, 表示普通的列表
            ["link-ja",None],   # 该标签表示为一个日本wiki标签  {{link-ja|黑澤久雄|黒澤久雄}}
            ["Plainlist",None],      # 一个列表，中间没有"|"分割，用的是"\n*", 不过这个已经被截取infobox的操作消除了
            ["flagicon",self.flag_icon]
        ]

        for item in cmd:
            if item[0] in s:
                s = s[2:-2]  # 去掉前后的括号,开始接下来的操作
                if item[1] is not None:
                    # 自定义方法
                    s=item[1](s)
                    return s

                else:
                    s = s.replace(item[0], "").replace("|","、")
                    # s = s.split("|")
                    # s = [i for i in s if i]
                    return s

        return s

    def match_process(self,matched):
        s=matched.group()
        s=self.process(s)
        return s

    def flag_icon(self,s):
        return s


if __name__=="__main__":
    wiki_labels = WikiLabels()
    s="[[威廉·狄尔泰]]<br>[[弗里德里希·威廉·席尔马赫]]<br>[[菲利普·贾菲]]<br>hehe"
    # s="{{FRA}}[[上薩瓦省]][[克呂斯]]<br>hehe"
    s="168億美元(至2020年11月)<ref name=Forbes>{{cite web|url=http://www.forbes.com/profile/li-shufu/|title=Forbes profile:Li Shufu李書福|accessdate=2020-11-02|archive-date=2021-03-24|archive-url=https://web.archive.org/web/20210324223917/https://www.forbes.com/profile/li-shufu/|dead-url=no}}</ref>"
    s=value_split(s)
    s="{{marriage|[[约阿基姆王子 (丹麦)|約阿基姆王子]]|1995年11月18日|2005年4月8日|reason=divorced|}}"
    s=re.sub("\{\{.*?\}\}",wiki_labels.match_process,s)
    print(s)



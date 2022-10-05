# coding=utf-8
# Time : 2022/10/5 13:54
# Description : 通过infobox标签获取人物页面
from tqdm import tqdm
from .CommonTools.JsonTool import *

def get_infobox_templete():

    person_infobox_templete=[
        "Infobox academic",
        "Infobox architect",
        "Infobox Buddhist",
        "Infobox comics creator",
        "Infobox criminal",
        "Infobox_Prisoner",
        "Infobox Christian leader",
        "Infobox person",
        "Infobox economist",
        "Infobox EPW",
        "Infobox FBI Ten Most Wanted",
        "艺人"
        "Infobox online streamer",
        "Infobox person",
        "Infobox professional wrestler",
        "Infobox spy",
        "Politician",
        "Infobox Tulku",
        "Infobox video game player",
        "Infobox vtuber",
        "Infobox War on Terror detainee",
        "Infobox Wikipedia user",
        "Infobox medical person",
        "Infobox pageant titleholder",
        "Infobox religious biography",
        "Infobox Taoist",
        "Infobox writer",
        "Infobox YouTube personality",
        "中國古代人物信息框",
        "中國古代人物信息框",
        "Infobox military person",
        "東亞男性歷史人物",
        "Infobox saint",
        "AV女優",
        "Infobox ACG creator",
        "Infobox adult biography",
        "Infobox artist",
        "Infobox comedian",
        "Infobox model",
        "Infobox Sakamichi-series member",
        "Infobox entertainer",
        "配音員",
        "歌人",
        "Infobox chef",
        "Infobox astronaut",
        "哲学家",
        "Infobox scientist",
        "classical composer",
        "classical",
        "Infobox sportsperson",
        "中国死刑犯",
        "Infobox person",
        "Infobox monarchy",
        "Infobox noble",
        "Infobox royalty",
        "Infobox basketball biography",
        "Infobox cyclist",
        "Infobox NBA Player",
        "Infobox football biography",
        "Infobox NFL player",
        "Infobox Badminton player",
        "Infobox volleyball biography",
        "Infobox racing driver",
        "Infobox short track speed skater",
        "Infobox skier",
        "Infobox alpine ski racer",
        "Infobox speed skater",
        "Infobox tennis player season",
        "Infobox boxer",
        "Infobox baseball biography",
        "Infobox baseball player",
        "Infobox Paralympic",
        "Infobox football official",
        "Infobox F1 driver",
        "Infobox handball biography",
        "Infobox badminton player",
        "Infobox figure skater",
        "Infobox go player",
        "Infobox golfer",
        "Infobox officeholder",
        "Infobox_officeholder"
        "Infobox ice hockey player",
        "Infobox snooker player",
        "Infobox speedcubing player",
        "Infobox swimmer",
        "Infobox table tennis player",
        "Infobox tennis biography",
        "Infobox 體操選手",
        "壁球選手信息框",
        "Infobox band",
        "Infobox Singer",
        "Infobox Band",
        "Infobox singer",
        "Infobox musical artist",
        "Infobox actor",
        "Infobox Actor",
        "監製資訊框",
        "Infobox Musician",
        "Infobox Musical artist",
        "Infobox dancer",
        "Infobox musician",
        "相聲小品演員",
        "相聲小品藝術家",
        "Infobox Chinese-language singer and actor",
        "Infobox Dancer",
        "Infobox entertainer",
        "ActorActress",
        "演員資訊框",
        "Infobox filmmaker",
        "Infobox Filmmaker",
        "Infobox magician",
        "Infobox director",
        "Infobox actress",
        "Infobox performer",
        "Infobox Actress",
        "Infobox film actor",
        "Infobox photographer",
        "Infobox film director",
        "芸能人",
        "Infobox sports announcer",
        "Infobox presenter",
        "Infobox radio host",
        "Infobox Radio host",
        "Infobox sports announcer details",
        "Infobox Astronaut",
        "宇航员信息框",
        "Infobox Political EPW",
        "Infobox Biography",
        "Infobox Celebrity",
        "Infobox People",
        "Infobox fashion designer",
        "Infobox journalist",
        "Infobox people",
        "Infobox Person",
        "人物信息框",
        "網民信息框",
        "Infobox Profile",
        "Infobox Fashion Designer",
        "Personbox",
        "Infobox victim",
        "Infobox vcelebrity",
        "Infobox biography",
        "Infobox Military Person",
        "军人",
        "军人模板",
        "中国人民解放军将领",
        "中国死刑犯",
        "Infobox People CAE",
        "Infobox People CAS",
        "Infobox AM",
        "Infobox Canadian MP",
        "Infobox Canadian senator",
        "Infobox candidate",
        "Infobox chairman",
        "Infobox chancellor",
        "Infobox congressional candidate",
        "Infobox congressman",
        "Infobox defense minister",
        "Infobox deputy first minister",
        "Infobox deputy prime minister",
        "Infobox doge",
        "Infobox Eritrea cabinet official",
        "Infobox first lady",
        "Infobox first minister",
        "Infobox governor",
        "Infobox governor-elect",
        "Infobox governor general",
        "Infobox governor-general",
        "Infobox Indian politician",
        "Infobox judge",
        "Infobox lt governor",
        "Infobox mayor",
        "Infobox MEP",
        "Infobox minister",
        "Infobox MLA",
        "Infobox MP",
        "Infobox MSP",
        "Infobox PM",
        "Infobox politician",
        "Infobox politician (general)",
        "Infobox premier",
        "Infobox premier Canada",
        "Infobox president",
        "Infobox president-elect",
        "Infobox prime minister",
        "Infobox prime minister-elect",
        "Infobox representative-elect",
        "Infobox SCC chief justice",
        "Infobox SCC puisne justice",
        "Infobox secretary-general",
        "Infobox senator",
        "Infobox senator-elect",
        "Infobox speaker",
        "Infobox state representative",
        "Infobox state SC associate justice",
        "Infobox state SC justice",
        "Infobox state senator",
        "Infobox US ambassador",
        "Infobox Military Person",
        "军人",
        "军人模板",
        "中国人民解放军将领",
        "peer",
        "基礎情報 ",
        "朝鮮半島",
        "琉球群島",
        "百越",
        "越南",
        "中国宗室信息框",
        "Infobox MLB player",
        "Infobox_officeholder",
        "Infobox_Person",
        "Infobox Monarch",
        "Infobox US Cabinet official",
        "Infobox Korean name",
        "Infobox Officeholder",
        "Infobox_Officeholder"
        "Infobox Go player",
        "Infobox_Scientist",
        "乒乓球",
        "Infobox Writer",
        "Infobox classical",
        "Infobox CPBL player",
        "Infobox 羽球選手"
    ]
    templete_set=set(person_infobox_templete)
    for i in person_infobox_templete:
        if "Infobox " in i:
            templete_set.add(i.replace("Infobox ","Infobox_"))
    person_infobox_templete=list(templete_set)
    return person_infobox_templete

def get_person_via_infobox(filename,des_filename):
    """根据模板获取人物的网页"""
    person_infobox_templete=get_infobox_templete()
    data=load_json(filename)
    new_data=[]
    count=0
    pbar=tqdm(data)
    for item in pbar:
        if "infobox" in item and item["infobox"]:
            for templete in person_infobox_templete:
                if templete in item["infobox"][:3+len(templete)]:
                    new_data.append(item)
                    count+=1
                    pbar.set_description("已记录{}个".format(count))
                    break
    save_json(new_data,des_filename)


if __name__ == "__main__":
    get_person_via_infobox("data/wiki_page_1294978.json", "data/wiki_page_person.json")
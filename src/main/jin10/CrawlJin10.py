import time

import requests
import datetime
import pymysql
from requests.adapters import HTTPAdapter

from logger import logger

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from dao.MysqlHelper import MysqlHelper

aaa = {
    "country": ["中国", "蒙古", "朝鲜", "韩国", "日本 ", "菲律宾", "越南", "老挝", "柬埔寨", "缅甸", "泰国", "马来西亚", "文莱", "新加坡", "印度尼西亚", "东帝汶 ", "尼泊尔", "不丹", "孟加拉国", "印度", "巴基斯坦", "斯里兰卡", "马尔代夫", "哈萨克斯坦", "吉尔吉斯斯坦", "塔吉克斯坦", "乌兹别克斯坦", "土库曼斯坦", "阿富汗", "伊拉克", "伊朗", "叙利亚", "约旦", "黎巴嫩", "以色列", "巴勒斯坦", "沙特阿拉伯", "巴林", "卡塔尔", "科威特", "阿拉伯联合酋长国(阿联酋)", "阿曼", "也门", "格鲁吉亚", "亚美尼亚", "阿塞拜疆", "土耳其", "塞浦路斯", "芬兰", "瑞典", "挪威", "冰岛", "丹麦 法罗群岛(丹)", "爱沙尼亚", "拉脱维亚", "立陶宛", "白俄罗斯", "俄罗斯", "乌克兰", "摩尔多瓦", "波兰", "捷克", "斯洛伐克", "匈牙利", "德国", "奥地利", "瑞士", "列支敦士登", "英国", "爱尔兰", "荷兰", "比利时", "卢森堡", "法国", "摩纳哥", "罗马尼亚", "保加利亚", "塞尔维亚", "马其顿", "阿尔巴尼亚", "希腊", "斯洛文尼亚", "克罗地亚", "波斯尼亚和墨塞哥维那", "乍得", "中非", "喀麦隆", "赤道几内亚", "加蓬", "刚果(布)", "刚果(金)", "圣多美及普林西比", "毛里塔尼亚", "西撒哈拉", "塞内加尔", "冈比亚", "马里", "布基纳法索", "几内亚", "几内亚比绍", "佛得角", "塞拉利昂", "利比里亚", "科特迪瓦", "加纳", "多哥", "贝宁", "尼日尔", "加那利群岛(西)", "赞比亚", "安哥拉", "津巴布韦", "马拉维", "莫桑比克", "博茨瓦纳", "纳米比亚", "南非", "斯威士兰", "莱索托", "马达加斯加", "科摩罗", "毛里求斯", "留尼旺(法)", "圣赫勒拿(英)", "澳大利亚", "新西兰", "巴布亚新几内亚", "所罗门群岛", "瓦努阿图", "密克罗尼西亚", "马绍尔群岛", "帕劳", "瑙鲁", "基里巴斯", "图瓦卢", "萨摩亚", "斐济群岛", "汤加", "库克群岛(新)", "关岛(美)", "新喀里多尼亚(法)", "法属波利尼西亚", "皮特凯恩岛(英)", "瓦利斯与富图纳(法)", "纽埃(新)", "托克劳(新)", "美属萨摩亚", "北马里亚纳(美)", "加拿大", "美国", "墨西哥", "格陵兰(丹)", "危地马拉", "伯利兹", "萨尔瓦多", "洪都拉斯", "尼加拉瓜", "哥斯达黎加", "巴拿马", "巴哈马", "古巴", "牙买加", "海地", "多米尼加共和国", "安提瓜和巴布达", "圣基茨和尼维斯", "多米尼克", "圣卢西亚", "圣文森特和格林纳丁斯", "格林纳达", "巴巴多斯", "特立尼达和多巴哥", "波多黎各(美)。", "英属维尔京群岛", "美属维尔京群岛", "安圭拉(英)", "蒙特塞拉特(英)", "瓜德罗普(法)", "马提尼克(法)", "荷属安的列斯", "阿鲁巴(荷)", "特克斯和凯科斯群岛(英)", "开曼群岛(英)", "百慕大(英)", "哥伦比亚", "委内瑞拉", "圭亚那", "法属圭亚那", "苏里南", "厄瓜多尔", "秘鲁", "玻利维亚", "巴西", "智利", "阿根廷", "乌拉圭", "巴拉圭", "意大利", "梵蒂冈", "圣马力诺", "马耳他", "西班牙", "葡萄牙", "安道尔", "埃及", "利比亚", "苏丹", "突尼斯", "阿尔及利亚", "摩洛哥", "亚速尔群岛(葡)", "马德拉群岛(葡)", "埃塞俄比亚", "厄立特里亚", "索马里", "吉布提", "肯尼亚", "坦桑尼亚", "乌干达", "卢旺达", "布隆迪", "塞舌尔"],
    "type": ["黄金", "白银", "原油", "美元指数", "新冠肺炎", "非农", "快讯", "利率", "行情", "纳指", "道指", "标普", "楼市", "钯金", ""]
}


# 爬虫获取页面数据
url = "https://flash-api.jin10.com/get_flash_list"
header = {
    "x-app-id": "SO1EJGmNgCtmpcPF",
    "x-version": "1.0.0",
}
queryParam = {
    "max_time": "2020-09-03 22:00:00",
    "channel": "-8200",
}

insert_template = "insert into jin10(jid, createTime, country, fmt_type, coarseness, info, outline, provenance) values (%s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update country=values(country)"

mysql_helper = MysqlHelper("wedo.com", "wedo", "233288#Adnine", "wedo")

def conn():
    connect = pymysql.connect(host='wedo.com', user='wedo', password='233288#Adnine', database='wedo', charset='utf8')
    if connect:
        logger.info("连接成功!")
    return connect


def parse_content(content):
    # content = str(content)
    content = content.strip()
    country = fmt_type = coarseness = outline = provenance = info = None

    for c in aaa["country"]:
        if content.__contains__(c):
            country = c

    for t in aaa["type"]:
        if content.__contains__(t):
            fmt_type = t

    if content.startswith("【"):
        content = content.replace("【", "")
        if content.__contains__("："):
            coarseness = content.split("：", 1)[0]
            outline = content.split("：", 1)[1]
            info = content.split("】")[1]

        else:
            if content.__contains__("】"):
                coarseness = content.split("】")[0]
                info = content.split("】")[1]
            else:
                info = content

    elif content.__contains__("："):
        coarseness = content.split("：", 1)[0]
        info = content.split("：", 1)[1]
    else:
        info = content

    if content.endswith("）"):
        p = "（"
        if not info.__contains__(p):
            p = "("
        arr = info.rsplit(p, 1)
        info = arr[0]
        if len(arr) >1:
            provenance = arr[1]
            provenance = provenance.replace("）", "")

    return country, fmt_type, coarseness, info, outline, provenance


def convert_es_data(d):
    doc = {"createTime": d[1], "info": d[5]}
    if d[2]:
        doc["country"] = d[2]
    if d[3]:
        doc["fmt_type"] = d[3]
    if d[4]:
        doc["coarseness"] = d[4]
    if d[6]:
        doc["outline"] = d[6]
    if d[7]:
        doc["provenance"] = d[7]

    return {"_index": "jin10",
            # "_type": "review_feature",
            "_id": d[0],
            "_source": doc}


es = Elasticsearch("wedo.com", port=9200)


def main():
    # 循环爬取并插入数据：结束条件是爬不到数据为止
    totalCount = 0
    with open("record", 'r') as f:
        queryParam["max_time"] = f.read()
    Data = requests.get(url, queryParam, headers=header).json()['data']
    length = len(Data)
    while length > 0:
        convert_data = []
        convert_docs = []
        for i in range(length):
            id = Data[i]['id']
            create_time = Data[i]['time']
            ta = time.strptime(create_time, "%Y-%m-%d %H:%M:%S")
            jid = int(time.mktime(ta)) * 10000 + int(id[14:-2])
            # create_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            type = Data[i]['type']
            if type == 0:
                if len(Data[i]['data']) > 2:
                    # pic = Data[i]['data']['pic']
                    content = Data[i]['data']['content']
                    # title = Data[i]['data']['title']
                elif len(Data[i]['data']) == 1:
                    # pic = None
                    content = Data[i]['data']['content']
                    # title = None
                else:
                    # pic = Data[i]['data']['pic']
                    content = Data[i]['data']['content']
                    # title = None

                l = list(parse_content(content))
                l.insert(0, create_time)
                l.insert(0, jid)

                convert_data.append(tuple(l))
                convert_docs.append(convert_es_data(l))
                # try:
                #
                #     sql = "insert into  jin10_data(id,create_time,type,pic,content,title) values(%s,%s,%s,%s,%s,%s)"
                #     cursor = conn.cursor()
                #     cursor.execute(sql, (id, create_time, type, pic, content, title))
                #     conn.commit()
                #     cursor.close()
                # except Exception as e:
                #     print(e)
                #     continue
                #
            # continue
        helpers.bulk(es, convert_docs)
        mysql_helper.insert_bulk(insert_template, convert_data)
        totalCount += length

        # 修正下一个查询时间
        queryParam['max_time'] = Data[length - 1]['time']
        with open('record', 'w') as f:
            f.write(queryParam['max_time'])
        logger.info('next queryParam is {}'.format(queryParam['max_time']))

        # 再请求一次数据
        # time.sleep(30)
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        Data = requests.get(url, queryParam, timeout=5, headers=header).json()['data']
        length = len(Data)

    logger.info('all ok,totalCount is:', totalCount)


if __name__ == '__main__':
    main()
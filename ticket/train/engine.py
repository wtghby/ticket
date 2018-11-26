# -*- coding: UTF-8 -*-
import requests
import re
from ticket.train.stations import stations


class Engine(object):
    b_stations = None

    def __init__(self):
        self.url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={0}&leftTicketDTO' \
                   '.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT'
        self.header = {
            "User-Agent":
                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/"
                "537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }

    def query(self, start, end, date):
        if Engine.b_stations is None:
            Engine.b_stations = self.get_stations()
        s = Engine.b_stations[start]
        e = Engine.b_stations[end]

        url = self.url.format(date, s, e)
        print(url)
        web_data = requests.get(url, headers=self.header)  # verify=False表示不判断证书
        web_data.encoding = "utf-8"
        print(web_data)
        # 返回的结果，转化成json格式，取出data中的result方便后面解析列车信息用
        datas = web_data.json()["data"]["result"]
        results = []
        for data in datas:
            item = {}
            data = data.split("|")
            item['remark'] = data[1]  # 备注
            item['number'] = data[3]  # 车次
            item['start_station'] = data[4]  # 始发站
            item['end_station'] = data[5]  # 终点站
            item['start_station_ch'] = self.get_stations_key(item['start_station'])  # 始发站变为中文 如SZQ表示深圳站
            item['end_station_ch'] = self.get_stations_key(item['end_station'])  # 终点站变为中文
            item['from_station'] = data[6]  # 出发地简称
            item['to_station'] = data[7]  # 目的地简称
            item['from_station_ch'] = self.get_stations_key(item['from_station'])  # 出发地变为中文
            item['to_station_ch'] = self.get_stations_key(item['to_station'])  # 目的地变为中文
            item['departure_time'] = data[8]  # 出发时间
            item['arrival_time'] = data[9]  # 结束时间
            item['cost_time'] = data[10]  # 花费时间
            # 普快
            item['soft_bed'] = data[-14] if data[-14].strip() != "" else "-"  # 软卧
            item['no_seat'] = data[-11] if data[-11].strip() != "" else "-"  # 普快无座
            item['hard_bed'] = data[-9] if data[-9].strip() != "" else "-"  # 硬卧
            item['hard_seat'] = data[-8] if data[-9].strip() != "" else "-"  # 硬座
            # 高铁/动车
            item['crh_no_seat'] = data[-11] if data[-11].strip() != "" else "-"  # 高铁无座
            item['second_seat'] = data[-7] if data[-7].strip() != "" else "-"  # 二等座
            item['first_seat'] = data[-6] if data[-6].strip() != "" else "-"  # 一等座
            item['business_seat'] = data[-5] if data[-5].strip() != "" else "-"  # 商务座
            item['special_seat'] = data[-12] if data[-12].strip() != "" else "-"  # 特等座
            item['crh_bed'] = data[-4] if data[-4].strip() != "" else "-"  # 动车动卧
            results.append(item)

            print(item['number'] + '---' + item['start_station_ch'] + '---' + item['end_station_ch'] + '---' + item[
                'from_station_ch'] + '---' + item['to_station_ch'])
        return results

    # 根据值value获取字典stations的key值，如get_stations_key('SZQ') = '深圳'
    def get_stations_key(self, value):
        key = list(stations.keys())[
            list(stations.values()).index(
                value)]  # 参考链接https://blog.csdn.net/ywx1832990/article/details/79145576
        return key

    # 获取站名的中文和大写英文简称对应的值，以字典形式保存
    def get_stations(self):
        # 该url是在NetWork的station_name.js?station_version=1.9075中获得
        # 版本官网会不定时更新
        url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9075"
        web_data = requests.get(url)
        web_data.encoding = "utf-8"
        # 　使用正则表达式提取所有的站点：汉字和对应的大写字母简称
        sta = dict(re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', web_data.text))
        return sta

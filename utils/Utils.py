# -*- coding: utf-8 -*-
"""
@Time        : 2020/7/19 12:25
@Author      : NingWang
@Email       : yogehaoren@gmail.com
@File        : Utils.py
@Description : 
@Version     : 0.1-dev
"""
import requests
import pickle

DEFAULT_HEADER = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.64",
    "X-Requested-With": "XMLHttpRequest",
}

UPLOAD_HEADER = {
    "Referer": "https://xxcapp.xidian.edu.cn/site/ncov/xisudailyup",
    "Origin": "https://xxcapp.xidian.edu.cn",
}

DEFAULT_UPLOAD_MESSAGE = {
    "geo_api_info": "{\"type\":\"complete\",\"info\":\"SUCCESS\",\"status\":1,\"VDa\":\"jsonp_156697_\",\"position\":{\"Q\":34.121994628907,\"R\":108.83715983073,\"lng\":108.83716,\"lat\":34.121995},\"message\":\"Get ipLocation success.Get address success.\",\"location_type\":\"ip\",\"accuracy\":null,\"isConverted\":true,\"addressComponent\":{\"citycode\":\"029\",\"adcode\":\"610116\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"雷甘路\",\"streetNumber\":\"264号\",\"country\":\"中国\",\"province\":\"陕西省\",\"city\":\"西安市\",\"district\":\"长安区\",\"township\":\"兴隆街道\"},\"formattedAddress\":\"陕西省西安市长安区兴隆街道西安电子科技大学长安校区办公辅楼\",\"roads\":[],\"crosses\":[],\"pois\":[]}",
    "area": "陕西省 西安市 长安区",  # 地区
    "city": "西安市",  # 城市
    "province": "陕西省",  # 省份
    "address": "陕西省西安市长安区兴隆街道西安电子科技大学长安校区行政辅楼",  # 实际地址
}

LOGIN_URL = "https://xxcapp.xidian.edu.cn/uc/wap/login/check"

UPLOAD_URL = "https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save"

COOKIE_FILE_NAME = "cookie.txt"


def get_cookie_from_login(student_id: str, password: str):
    """
    登录获取cookie
    :param student_id: 学号
    :param password:  密码
    :param cookie_file_path cookies文件路径
    :return:
    """
    r = requests.post(LOGIN_URL, data={"username": student_id, "password": password}, headers=DEFAULT_HEADER)
    if r.status_code == 200:
        if r.json()['e'] == 0:
            print("登录成功")
            # with open(cookie_file_path, 'wb') as f:
            #     pickle.dump(r.cookies, f)

            return "ok", r.cookies

        else:
            print(r.json()['m'])
            return "登录失败, 请检查用户名或密码是否正确:%s" % r.json()['m'], ""



# def load_cookie_from_file(cookie_file_path: str):
#     """
#     从文件中加载cookie
#     :param cookie_file_path: 文件路径
#     :return:
#     """
#     with open(cookie_file_path, 'rb') as f:
#         return pickle.load(f)


def load_upload_message_file(file_path: str):
    """
    从文件中解析需要提交的信息
    :param file_path: 文件路径
    :return:
    """
    with open(file_path, "r", encoding='utf8') as f:
        text = f.read()
        upload_message = eval(text)
        for key, value in DEFAULT_UPLOAD_MESSAGE.items():
            if key not in upload_message:
                upload_message[key] = value
        return upload_message


def upload_ncov_message(cookie, upload_message):
    header = dict(DEFAULT_HEADER.items() | UPLOAD_HEADER.items())
    r = requests.post(UPLOAD_URL, cookies=cookie, headers=header)
    if r.json()['e'] == 0:
        print("上报成功")
        return "ok"
    else:
        print("上报出现错误!")
        print("错误信息: ", r.json()['m'])
        return "上报出现错误!，错误信息:%s" % r.json()['m']


if __name__ == '__main__':
    pass

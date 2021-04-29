import json

import requests
import urllib3


def abc():
    sql = "select warehouse_priority_config_id as id from division_compartment_config where created_time='2021-04-25 10:00:00'"

    priority_lst = send_request_yaernings(sql)
    priority_id_lst = [priority_id_dict['id'] for priority_id_dict in priority_lst]
    priority_id_str = ",".join(priority_id_lst)

    sql2 = f"SELECT * from warehouse_priority_config_detail WHERE warehouse_priority_config_id IN ({priority_id_str})"
    detail = send_request_yaernings(sql2)
    for detail_lst in detail:
        print(detail_lst)


def send_request_yaernings(key_word):
    url = "https://yaernings-prod.viomi.com.cn/api/v2/query"
    heads = {
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTk0MzM4NjMsIm5hbWUiOiJwZW5na2FpbGlhbmciLCJyb2xlIjoiZ3Vlc3QifQ.C_zQ8ZsScMk20x4TemkR9swHyLh3TJDsh50KmVv4rOw',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': 'KLBRSID=9b7a9e701b529f7aa407ca50f2f37247|1619413680|1619405019',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    sql = key_word
    # print(sql)
    data = {"basename": "vm_warehouse",
            "source": "prod_express_read_134",
            "sql": sql}
    urllib3.disable_warnings()
    res = requests.post(url=url, headers=heads, data=json.dumps(data), verify=False)
    yaernings_json = res.text  # 返回的json
    yaernings_dict = json.loads(yaernings_json)
    return yaernings_dict['data']


if __name__ == '__main__':
    abc()

import json

import requests
import urllib3


# 连接yaerning,返回列表数据
def yaerning(sql, authorization, cookie, database):
    url = "https://yaernings-prod.viomi.com.cn/api/v2/query"
    heads = {
        'authorization': f'Bearer {authorization}',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': f'KLBRSID={cookie}',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    data = {"basename": database,
            "source": "prod_express_read_134",
            "sql": sql}
    urllib3.disable_warnings()
    res = requests.post(url=url, headers=heads, data=json.dumps(data), verify=False)
    yaerning_json = res.text  # 返回的json
    yaerning_dict = json.loads(yaerning_json)
    if 'data' in dict(yaerning_dict).keys():
        return yaerning_dict['data']


# 均分列表
def divide(lst, flag):
    result_lst = []
    for i in range(0, len(lst), flag):
        portion_lst = lst[i:i + flag]
        result_lst.append(portion_lst)
    return result_lst


def write_file(filename, data_lst):
    filepath = f"C:\\Users\\Administrator\\Desktop\\{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        for line in data_lst:
            f.write(line)
            # f.write('\n')


if __name__ == '__main__':
    pass

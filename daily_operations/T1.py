import json

import requests
import urllib3

import tool.tools as tool
from tool import excel


def start():
    filename = "期初库存导入数据京东西安仓--已导入.xlsx"
    excel_obj = excel.Excel(filename=filename, flag="DW")
    excel_data = excel_obj.data
    index = 1  # 从第二行开始读
    product_code_lst = []
    data = {}
    warehouse_code_lst = ['110009250']
    data['warehouseCodeList'] = warehouse_code_lst
    url = 'https://ms.viomi.com.cn/warehouse-web/services/centerWarehouse/skuStock/synWMSSkuStock'
    heads = {
        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    while index < len(excel_data):
        product = excel_data[index]
        index += 1
        try:
            product_code = int(float(product.strip()))
            product_code_lst.append(product_code)
        except Exception as e:
            print(e)
            continue
    l = list(set(product_code_lst))
    print(len(l))
    divide = tool.divide(l, 10)
    for d in divide:
        data['itemCodeList'] = d
        data_json = json.dumps(data)
        print(data_json)
        urllib3.disable_warnings()
        res = requests.post(url=url, headers=heads, data=data_json, verify=False)
        print(res.json())


if __name__ == '__main__':
    start()

import json

import requests
import urllib3

import tool.tools as tool
from tool import excel

warehouse_name = "宅急送合肥仓"
warehouse_code = "ZJSHF001"
warehouse_id = 459
token = "aE9TcH9TBZZKTeNh"
prod_url = "https://ms.viomi.com.cn/warehouse-web/services/"
limit_flag = 0

heads = {
    'content-type': 'application/json;charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}


def b():
    warehouse_name = "宅急送北京仓"
    warehouse_code = "ZJSBJ"
    warehouse_id = 763


def c():
    time = "2021年05月01日 18：00"


def update_warehouse_dict_value():
    url = prod_url + f"warehouse/common/updateWarehouseDictValue?token={token}&id=97&value={limit_flag}&code=compartment_limit_flag&groupCode=ServiceFlag"
    urllib3.disable_warnings()
    res = requests.post(url=url, headers=heads, verify=False)
    print("更新分仓限制开关", res.json())
    url2 = prod_url + f"warehouse/common/updateWarehouseDictValue?token={token}&id=98&code=compartment_limit_warehouse_id_list&value={warehouse_id}&groupCode=ServiceFlag"
    res2 = requests.post(url=url2, headers=heads, verify=False)
    print("更新分仓限制开关仓库", res2.json())


def update_wms_route_message():
    url = prod_url + "warehouse/common/updateWmsRouteMessage.json"
    data1 = {"wmsRouteMessageCode": "wms_owner_code",
             "wmsUpdateRouteMessageBasicDTOS": [{"warehouseId": warehouse_id, "value": "YM_FLUX"}]}
    data2 = {"wmsRouteMessageCode": "customer_id",
             "wmsUpdateRouteMessageBasicDTOS": [{"warehouseId": warehouse_id, "value": "YM_FLUX"}]}
    urllib3.disable_warnings()
    res1 = requests.post(url=url, headers=heads, data=json.dumps(data1), verify=False)
    print("更新wms_owner_code", res1.json())
    res2 = requests.post(url=url, headers=heads, data=json.dumps(data2), verify=False)
    print("更新customer_id", res2.json())


def start():
    filename = "期初库存导入数据京东西安仓--已导入.xlsx"
    excel_obj = excel.Excel(filename=filename, flag="DW")
    excel_data = excel_obj.data
    index = 1  # 从第二行开始读
    product_code_lst = []
    data = {}
    warehouse_code_lst = [warehouse_code]
    data["warehouseCodeList"] = warehouse_code_lst
    url = prod_url + "centerWarehouse/skuStock/synWMSSkuStock"
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
    update_warehouse_dict_value()

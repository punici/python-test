import json
import os

import requests
import urllib3

import tool.excel as excel
import tool.tools as tools


def deal_data():
    filename = "新增店铺维度分仓规则导入模板(3).xlsx"
    excel_obj = excel.Excel(filename=filename)
    excel_data = excel_obj.data
    start_flag = 1
    config_id = 7000
    config_sku_id = 786000
    priority_id = 7000
    priority_detail_id = 15000
    create_time = "'2021-04-25 10:00:00'"
    create_status = 1

    # 保存
    save_filepath_1 = f"C:\\Users\\Administrator\\Desktop\\sql\\division_compartment_config.txt"
    save_filepath_2 = f"C:\\Users\\Administrator\\Desktop\\sql\\division_compartment_config_sku.txt"
    save_filepath_3 = f"C:\\Users\\Administrator\\Desktop\\sql\\warehouse_priority_config.txt"
    save_filepath_4 = f"C:\\Users\\Administrator\\Desktop\\sql\\warehouse_priority_config_detail.txt"
    if os.path.exists(save_filepath_1):
        os.remove(save_filepath_1)
    if os.path.exists(save_filepath_2):
        os.remove(save_filepath_2)
    if os.path.exists(save_filepath_3):
        os.remove(save_filepath_3)
    if os.path.exists(save_filepath_4):
        os.remove(save_filepath_4)

    if not isinstance(excel_data, list):
        print("出错了:", excel_data)

    while start_flag < len(excel_data):
        row = excel_data[start_flag]
        start_flag += 1
        print("正在处理第", start_flag, "条数据")
        #print(row)
        division_code = str(row[2])
        product_code_lst_str = str(row[3])
        wms_id_1 = int(row[4]) if row[6] else 0
        wms_id_2 = int(row[6]) if row[6] else 0
        wms_id_3 = int(row[8]) if row[8] else 0
        wms_id_4 = int(row[10]) if row[10] else 0
        wms_id_lst = []
        if wms_id_1:
            wms_id_lst.append(str(wms_id_1))
        if wms_id_2:
            wms_id_lst.append(str(wms_id_2))
        if wms_id_3:
            wms_id_lst.append(str(wms_id_3))
        if wms_id_4:
            wms_id_lst.append(str(wms_id_4))
        wms_id_lst_str = str(wms_id_lst[0]) if len(wms_id_lst) == 1 else ",".join(wms_id_lst)

        shop_code = str(row[14])

        config_sql_lst = []
        priority_detail_sql_lst = []
        config_sku_sql_lst = []
        priority_sql_lst = []

        product_code_lst = product_code_lst_str.split("、")
        product_code_lst_trans = ",".join([f"'{n}'" for n in product_code_lst])
        skuref_id_lst_res = send_request_yaernings(product_code_lst_trans)
        skuref_id_lst_divide = tools.divide(skuref_id_lst_res, 500)
        for skuref_id_lst in skuref_id_lst_divide:
            config_sql = "INSERT INTO `vm_warehouse`.`division_compartment_config` (`id`, `division_code`, `shop_code`, `warehouse_priority_config_id`, `status`, `created_time`, `created_by`, `updated_time`, `updated_by`) VALUES (" \
                         f"{config_id}, '{division_code}', '{shop_code}', {priority_id}, {create_status}, {create_time}, 'sys', NULL, NULL);"
            config_sql_lst.append(config_sql)

            # print(config_sql)
            for sku_id in skuref_id_lst:
                if sku_id:
                    config_sku_sql = "INSERT INTO `vm_warehouse`.`division_compartment_config_sku` (`id`, `division_compartment_config_id`, `sku_id`, `status`, `created_time`, `created_by`, `updated_time`, `updated_by`) VALUES (" \
                                     f"{config_sku_id}, {config_id}, {sku_id},{create_status}, {create_time}, 'sys', NULL, NULL);"
                    config_sku_id += 1
                    config_sku_sql_lst.append(config_sku_sql)

            priority_sql = "INSERT INTO `vm_warehouse`.`warehouse_priority_config` (`id`, `warehouse_id_list_str`, `status`, `created_time`, `created_by`, `updated_time`, `updated_by`) VALUES (" \
                           f"{priority_id}, '{wms_id_lst_str}', {create_status}, {create_time}, 'sys', NULL, NULL);"
            priority_sql_lst.append(priority_sql)

            if wms_id_1:
                priority_detail_sql_1 = "INSERT INTO `vm_warehouse`.`warehouse_priority_config_detail` (`id`, `warehouse_priority_config_id`, `warehouse_id`, `priority`, `status`, `created_time`, `created_by`, `updated_time`, `updated_by`) VALUES (" \
                                        f"{priority_detail_id}, {priority_id}, {wms_id_1}, 1, {create_status}, {create_time}, 'sys', NULL, NULL);"
                priority_detail_sql_lst.append(priority_detail_sql_1)
                priority_detail_id += 1
            if wms_id_2:
                priority_detail_sql_2 = "INSERT INTO `vm_warehouse`.`warehouse_priority_config_detail` (`id`, `warehouse_priority_config_id`, `warehouse_id`, `priority`, `status`, `created_time`, `created_by`, `updated_time`, `updated_by`) VALUES (" \
                                        f"{priority_detail_id}, {priority_id}, {wms_id_2}, 2, {create_status}, {create_time}, 'sys', NULL, NULL);"
                priority_detail_sql_lst.append(priority_detail_sql_2)
                priority_detail_id += 1
            if wms_id_3:
                priority_detail_sql_3 = "INSERT INTO `vm_warehouse`.`warehouse_priority_config_detail` (`id`, `warehouse_priority_config_id`, `warehouse_id`, `priority`, `status`, `created_time`, `created_by`, `updated_time`, `updated_by`) VALUES (" \
                                        f"{priority_detail_id}, {priority_id}, {wms_id_3}, 3, {create_status}, {create_time}, 'sys', NULL, NULL);"
                priority_detail_sql_lst.append(priority_detail_sql_3)
                priority_detail_id += 1
            if wms_id_4:
                priority_detail_sql_4 = "INSERT INTO `vm_warehouse`.`warehouse_priority_config_detail` (`id`, `warehouse_priority_config_id`, `warehouse_id`, `priority`, `status`, `created_time`, `created_by`, `updated_time`, `updated_by`) VALUES (" \
                                        f"{priority_detail_id}, {priority_id}, {wms_id_4}, 4, {create_status}, {create_time}, 'sys', NULL, NULL);"
                priority_detail_sql_lst.append(priority_detail_sql_4)
                priority_detail_id += 1
            priority_id += 1
            config_id += 1

        with open(save_filepath_1, "a+", encoding="utf-8") as t1, open(save_filepath_2, "a+",
                                                                       encoding="utf-8") as t2, \
                open(save_filepath_3, "a+", encoding="utf-8") as t3, open(save_filepath_4, "a+",
                                                                          encoding="utf-8") as t4:
            for sql1 in config_sql_lst:
                t1.write(sql1 + "\n")
            for sql2 in priority_sql_lst:
                t3.write(sql2 + "\n")
            for i in config_sku_sql_lst:
                t2.write(i + "\n")
            for j in priority_detail_sql_lst:
                t4.write(j + "\n")



def send_request_yaernings(key_word):
    sku_id_lst = list()
    url = "https://yaernings-prod.viomi.com.cn/api/v2/query"
    heads = {
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTkzMzMyNDEsIm5hbWUiOiJwZW5na2FpbGlhbmciLCJyb2xlIjoiZ3Vlc3QifQ.C3Bc54RrhuVSjVw6qIKYVLGBAt0DnPlMITp11rxvXA8',
        'content-type': 'application/json;charset=UTF-8',
        'cookie': 'KLBRSID=3d2bbd55064a7c02424984013b049571|1619318864|1619318839',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    sql = f"select distinct sku_id from warehouse_skuinfo_ref where barcode in ({key_word})"
    # print(sql)
    data = {"basename": "vm_warehouse",
            "source": "prod_express_read_134",
            "sql": sql}
    urllib3.disable_warnings()
    res = requests.post(url=url, headers=heads, data=json.dumps(data), verify=False)
    yaernings_json = res.text  # 返回的json
    yaernings_dict = json.loads(yaernings_json)
    yaernings_data = yaernings_dict['data']
    if yaernings_data:
        for db_sku_id in yaernings_data:
            if db_sku_id:
                sku_id_lst.append(db_sku_id['sku_id'])
    return sku_id_lst


if __name__ == '__main__':
    deal_data()

import tool.excel as excel


def a():
    filename = "库存负数订单记录-20210425.xls"
    excel_obj = excel.Excel(filename=filename)
    excel_data = excel_obj.data
    index = 1  # 从第二行开始读
    oms_order_lst = set()
    while index < len(excel_data):
        row = excel_data[index]
        index += 1
        print("正在处理第", index, "行")
        print(row)
        deal_flag = str(row[6])
        oms_code = str(row[3])
        if deal_flag != '暂不处理':
            oms_order_lst.add(oms_code)
    lst_1 = [f"'{o}'" for o in oms_order_lst]
    join = ','.join(list(lst_1))
    print(join)


if __name__ == '__main__':
    a()

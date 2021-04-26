import xlwings as xw


class Excel:
    def __init__(self, filename, flag=""):
        self.filepath = "C:\\Users\\Administrator\\Desktop\\"
        self.filename = filename
        self.row = 0
        self.column = 0
        self.data = self.__get_data_lst(flag=flag)

    def __get_data_lst(self, flag=""):
        app = None
        wb = None
        data_lst = []
        try:
            app = xw.App(visible=True, add_book=False)
            app.display_alerts = False  # 关闭一些提示信息，可以加快运行速度。 默认为 True。
            app.screen_updating = False  # 更新显示工作表的内容。默认为 True。关闭它也可以提升运行速度。
            wb = app.books.open(self.filepath + self.filename)
            sheet = wb.sheets[0]
            shape = sheet.range(1, 1).expand().shape
            self.row = shape[0]
            self.column = shape[1]
            if flag:
                return sheet.range(f"{flag}1:{flag}{self.row}").value
            # 用切片
            for row in range(0, self.row):
                data_lst.append(sheet[row, :self.column].value)
            return data_lst
        except Exception as e:
            return e
        finally:
            if wb:
                wb.close()
            if app:
                app.quit()


if __name__ == '__main__':
    excel = Excel(filename="新增店铺维度分仓规则导入模板(3).xlsx")
    print(excel.row)
    print(excel.column)
    data = excel.data
    if isinstance(data, list):
        for i in data:
            print(i)
    else:
        print(data)

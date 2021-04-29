import random
import time

from tool import baidu as bd
from tool import youdao as yd


def translation(filename):
    read_path = f'C:\\Users\\Administrator\\Desktop\\{filename}.md'
    write_path = f'C:\\Users\\Administrator\\Desktop\\{filename}_翻译.md'

    skip_lst = ["Java\n", "Kotlin\n"]
    with open(read_path, 'r', encoding='utf-8') as read_file, open(write_path, 'w', encoding='utf-8') as write_file:
        lines = read_file.readlines()
        flag = 1
        code_flag = 0
        for document_line in lines:
            print('文档总共', len(lines), '行,正在处理第', flag, '行')
            flag += 1

            if document_line in skip_lst:
                continue

            document_line = link(document_line)
            # 代码行
            if '```' in document_line:
                code_flag += 1

            if (len(document_line) > 0) and (code_flag % 2 == 0):
                document_line = conversion(do_trans(document_line))
            if '\n' not in document_line:
                document_line = document_line + '\n'

            write_file.write(document_line)
            if flag == 2000:
                break


def do_trans(row):
    spec_word_lst = ['#', '-']
    row_0 = row[0]
    if row_0.isalpha():
        row = choose_tool(row)
    if row_0 in spec_word_lst:
        row.index(' ')
        row = choose_tool(row[row.index(' ') + 1:])
    return row


def choose_tool(keywords):
    randint = random.randint(1, 100)
    if randint > 49:
        keywords = baidu(keywords)
    else:
        keywords = youdao(keywords)
    return keywords


def link(keyword):
    if isinstance(keyword, str) and "http" in keyword and "[" in keyword:

        http_index = keyword.find("http")
        if '(' == keyword[http_index - 1]:
            last_index = keyword.find(")", http_index)
            keyword = keyword[0:http_index - 1] + keyword[last_index + 1:]

            if "http" not in keyword and "[" not in keyword:
                return keyword.replace("[", "").replace("]", "")
            else:
                return link(keyword)
    else:
        return keyword


def table(keyword):
    if isinstance(keyword, str) and keyword.count("|") == 3:
        pass


def youdao(keyword):
    time.sleep(random.randint(10, 15))
    return yd.Youdao(keyword).get_result()


def baidu(keyword):
    time.sleep(random.randint(10, 15))
    return bd.trans(keyword)


def conversion(keyword):
    keyword = keyword.replace("' ", "`")
    keyword = keyword.replace(" '", "`")
    keyword = keyword.replace("注释", "注解")
    keyword = keyword.replace("“", "`")
    keyword = keyword.replace("”", "`")
    keyword = keyword.replace("（", "(")
    keyword = keyword.replace("）", ")")
    return keyword


if __name__ == '__main__':
    translation("spring_2")

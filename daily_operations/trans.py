import random
import time

from tool import youdao


def document_trans():
    read_path = r'C:\Users\Administrator\Desktop\spring_2.md'
    write_path = r'C:\Users\Administrator\Desktop\spring_ch_2.md'
    spec_word_lst = ['#', '-']
    read_flag = 1
    read_flag_line = 1

    with open(read_path, 'r', encoding='utf-8') as read_file, open(write_path, 'w', encoding='utf-8') as write_file:
        lines = read_file.readlines()
        flag = 1
        code_flag = 0
        for document_line in lines:
            print('文档总共', len(lines), '行,正在处理第', flag, '行')
            read_flag += 1
            flag += 1
            if read_flag <= read_flag_line:
                continue
            # 代码行
            if '```' in document_line:
                code_flag += 1

            if (len(document_line) > 0) and (code_flag % 2 == 0):
                document_line_0 = document_line[0]
                if document_line_0.isalpha():
                    #  document_line = baidu.trans(document_line)
                    document_line = youdao.Youdao(document_line).get_result()
                    time.sleep(random.randint(10, 15))
                if document_line_0 in spec_word_lst:
                    document_line.index(' ')
                    # document_line = document_line[0:document_line.index(' ') + 1] + baidu.trans(
                    #   document_line[document_line.index(' ') + 1:])
                    time.sleep(random.randint(10, 15))
                    document_line = document_line[0:document_line.index(' ') + 1] + youdao.Youdao(
                        document_line[document_line.index(' ') + 1:]).get_result()
                if '\n' not in document_line:
                    document_line = document_line + '\n'

            write_file.write(document_line)
            if flag == 1000:
                break


if __name__ == '__main__':
    document_trans()

import os
import time

import matplotlib.image as mpimg
import requests


def read_file(name):
    filepath = "C:\\Users\\murloc\\Desktop\\软件工程学习笔记\\"
    filename = f"{name}.md"
    filename_wt = f"{name}_1.md"
    wt_path = f"{filepath}{name}_img\\"
    if not os.path.exists(wt_path):
        os.makedirs(wt_path)

    with open(filepath + filename, "r", encoding="utf-8") as r, open(filepath + filename_wt, "w",
                                                                     encoding="utf-8") as w:
        lines = r.readlines()
        for line in lines:
            if "![" in line and "](" in line:
                time_now = str(time.time_ns())[0:-2]
                img_path = line[line.index("(") + 1:line.index(")")]
                if "http" in img_path:
                    header = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}  # 设置http header，视情况加需要的条目，这里的token是用来鉴权的一种方式
                    r = requests.get(img_path, headers=header, stream=True)
                    if r.status_code == 200:
                        open(f"{wt_path}{time_now}.png", 'wb').write(r.content)  # 将内容写入图片
                    else:
                        print(img_path)
                else:
                    image = mpimg.imread(img_path)
                    mpimg.imsave(f"{wt_path}{time_now}.png", image)
                line = f"![]({wt_path}{time_now}.png)\n"
            w.write(line)


if __name__ == '__main__':
    read_file("设计模式")

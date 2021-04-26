import hashlib
import random
import time

import requests

"""
向有道翻译发送data，得到翻译结果
"""


class Youdao:
    def __init__(self, msg):
        self.url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.msg = msg
        self.ts = self.get_ts()
        self.salt = self.get_salt()

    def get_ts(self):
        # 根据当前时间戳获取ts参数
        s = int(time.time() * 1000)
        return str(s)

    def get_salt(self):
        # 根据当前时间戳获取salt参数
        s = int(time.time() * 1000) + random.randint(0, 10)
        return str(s)

    def get_sign(self):
        # 使用md5函数和其他参数，得到sign参数
        words = "fanyideskweb" + self.msg + self.salt + "Tbh5E8=q6U3EXe+&L[4c@"

        # 对words进行md5加密
        hashlib.md5()
        m = hashlib.md5()
        m.update(words.encode('utf-8'))
        return m.hexdigest()

    def get_result(self):
        form_data = {
            'i': self.msg,
            'from': 'en',
            'to': 'zh-CHS',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': self.salt,
            'sign': self.get_sign(),
            'lts': self.ts,
            'bv': 'eff2e73dc527a143fb4d0a678a264090',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }
        headers = {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-532515957@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=782923961.7887233; _ntes_nnid=4f9d11e8563bea5e350424763c6f03e0,1615603693257; _ga=GA1.2.1123212858.1615881635; UM_distinctid=178d312ac248a7-0a32dd03559d2f-c3f3568-1fa400-178d312ac25b15; JSESSIONID=aaau4eIqlwsMF-baHZSJx; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1618911734282',
            'Referer': 'https://fanyi.youdao.com/?keyfrom=dict2.index',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OSX10_14_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        try:
            time.sleep(random.randint(10, 20))
            response = requests.post(self.url, data=form_data, headers=headers)
            translate_results = response.json()
            trans_result_str = ''
            # 找到翻译结果
            if 'translateResult' in translate_results:
                for translate_result in translate_results['translateResult'][0]:
                    trans_result_str += translate_result['tgt']
                return trans_result_str
            else:
                return self.msg
        except Exception as e:
            print("出错了,", e)
            return self.msg


if __name__ == "__main__":
    keywords = 'Spring makes it easy to create Java enterprise applications.It provides everything you need to embrace the ' \
               'Java language in an enterprise environment, with support for Groovy and Kotlin as alternative languages on the JVM, ' \
               'and with the flexibility to create many kinds of architectures depending on an application’s needs. ' \
               'As of Spring Framework 5.1, Spring requires JDK 8+ (Java SE 8+) and provides out-of-the-box support for JDK 11 LTS.' \
               ' Java SE 8 update 60 is suggested as the minimum patch release for Java 8, ' \
               'but it is generally recommended to use a recent patch release.'
    en = Youdao(keywords).get_result()
    print(en)

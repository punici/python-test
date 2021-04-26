import random
import re
import time

import js2py
import requests

# 浏览器代理
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    "referer": "https://fanyi.baidu.com/?aldtype=16047",
    "cookie": "BAIDUID=95EB2FC558ADC7FEAC8F7BAA2437876A:FG=1; PSTM=1618382672; BIDUPSID=C1003DC4AFD6440BC4CBC6D2FF984AEA; __yjs_duid=1_13d7ca5bc7a72217e2e09434751309b91618382687118; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BAIDUID_BFESS=4ABA7399E5AB44BB4D2B317333C243F0:FG=1; BDRCVFR[n9IS1zhFc9f]=mk3SLVN4HKm; delPer=0; PSINO=7; H_PS_PSSID=; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BCLID=9047858529143521072; BDSFRCVID=dHIOJexroG38EYQefle7hbAFquweG7bTDYLEOwXPsp3LGJLVJeC6EG0Pts1-dEu-EHtdogKK3gOTH4DF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR3aQ5rtKRTffjrnhPF3WM_zXP6-hnjy3bAOKxTt5RQSjljd-xQPKJLWbttf5q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvDP-g3-AJ0U5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrMb-7AWMT-MTryKK8y3xTGeJQ1bjJs-x_zKqofKx-fKHnRhlRNB-3iV-OxDUvnyxAZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDUJ9LUkJ3gcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLK-oj-DD4DT_53e; BCLID_BFESS=9047858529143521072; BDSFRCVID_BFESS=dHIOJexroG38EYQefle7hbAFquweG7bTDYLEOwXPsp3LGJLVJeC6EG0Pts1-dEu-EHtdogKK3gOTH4DF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tR3aQ5rtKRTffjrnhPF3WM_zXP6-hnjy3bAOKxTt5RQSjljd-xQPKJLWbttf5q3RymJJ2-39LPO2hpRjyxv4y4Ldj4oxJpOJ-bCL0p5aHl51fbbvbURvDP-g3-AJ0U5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIEoCvt-5rDHJTg5DTjhPrMb-7AWMT-MTryKK8y3xTGeJQ1bjJs-x_zKqofKx-fKHnRhlRNB-3iV-OxDUvnyxAZyxomtfQxtNRJQKDE5p5hKq5S5-OobUPUDUJ9LUkJ3gcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLK-oj-DD4DT_53e; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1618640748,1618640813; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1618640813; __yjs_st=2_OGZiNWE1MjY4NDM2MzYyOGIxOGYwYjQ5OGNiNmY4ZTgxNjEwZTE1MmMzOTgxMzkwNmFlYmEyNjBmODUxMTQ2NWI2M2EwNzkyODZhYTNmMTQ1Mjg3MzAxN2I5YTAwNzlmMmY1YzM3YzAwNDI1ZWYwZmIzNGQwNGE1NzFlYzdjNGY4MjQzMmIzZjg2ZjNiNTcxMWNiM2I0Zjg3MjZmNTY2Y2ZmZTEyYjg0OWFlNjExOTk5Yjk3MDgzNDhkZTkxOTc1NGI4ZDM3ZjQ4YWU0N2ExYWVmMjc2ZmE3OWY3ZDkwZThiZjRlZGQxODExNzI0ZDEwYTY1NzlhNzFmNDUxZjRlNDhmZDU1ZDI0ZjgyYTNkZjc0Y2ExYzliMzcxM2RiMjdhXzdfZjJhNWQ3MmY=; ab_sr=1.0.0_OTA5YmU1NWFkZDhhNWI1NWEzMTJjY2NiMDk3Zjc1ZGQ4YzU0OGU1NmQ5MDAxODEzNGE4MjMzNjBmZTllMDI4NjVjNzI0ZWJiNGNiY2E2MmJkMWZhNmIwMWMzOWY2OTYx; BA_HECTOR=2la4240g8l048481m81g7l2qr0q"
}


# 用来获取sign
def judge_sign(word):
    # 加载js里的算法 计算出sign
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"}
    session.headers = headers
    response = session.get("http://fanyi.baidu.com/")
    gtk = re.findall(";window.gtk = ('.*?');", response.content.decode())[0]

    context = js2py.EvalJs()
    js = r'''
    function a(r) {
            if (Array.isArray(r)) {
                for (var o = 0, t = Array(r.length); o < r.length; o++)
                    t[o] = r[o];
                return t
            }
            return Array.from(r)
        }
        function n(r, o) {
            for (var t = 0; t < o.length - 2; t += 3) {
                var a = o.charAt(t + 2);
                a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
                    a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
                    r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
            }
            return r
        }
        function e(r) {
            var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
            if (null === o) {
                var t = r.length;
                t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
            } else {
                for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                    "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                    C !== h - 1 && f.push(o[C]);
                var g = f.length;
                g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
            }
            var u = void 0
                , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
            u = 'null !== i ? i : (i = window[l] || "") || ""';
            for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
                var A = r.charCodeAt(v);
                128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
                    S[c++] = A >> 18 | 240,
                    S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
                    S[c++] = A >> 6 & 63 | 128),
                    S[c++] = 63 & A | 128)
            }
            for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
                p += S[b],
                    p = n(p, F);
            return p = n(p, D),
                p ^= s,
            0 > p && (p = (2147483647 & p) + 2147483648),
                p %= 1e6,
            p.toString() + "." + (p ^ m)
        }
    '''
    # js中添加一行gtk
    js = js.replace('\'null !== i ? i : (i = window[l] || "") || ""\'', gtk)
    # 执行js
    context.execute(js)
    # 调用函数得到sign
    return context.e(word)


# 传入form，to 和 待翻译的字符串 和 sign
def trans(word):
    # 获取 sign
    sign = judge_sign(word)
    # post请求url需要的data数据
    data = {
        "from": 'en',
        "to": 'zh',
        "query": word,
        "simple_means_flag": "3",
        "sign": sign,
        # 把token修改为自己的 在此没进行赋值
        "token": "b0e3e0db66023513c48790d27ce50f32",
        "transtype": "translang"
    }
    time.sleep(random.randint(1, 4))
    # 请求url
    translates = requests.post(url="https://fanyi.baidu.com/v2transapi", data=data,
                               headers=header).json()
    # 提取需要的内容
    if 'trans_result' in translates.keys():
        return translates["trans_result"]["data"][0]["dst"]
    else:
        return word


if __name__ == '__main__':
    # 待翻译的内容
    word = "This chapter covers the Spring Framework implementation of the Inversion of Control (IoC) principle. IoC is also known as dependency injection (DI). It is a process whereby objects define their dependencies (that is, the other objects they work with) only through constructor arguments, arguments to a factory method, or properties that are set on the object instance after it is constructed or returned from a factory method. The container then injects those dependencies when it creates the bean. This process is fundamentally the inverse (hence the name, Inversion of Control) of the bean itself controlling the instantiation or location of its dependencies by using direct construction of classes or a mechanism such as the Service Locator pattern."

    # 传入参数构造data
    translate = trans(word)

    print(translate)

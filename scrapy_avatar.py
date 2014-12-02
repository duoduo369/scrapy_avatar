#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import hashlib
import urllib
import sys
import os
import random
from functools import partial


AGENTS = [
    "Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 GTB5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 ( .NET CLR 3.5.30729; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110622 Firefox/6.0a2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
]


QQ_MD5_ESCAPE = ['11567101378fc08988b38b8f0acb1f74', '9d11f9fcc1888a4be8d610f8f4bba224']


LOG_FILES = 'scrapy_{}.log'
EMAIL_LIST = 'email_list_{}.json'
AVATAR_PATH = 'avatar/{}{}'


LOG_LEVEL_EXISTS = 'EXISTS'
LOG_LEVEL_NOTSET_OR_ERROR = 'NOTSET_OR_ERROR'
LOG_LEVEL_TYPE_ERROR = 'TYPE_ERROR'
LOG_LEVEL_ERROR = 'ERROR'
LOG_LEVEL_FAIL = 'FAIL'
LOG_LEVEL_SUCCESS = 'SUCCESS'
LOG_LEVEL_IGNORE = 'IGNORE'


def get_gravatar_url(email, default_avatar=None, use_404=False, size=100):
    data = {}
    if default_avatar and default_avatar.startswith('http'):
        data['d'] = default_avatar
    if use_404:
        data['d'] = '404'
    data['s'] = str(size)
    gravatar_url = "http://secure.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode(data)
    return gravatar_url


def get_random_headers():
    agent = random.choice(AGENTS)
    headers = {'User-Agent': agent}
    return headers


def check_logfile(part):
    last_scrapy_line = 1
    if os.path.exists('scrapy_{}.log'.format(part)):
        with open('scrapy_{}.log'.format(part)) as log_read:
            for line in log_read:
                last_scrapy_line = max(last_scrapy_line, int(line.split()[0]))
    print last_scrapy_line
    return last_scrapy_line + 1


def get_log_message(log_format='{index} {level} {email} {msg}', index=None, level=None, email=None, msg=None):
    return log_format.format(index=index, level=level, email=email, msg=msg)


SUCCESS_LOG = partial(get_log_message, level=LOG_LEVEL_SUCCESS, msg='scrapyed success')
EXIST_LOG = partial(get_log_message, level=LOG_LEVEL_EXISTS, msg='scrapyed already')
FAIL_LOG = partial(get_log_message, level=LOG_LEVEL_FAIL, msg='scrapyed failed')
NOT_QQ_LOG = partial(get_log_message, level=LOG_LEVEL_TYPE_ERROR, msg='not qq email')
IGNORE_LOG = partial(get_log_message, level=LOG_LEVEL_TYPE_ERROR, msg='ignore email')
EMPTY_SIZE_LOG = partial(get_log_message, level=LOG_LEVEL_ERROR, msg='empty avatar')
UNEXCEPT_ERROR_LOG = partial(get_log_message, level=LOG_LEVEL_ERROR, msg='unexcept error')


def write_log(log, msg):
    log.write(msg)
    log.write('\n')
    log.flush()


def save_avatar_file(filename, content):
    with open(filename, 'wb') as avatar_file:
        avatar_file.write(content)


def scrapy_context(part, suffix='.jpg', rescrapy=False, hook=None):
    last_scrapy_line = check_logfile(part)
    index = last_scrapy_line
    with open(LOG_FILES.format(part), 'a') as log:
        with open(EMAIL_LIST.format(part)) as list_file:
            for linenum, email in enumerate(list_file):
                if linenum < last_scrapy_line:
                    continue
                email = email.strip()
                if not rescrapy:
                    if os.path.exists(AVATAR_PATH.format(email, suffix)):
                        print EXIST_LOG(index=index, email=email)
                        index += 1
                        continue
                if not hook:
                    raise NotImplementedError()
                try:
                    hook(part, suffix=suffix, rescrapy=rescrapy, log=log, index=index, email=email)
                except Exception as ex:
                    print UNEXCEPT_ERROR_LOG(index=index, email=email)
                    write_log(log, UNEXCEPT_ERROR_LOG(index=index, email=email))
                    raise ex
                index += 1


def scrapy_qq_hook(part, suffix='.jpg', rescrapy=False, log=None, index=None, email=None):
    if 'qq.com' not in email.lower():
        print NOT_QQ_LOG(index=index, email=email)
        write_log(log, NOT_QQ_LOG(index=index, email=email))
        return

    url = 'http://q4.qlogo.cn/g?b=qq&nk={}&s=4'.format(email)
    response = requests.get(url, timeout=10, headers=get_random_headers())
    if response.status_code == 200:
        # 判断用户是否有大图标, 如果没有则请求小图标
        if hashlib.md5(response.content) in QQ_MD5_ESCAPE:
            url = 'http://q4.qlogo.cn/g?b=qq&nk={}&s=2'.format(email)
            response = requests.get(url, timeout=10, headers=get_random_headers())
            if response.status_code == 200:
                if not len(response.content):
                    print EMPTY_SIZE_LOG(index=index, email=email)
                    write_log(log, EMPTY_SIZE_LOG(index=index, email=email))
    # 这里再次判断是因为上一个200判断做了一次图片check
    if response.status_code == 200:
        save_avatar_file(AVATAR_PATH.format(email, suffix), response.content)
        print SUCCESS_LOG(index=index, email=email)
        write_log(log, SUCCESS_LOG(index=index, email=email))
    else:
        print FAIL_LOG(index=index, email=email)
        write_log(log, FAIL_LOG(index=index, email=email))


def scrapy_gravatar_hook(part, suffix='.jpg', rescrapy=False, ignore_email_suffix=None, log=None, index=None, email=None):
    if ignore_email_suffix and ignore_email_suffix in email.lower():
        print IGNORE_LOG(index=index, email=email)
        write_log(log, IGNORE_LOG(index=index, email=email))
        return

    response = requests.get(get_gravatar_url(email, use_404=True), timeout=10, headers=get_random_headers())
    if response.status_code == 200:
        save_avatar_file(AVATAR_PATH.format(email, suffix), response.content)
        print SUCCESS_LOG(index=index, email=email)
        write_log(log, SUCCESS_LOG(index=index, email=email))
    else:
        print FAIL_LOG(index=index, email=email)
        write_log(log, FAIL_LOG(index=index, email=email))
        return


scrapy_gravatar = partial(scrapy_context, hook=scrapy_gravatar_hook)
scrapy_qq = partial(scrapy_context, hook=scrapy_qq_hook)


FUNC_MAPPER = {
    'qq': scrapy_qq,
    'gravatar': scrapy_gravatar,
}

if __name__ == '__main__':
    scrapy_type = sys.argv[1]
    part = sys.argv[2]
    if scrapy_type not in FUNC_MAPPER:
        print 'type should in [qq | gravatar]'
        exit(0)
    FUNC_MAPPER[scrapy_type](part)

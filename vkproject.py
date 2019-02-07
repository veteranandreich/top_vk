import requests
import lxml.html
import vk_requests
from config import vk_config
import datetime
import time
import json
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    return response.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    answer = soup.findAll('a', class_="top_hashtags_item al_tab")
    return [i.text for i in answer]


def log_in():
    login = vk_config['login']
    password = vk_config['password']
    url = 'https://vk.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-ru,ru;q=0.8,en-us;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'DNT': '1'
    }
    session = requests.session()
    data = session.get(url, headers=headers)
    page = lxml.html.fromstring(data.content)
    form = page.forms[0]
    form.fields['email'] = login
    form.fields['pass'] = password
    session.post(form.action, data=form.form_values())
    return session


def get_last_5_min(tag, cur_time):
    five_m_dict = [{}]
    start_time = cur_time
    end_time = cur_time - 60
    for shift in range(0, 300, 60):
        start_time -= 60
        end_time -= 60
        t1 = datetime.datetime.fromtimestamp(start_time).time()
        t = "{:d}:{:02d}".format(t1.hour, t1.minute)
        five_m_dict[0][t] = {}
        flag = False
        s = 0
        ids = []
        for offset in range(0, 1000, 200):
            time.sleep(0.333333334)
            a = api.newsfeed.search(q=tag, count=200, offset=offset, v=5.12)['items']
            for news in a:
                if end_time <= news['date'] <= start_time and news['id'] not in ids:
                    s += 1
                    ids.append(id)
                five_m_dict[0][t][tag] = s
                if news['date'] <= end_time:
                    flag = True
                    s = 0
                    break
            if flag:
                break
    return json.dumps(five_m_dict, indent=4, ensure_ascii=False)


def get_top_5():
    session = log_in()
    response = session.get('https://vk.com/feed?section=search')
    tags = parse(response.text)
    return tags


print(get_top_5())
api = vk_requests.create_api(app_id=6751640, login=vk_config['login'], password=vk_config['password'])
cur_time = int(time.time())
print(get_last_5_min('#играемвклевер', cur_time))

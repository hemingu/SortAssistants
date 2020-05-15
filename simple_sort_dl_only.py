from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from PIL import Image
import urllib
import datetime
from operator import attrgetter


class assistant:
    def __init__(self, name, age, height, bust, waist, hip, cup, pic_path, is_silver, is_gold, next_work_datetime):
        if not (isinstance(name, str) and isinstance(age, int) and isinstance(height, int) and isinstance(bust, int) and
                isinstance(waist, int) and isinstance(hip, int) and isinstance(cup, str) and (isinstance(pic_path, str) or pic_path is None)):
            raise TypeError

        result = re.fullmatch('[A-Z]', cup)
        if result is None:
            raise ValueError

        self.name = name
        self.age = age
        self.height = height
        self.bust = bust
        self.waist = waist
        self.hip = hip
        self.cup = cup
        self.pic_path = pic_path
        self.is_silver = is_silver
        self.is_gold = is_gold
        self.next_work_datetime = next_work_datetime

    def output_info(self):
        # print(self.name, self.age, self.height, self.bust, self.waist, self.hip, self.cup, self.next_work_datetime, sep='\t')
        print('{:　<5}{:>3}  {:>4}  {:>3}  {:>3}  {:>3}  {:2} {}'.format(self.name, self.age, self.height, self.bust, self.waist, self.hip, self.cup, self.next_work_datetime))

def selection(an_assistant):
    if not isinstance(an_assistant, assistant):
        raise TypeError
    # if an_assistant.age <= 25 and an_assistant.cup >= 'H':
    if an_assistant.cup >= 'G':
        return True
    return False


url = 'https://www.oideyasugstyle.com/girls/'
html = requests.get(url).text

soup = BeautifulSoup(html, 'html.parser')

assistants_html = soup.select('.girlCell')

assistants = []


for assistant_html in assistants_html:
    info_str = assistant_html.text
    result = re.search('([\u3041-\u3096\u30A1-\u30FA]+).*\((\d+)\)', info_str)
    name, age = result.groups()
    age = int(age)
    result = re.search('T(\d+).*B(\d+).*\(([A-Z])\).*W(\d+).*H(\d+)', info_str)
    height, bust, cup, waist, hip = result.groups()
    height, bust, waist, hip = map(int, (height, bust, waist, hip))

    img_path = None
    # imgPIL = Image.open(img_path)
    # imgPIL.show()
    icon_html = assistant_html.contents[1].contents[5].contents
    is_silver = False
    is_gold = False
    if len(icon_html) == 1:
        pass
    elif len(icon_html) == 5:
        is_silver = True
        is_gold = True
    elif icon_html[1].contents[0].attrs['alt'] == 'ゴールド':
        is_gold = True
    elif icon_html[1].contents[0].attrs['alt'] == 'シルバー':
        is_silver = True
    else:
        pass

    # next_work_date_str = 
    result = re.search('次回：未定', info_str)
    if result is not None:
        next_work_datetime = None
    result = re.search('次回：(\d+)/(\d+)', info_str)
    if result is not None:
        month, day = map(int, result.groups())
        time_now = datetime.datetime.now()
        next_work_datetime = datetime.datetime(time_now.year, month, day)
    result = re.search('本日.*｜.*(\d+):(\d+)-(\d+):(\d+)', info_str)
    if result is not None:
        start_hour, start_minute, end_hour, end_time = map(int, result.groups())
        time_now = datetime.datetime.now()
        next_work_datetime = datetime.datetime(time_now.year, time_now.month, time_now.day, start_hour, start_minute)
    the_assistant = assistant(name, age, height, bust, waist, hip, cup, img_path, is_silver, is_gold, next_work_datetime)
    if selection(the_assistant):
        assistants.append(the_assistant)



assistants.sort(key=attrgetter('cup'), reverse=True)

print('Name       {:>3}  {:^4}  {:^3}  {:^3}  {:^3}  {:^3} {}'.format('Age', 'T', 'B', 'W', 'H', 'Cup', 'Next'))
for the_assistant in assistants:
    the_assistant.output_info()
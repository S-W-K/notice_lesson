# -*- coding: utf-8 -*-
# @Author: S_W_K

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree
import requests
from requests.cookies import RequestsCookieJar
import datetime
import keyring
import yagmail


class NoticeYou:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def register(self, student_id, password):
        keyring.set_password('IbarakiUniv', student_id, password)

    def login(self, id_, password_):

        request_url = 'https://idc.ibaraki.ac.jp/portal/Login.aspx'
        id_ = id_
        password_ = password_

        self.driver.get(request_url)
        login_button = self.driver.find_element_by_xpath(
            '//*[@id="ctl22_btnShibLogin"]')
        login_button.click()
        id_input = self.driver.find_element_by_xpath(
            '//*[@id="userNameInput"]')
        password_input = self.driver.find_element_by_xpath(
            '//*[@id="passwordInput"]')
        id_input.clear()
        password_input.clear()
        id_input.send_keys(id_)
        password_input.send_keys(password_)
        login_button = self.driver.find_element_by_xpath(
            '//*[@id="submitButton"]')
        login_button.click()

        cookies = self.driver.get_cookies()
        jar = RequestsCookieJar()
        for cookie in cookies:
            jar.set(cookie['name'], cookie['value'])
        page_source = self.driver.page_source

        return page_source, jar

    def if_tomorrow(self, date_str, days):
        weekday_dic = {}
        weekday_jpn = ['月', '火', '水', '木', '金', '土', '日']
        weekday_en = [i for i in range(1, 8)]
        for en, jpn in zip(weekday_en, weekday_jpn):
            weekday_dic[en] = jpn

        tomorror_date = datetime.datetime.today()+datetime.timedelta(days=days)
        tomorror_weekday = tomorror_date.isoweekday()
        tomorror_date = tomorror_date.strftime('%Y/%m/%d')
        tomorror_date += ('(%s)' % weekday_dic[tomorror_weekday])

        if tomorror_date == date_str:
            return True
        else:
            return False

    def get_subject_schedule(self, page_source):
        html = etree.HTML(page_source)
        subjects = {}
        tables = html.xpath(
            '//*[@id="ctl00_phContents_ucScheduleWeek_gv"]//tr//td//table')
        for table in tables:
            subject_info = table.find('.//tr[2]/td/a')
            subject_name = subject_info.text
            subject_url = subject_info.items()
            subject_url = 'https://idc.ibaraki.ac.jp'+subject_url[2][1]
            subjects[subject_name] = subject_url
        return subjects

    def has_lesson(self, url, cookies, days):
        response = requests.get(url, cookies=cookies)
        schedual = response.text
        html = etree.HTML(schedual)
        trs = html.xpath('//table[@id="ctl00_phContents_ucLctList_gv"]/tr')
        for tr in trs[1:]:
            date = tr.find('.//td[2]')
            if self.if_tomorrow(date.text, days):
                No = tr.find('.//td[1]')
                jigen = tr.find('.//td[3]')
                yield No.text, date.text, jigen.text

    def check(self, id_, days=1, password=None):
        if password == None:
            password = keyring.get_password('IbarakiUniv', id_)
        page_source, cookies = self.login(id_, password)
        subject_dic = self.get_subject_schedule(page_source)

        schedule = []
        for name, url in subject_dic.items():
            for No, date, jigen in self.has_lesson(url, cookies, days):
                info = '%s: 第%s回,%s,%s' % (name, No, date, jigen)
                schedule.append(info)

        self.driver.close()
        return schedule

    def register_email(self, adress, password):
        yagmail.SMTP(adress, password)

    def notice_by_email(self, from_, to, schedule, password=None):
        if password == None:
            yag = yagmail.SMTP(from_)
        else:
            yag = yagmail.SMTP(from_, password)

        if len(schedule) == 0:
            schedule = ['授業ないよ!!!!!!!!!!!!!']
        try:
            yag.send(to, 'Your Lesson INFO', schedule)
        except Exception:
            print('Something crushed down')
        else:
            print('Send email successfully')
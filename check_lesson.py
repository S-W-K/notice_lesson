# -*- coding: utf-8 -*-
# @Author: S_W_K
import yagmail
import datetime
from requests.cookies import RequestsCookieJar
import requests
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import base64
import pickle


class NoticeYou:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)

    def register(self, student_id, password):
        student_id = student_id.encode('utf-8')
        student_id = base64.b64encode(student_id)
        password = password.encode('utf-8')
        password = base64.b64encode(password)
        with open('IbarakiUniv.pkl', 'wb') as f:
            pickle.dump([student_id, password], f)

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

        return jar

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

    def check(self, id_=None, days=1, password=None):
        if password == None:
            with open('./IbarakiUniv.pkl', 'rb') as f:
                id_password = pickle.load(f)
            id_ = base64.b64decode(id_password[0]).decode('utf-8')
            password = base64.b64decode(id_password[1]).decode('utf-8')
        cookies = self.login(id_, password)

        request_url = 'https://idc.ibaraki.ac.jp/portal/StudentApp/Top.aspx'
        response = requests.get(request_url, cookies=cookies)
        page_source = response.text
        subject_dic = self.get_subject_schedule(page_source)

        schedule = []
        for name, url in subject_dic.items():
            for No, date, jigen in self.has_lesson(url, cookies, days):
                info = '%s: 第%s回,%s,%s' % (name, No, date, jigen)
                schedule.append(info)

        self.driver.quit()
        return schedule

    def register_email(self, address, password):
        address = address.encode('utf-8')
        address = base64.b64encode(address)
        password = password.encode('utf-8')
        password = base64.b64encode(password)
        with open('email.pkl', 'wb') as f:
            pickle.dump([address, password], f)

    def notice_by_email(self, to, schedule, from_=None, password=None):
        if password == None:
            with open('./email.pkl', 'rb') as f:
                from_password = pickle.load(f)
            from_ = base64.b64decode(from_password[0]).decode('utf-8')
            password = base64.b64decode(from_password[1]).decode('utf-8')
        yag = yagmail.SMTP(from_, password)

        if len(schedule) == 0:
            schedule = ['授業ないよ!!!!!!!!!!!!!']
        try:
            yag.send(to, 'Your Lesson INFO', schedule)
        except Exception:
            print('Something crushed down')
        else:
            print('Send email successfully')

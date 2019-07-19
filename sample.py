# -*- coding: utf-8 -*-
# @Author: S_W_K

from check_lesson import NoticeYou

if __name__ == '__main__':
    NY = NoticeYou()
    a = NY.check(id_='student_id',password='student_password')
    NY.notice_by_email(from_='from_email_address',
                       to='to_email_address',
                       schedule=a,password='YourEmailPassword')

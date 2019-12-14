# -*- coding: utf-8 -*-
# @Author: S_W_K

from check_lesson import NoticeYou

NY = NoticeYou()
# register only need do once
NY.register(YourStudentID,StudentID_password)
NY.register_email(YourEmailAdress,EmailAdress_password)

schedule = NY.check()
NY.notice_by_email(to='to_email_address', schedule=schedule)

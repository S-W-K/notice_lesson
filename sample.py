# -*- coding: utf-8 -*-
# @Author: S_W_K

from check_lesson import NoticeYou

# register only need do once
# NY.register(YourStudentID,StudentID_password)
# NY.register_email(YourEmailAdress,EmailAdress_password)

NY = NoticeYou()
schedule = NY.check()
NY.notice_by_email(to='s979612095@gmail.com', schedule=schedule)

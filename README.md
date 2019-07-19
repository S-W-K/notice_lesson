# notice_lesson
茨城大学のDreamCampusから授業情報をスクレイピングし，メールでお知らせ！

# Dependencies
```python
pip install lxml,selenium,requests,yagmail,keyring
```

そして，[ChromeDrive](http://chromedriver.chromium.org/)をダンロード，PATHに添加する．

# Usage
```python
from check_lesson import NoticeYou

NY = NoticeYou()
schedule = NY.check(id_='student_id',password='student_password')
NY.notice_by_email(from_='from_email_address',
                       to='to_email_address',
                       schedule=schedule,password='YourEmailPassword')
```

パスワードをスクリプトにそのまま保存したくない方は，keyringを介したパスワード管理をおすすめ．
```python
# register your student id and password
NY.register(student_id,student_password)

# register your email_address and password
NY.register_email(email_address,email_password)
```
以上のコードでパスワードをkeyringに登録できる（一回実行すればオーケー）．
パスワードが登録された後，スクリプトにパスワードの入力が不要になる．
```python
schedule = NY.check(id_='student_id')
NY.notice_by_email(from_='from_email_address',
                       to='to_email_address',
                       schedule=schedule)
 ```                      
 
# スクリプトの自動化
LinuxとMacユーザーはcrontabを使えば，設定された時間に自動的にスクリプトを実行し，
送信することができる．

もう振り替えの時，授業を忘れる心配がなし！

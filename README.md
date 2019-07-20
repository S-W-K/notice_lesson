# notice_lesson
茨城大学のDreamCampusから授業情報をスクレイピングし，メールでお知らせ！

# Dependencies
```python
pip install lxml,selenium,requests,yagmail
```

そして，[ChromeDrive](http://chromedriver.chromium.org/)をダンロード，PATHに添加する．

# Usage
## Basic
```python
from check_lesson import NoticeYou

NY = NoticeYou()
schedule = NY.check(id_='student_id',password='student_password')
NY.notice_by_email(from_='from_email_address',
                       to='to_email_address',
                       schedule=schedule,password='YourEmailPassword')
```
## Register
パスワードをスクリプトにそのまま保存したくない方は，`register`と`register_email`関数を使ってください．
```python
# register your student id and password
NY.register(student_id,student_password)

# register your email_address and password
NY.register_email(email_address,email_password)
```
以上のコードでパスワードをkeyringに登録できる（一回実行すればオーケー）．
パスワードが登録された後，スクリプトにIDとパスワードの入力が不要になる．
```python
schedule = NY.check()
NY.notice_by_email(to='to_email_address',schedule=schedule)
 ```                      
 ## Check Another Day
 デフォルトの設定は明日の授業をチェックする．
 しかし，`check()`関数の*days*パラメーターの値変更することで，チェックする日付を変えることが可能．
 ```python
 schedule = NY.check(days=1) # 明日の授業をチェックする（デフォルト）
 
  schedule = NY.check(days=-3) # 3日前の授業をチェックする
  
  schedule = NY.check(days=0) # 今日の授業をチェックする
 ```
 
# スクリプトの自動化
LinuxとMacユーザーはcrontabを使えば，設定された時間に自動的にスクリプトを実行し，
送信することができる.  
書き方は[check_lesson.sh](https://github.com/S-W-K/notice_lesson/blob/master/check_lesson.sh)を参照してください．

> *P.S.*  crontabで実行する時，絶対パスしか使えない！あと，実行環境のPATH情報もスクリプトに指定する必要がある．パス情報は
`echo ${PATH}`で調べられる

**もう振り替えの時，授業を忘れる心配がなし！**

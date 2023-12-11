注册
登录
激活
验证
注销
重置
修改
操作，对用户模块，能够说明流程，抓取界面，已经实现；
对业务模块，说明功能、设计界面、说明流程，可以不实现
django
pip install django
conda install django

1、启动
(p39) H:\test\python1\www_book1>py manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 16, 2023 - 20:09:19
Django version 4.1.3, using settings 'www_book.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

2、浏览器地址栏
http://127.0.0.1:8000/

3、用户密码
其他+abcabcab
1+1

EMAIL_HOST_USER = 'abcd@126.com'
EMAIL_HOST_PASSWORD = 'abcd的SMTP密码'

4、测试，增加内容的手段
盗链\输入\

5、概述、需求分析、概要设计、详细设计及实现
详细设计及实现
(1)用户注册模块
(2)用户登录模块
功能、操作流程、界面、程序流程、配置、代码（可选）
(3)

6、MTV
model（数据库）、template（网页）、view（函数）

https://www.runoob.com/django/django-tutorial.html
https://www.runoob.com/bootstrap5/bootstrap5-tutorial.html

7、其他
django的request与网络爬虫的request不同
模板语法，{{ var_nam }} {% for k in vs %} {% endfor %} {% if v %} {% endif %}
import requests
data_list = requests.get("http://chinaunicom.com/api/article/NewsByIndex/1/2023/20/news")
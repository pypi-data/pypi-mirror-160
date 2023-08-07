# 小工具

- common
    - exceptions: 异常处理
    - ftp: FTP上传下载
    - logger: 日志打印
    - mail: 邮件发送
    - retry_decorator: 重试装饰器
    - setqueue: 去重队列，有序去重队列
- db
    - mysql
    - redis
- spider 爬虫基类
    - basespider
    - selenium_spider

```shell
# 打包环境

# 安装
pip install -i https://pypi.org/simple/ wise-utils

# 打包
python3 -m build

python3 -m twine upload --repository testpypi dist/*

python3 -m twine upload --repository pypi dist/*
```

```angular2html
python setup.py sdist
python setup.py install
pip install twine
twine upload dist/*
```

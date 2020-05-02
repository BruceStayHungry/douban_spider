# CookiesPool

可扩展的Cookies池，目前对接了豆瓣(https://www.douban.com)，可自行扩展其他站点


## 安装

```
pip3 install -r requirements.txt
```

## 基础配置 

### 接口基本配置

```python
# Redis数据库地址
REDIS_HOST = 'localhost'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'foobared'

# 产生器使用的浏览器
BROWSER_TYPE = 'Chrome'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'douban': 'DoubanCookiesGenerator'
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'douban': 'DoubanValidTester'
}

# 检测器检测接口
TEST_URL_MAP = {
    'douban': 'https://www.douban.com'
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5000

```

### 进程开关

在config.py修改

```python
# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
# API接口服务
API_PROCESS = True
```



## 导入账号

```
python3 importer.py
```

```
请输入账号密码组, 输入exit退出读入
18459748505----astvar3647
14760253606----gmidy8470
14760253607----uoyuic8427
18459749258----rktfye8937
账号 18459748505 密码 astvar3647
录入成功
账号 14760253606 密码 gmidy8470
录入成功
账号 14760253607 密码 uoyuic8427
录入成功
账号 18459749258 密码 rktfye8937
录入成功
exit
```


## 运行

请先导入一部分账号之后再运行，运行命令：

```
python3 run.py
```

## 运行效果

三个进程全部开启：


```
API接口开始运行
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
Cookies生成进程开始运行
Cookies检测进程开始运行
正在生成Cookies 账号 14747223314 密码 asdf1129
正在测试Cookies 用户名 14747219309
Cookies有效 14747219309
正在测试Cookies 用户名 14740626332
Cookies有效 14740626332
正在测试Cookies 用户名 14740691419
Cookies有效 14740691419
正在测试Cookies 用户名 14740618009
Cookies有效 14740618009
正在测试Cookies 用户名 14747222472
Cookies有效 14747222472
Cookies检测完成
成功获取到Cookies 
成功保存Cookies
```

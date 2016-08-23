#-*- coding:utf-8 -*-
import logging

# 配置日志信息
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='w')

# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

# 设置日志打印格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)

# 将定义好的console日志handler添加到root logger
logging.getLogger('console').addHandler(console)

#log = logging.getLogger('console')
#log.debug('this is a test')

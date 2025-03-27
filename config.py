import configparser
# 创建配置文件对象
con = configparser.ConfigParser()
# 读取文件
con.read("config.ini", encoding='utf-8')
# 获取所有section
sections = con.sections()
image_items = dict(con.items('image'))
window_items = dict(con.items('window'))

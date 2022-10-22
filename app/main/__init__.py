# -*- coding:utf-8 -*-


from flask import Blueprint

# 第一个参数：蓝图名字，自定义,随意;
# 第二个参数：'__name__' 蓝图所在的模块或者包，一般为'__name__'变量
main = Blueprint('main', __name__)

# app/__init__.py 中初始化 app 实例的时候，会加载 Flask 插件和注册蓝图
# 所以会把蓝图和插件都 import 进来
# 而蓝图下的视图 views 的业务逻辑又需要用到插件，所以又会需要 import 进来
# 这样就形成了
#
# app/auth/views.py ←-------+
#      ↓(注册蓝图)           |
# app/__init__.py           |(views 的业务逻辑需要引入插件)
#      ↑(初始化插件)         |
# app/plugins/db -----------+
#

# 这样一定要在初始化完成蓝图后再 import 进来
from . import views

[TOC]

最好还是翻翻狗书吧
# 路由URL

* url变量规则   
转换器: 把url的部分作为关键字传递给函数, 现有转换器有:````int````,````float````,````path````用法: ```<int:post_id>```   
那如果我想用<正则表达式>来规定路由规则呢？<麦子学院那个课好像有讲>

* URL后面有没有 ‘/’ 的区别
> ```` /projects/````标准写法,就像访问文件夹路径一样
> ````/about```` 就像访问一个文件   
> 访问一个结尾没有斜杠的URL时, flask会重定向, 帮你在后面加一个斜杠, 所以如果你访问的是````/about/````就会404错误

* url_for   
要修改的话, 你只要改处理这个URL的函数就行了, 其他访问这个路径的地方不会有牵连


# HTTP方法
通常有```OPTIONS、GET、HEAD、POST、PUT、DELETE、TRACE 和 CONNECT ```这八个方法   
即告诉服务器一个页面请求要做什么,缺省情况下, 一个路由只回应get请求

```
可以通过methods参数使用不同的方法
@app.route('/test',methods=['GET','POST'])
def test():
    if request.method == 'POST':
        pass
```

* get  
    浏览器告诉服务器,要得到页面上的哪些信息

* head  
    浏览器告诉服务器想要得到的信息, 但只要得到信息头就行了,页面内容不要

* post  
    浏览器告诉服务器想要向 URL 发表一些新的信息, 服务器必须确保数据被保存好
    且**只保存一次**. HTML表单实际上就是使用这个访求向服务器传送数据的

* put  
    和post类似,不同的是服务器可以触发**多次存储**过程而把旧的值覆盖掉。

* delete  
    删除给定位置的信息

* options  
    为客户端提供一个查询url支持那些方法的捷径.

# 静态文件
所需要的静态文件一般是 CSS 和 JavaScript, Flask的静态文件都放在```/static```文件夹中,
使用选定的```static```端点,就可以生成相应的 URL:
````
url_for('static', filename='style.css') # 这个静态文件的位置就是 static/style.css
````

# 渲染模板
在 Flask 内部生成 html 相当笨拙，且你必须自己负责```html```的转义以确保应用的安全，因此
 Flask 提供了JinJa2模板引擎, Flask 中渲染的 HTML 文件统一放在```templates/```文件夹中
````
render_template('test.html',name=name) # 访问templates/test.html这个文件
# {{name}}获取和使用传进来的name参数
````
* 自动转义默认开启  
如果name包含 html ,那会被自动转义

# 操作请求数据

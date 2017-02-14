[TOC]

**[慕课网-HTML+CSS基础课程](http://www.imooc.com/learn/9)**

# HTML

* 一般
 * 加粗:```<strong></strong>```
 * 斜体:```<em></em>```
 * 引用:```<q></q>```
 * 分割:```<hr />```
 * 换行:```<br />```
 * 短代码:```<code></code>```
 * 多行代码:```<pre></pre>```
 * 引用长文本,样式缩进: ```<blockquote></blockquote>```
* 列表
 * 无序列表
     ```
     <ul>
        <li></li>
    </ul>
     ```
 * 有序列表
     ```
    <ol>
        <li></li>
    </ol>
     ```
* 表格
    <table summary = "表格简介"> #table 整个表格内容下载多少就显示多少<br />
      <tbody> # tbody整个表格内容下载完才显示出来 <br />
        <caption>表格标题</caption>
        <tr> # 一行
          <th>班级</th> # 表头
          <th>学生</th>
        </tr>
        <tr>
          <td>一班</td> # 一列
          <td>30</td>
        </tr>
* 链接
 * 超链接
    ````
    <a href="http://www.google.com" title="鼠标划过显示" target='_blank' >
    链接(target='_blank'新窗口打开)</a>
    ````
 * 邮箱
    第一个参数前要加'?'后面的参数前加'&'
    cc:抄送 bcc:密抄 subject:主题 body:内容 多个邮箱地址用';'分开
    ````
    <a href="mailto:m_kepler@foxmail.com?cc=870131615@qq.com
    &bcc=870131615@qq.com;jie.1995.cool@163.com&subject=主题&body=内容">发邮件</a>
    ````
* 图片img

    ```<img src="图片地址" alt="下载失败时替换的文本" title="悬停文字">```
* 表单
```
    <form method = "传送方式" action = "服务器文件">
        <input type="text或password" name="名称" value="预设值" />
        <input type="submit或reset" value="提交／c重置" >
        <!-- 同一组单选按钮, name一定一直 -->
        <label>男</label>
        <input type = "radio单选checkbox多选" value="提交的值" name="名称" checked="checked">
        <!-- 下拉框 -->
        <option value="选项１">选项１</option>
        <option value="选项2">选项2</option>
        <option value="选项3" selected="selected">选项3</option>
        <!-- 标签for的值要和相关控件的id值相同 -->
        <label for="male">男</label>
        <input type="radio" name="gender" id="male">
        <!-- 文本框 -->
        <textarea rows="行数" cols="列数"> ---文本框--- </textarea>
    </form>
```

# CSS

引用<span id="jump">优先级</span>: 内联 > 嵌入 > 外部, 总结起来就是就近原则(离被设置元素跃进优先级别越高)

* 内联式
```
# 这些都放在了head下的style标签内
# 给p标签添加样式，p称为选择器, {}里的就是样式
p{
    font-size:21px;/*这是注释*/
    color:red;
}
```

* 内嵌样式
```
    <p style="color:red;font-size:12px">这里是红色</p>
```

* 外部css文件
```
    # 引入a.css
    <link rel="stylesheet" href="a.css" type="text/css" media="screen" title="test css" charset="utf-8">
```

* 选择器
 * 类选择器

```
.setGreen{
    color:green;
}
<span class="setGreen"></span>

/* ↑两者的区别↓ */
1. id选择器只能在文档中使用一次
2. 类选择器效果可以叠加
```

 * id选择器

```
#setYellow{
    color:yellow;
}
<span id="setYellow"></span>
```

 * 子选择器

```
// 子选择器可对某个标签下的内容套用样式
.subselector > span{
    border:1px solid red;
}
<p class="subselector"><span>测试</span></p>

/* ↑两者区别↓ */
子选择器样式只包含头尾
后代选择器将标签下的子标签都套用了样式
```

 * 包含(后代)选择器

```
//子选择器的>去掉就成了
    <ul class="includeselector">
      <li> 包含选择器
        <ul>
          <li> test1 </li>
          <li> test2</li>
        </ul>
      </li>
    </ul>
```

 * 通用选择器

```
// 所有的标签都套用了这个样式
 * {color:red; font-size:20px;}
```

 * 伪类选择器

```
允许给html不存在的标签设置样式
b:hover{color:green;}
<b> </b>
或:比如,给有链接的文字添加鼠标滑过的样式
a:hover{color:red; font-size:20px}
<a href="http://www.baidu.com">百度</a>
```

 * 分组选择符

```
/* 给多个标签元素设置同一个样式, 分组选择符"," */
h1,span{color:red;}
.first, #second span{color:green;}
```

* <span id="jump2">继承</span>
> css的有些样式具有继承性;允许杨思不仅作用与某个特定的html标签，而且作用做这个标签下的
所有其他标签（子选择器？后代选择器？）

```
    aa{color:green;}
    aa{border:1px solid red;}
```

* 特殊性(权值)

> 有时候为一个元素设置了多个样式后, 元素会启用哪个CSS样式呢？
联想到上面说的[优先级和权值](#jump)

```
    /* 标签权值为1 类选择符权值为10 ID选择符为100
	p{color:red;} /*权值为1*/
	p span{color:green;} /*权值为1+1=2*/
	.warning{color:white;} /*权值为10*/
	p span.warning{color:purple;} /*权值为1+1+10=12*/
    #footer .note p{color:yellow;} /*权值为100+10+1=111*/
```

* 层叠

> 如果一个权值相同的标签有多个css样式呢?那就不是有优先级来决定,由css样式的
> 前后顺序来决定,处在最后的css样式会被应用,后面的样式会覆盖前面的样式
和[继承性](#jump2)区分开吧

```
    p{color:red;}
    p{color:green;}
    <p class="first">jfadjffasdkfjasdkfj</p>
```

* 最高权值

> 某些特殊情况需要为耨写样式设置具有最高权值,用!important

```
    p{color:red!important;}
    p{color:green;}
    <p class="first">jfadjffasdkfjasdkfj</p>
```

## 字体排版

```
# 如果用户电脑没有你设置的这个字体,将会显示浏览器的默认字体
span {
    font-family:"宋体";
    font-size:12px;
    color:#666;

    letter-spacing:50px; /* 设置字母间距 */
    word-spacing:50px; /* 单词间距 */
    line-height:1.5em; /* 设置1.5倍行间距 */

    font-weight:bold; /* 设置粗体 */
    font-style:italic; /* 设置斜体 */
    text-decoration:underline; /* 下划线 */
    text-decoration:line-through; /* 删除线 */

    text-indent:2em; /* 缩进两空格 */
    text-align:center; /* 元素居中,left\right */
}
```

## 元素分类

> 块级元素: ``` <div> <p> <h1> <form> <ul>和<li> ```
> 内联(行内)元素: ```<span> <a> <label> <strong>和<em> ```
> 内联快级元素: 同时具备内联和块级两种元素特点

块级元素特点:
* 每个块状元素都是从新的一行开始,并气候的元素也另起一行
* 元素的高度、宽度、行高、顶底距都可以设置
* 宽度默认和父元素的宽度一致

内联元素特点:
* 和其他元素都在一行上
* 元素的高度、宽度、顶底距都**不可以**设置
* 元素宽度就是它包含的文字或图片的宽度,不可改变

内联块级元素特点:
* 和其他元素都在一行上
* 元素的高度、宽度、顶底距都**可以**设置

```
将元素显示为块级元素: span{display:block;}
将块级元素显示为行内元素: div{display:inline;}
内联块级元素: { display:inline-block; }
```

## 盒子模型

> 块级标签都具备盒子模型的特征

![盒子模型](http://img.mukewang.com/543b4cae0001b34304300350.jpg)

```
border: 边框
margin: div和div之间
padding: (填充)距离边缘
```

### 边框border

> 可以设置粗细、样式、颜色三个属性

```
div{ border:2px solid red; }
或
div{
    border-width:2px; # 可单独设置上下左右某条边框 border-top bottom left right
    border-style:solid; # dashed虚线, dotted点线
    border-color:red; # 可设置十六进制颜色
}
```

### 宽度和高度

> css内定义的宽width高height都是指包括margin + border + padding的总和

![盒模型-宽度](http://img.mukewang.com/539fbb3a0001304305570259.jpg)

```
div{
    width:200px;
    padding:20px;
    border:1px solid red;
    margin:10px;
}
```

### 边界margin

> padding在边框里,margin在边框外; 设置都差不多,没什么好说的


### 填充padding

> 元素内容与边框之间的距离,称做填充. 顺序必须是↑→↓←

```
div{padding:10px;} # 如果上右下左都填充10px的话
div{padding:10px 20px;} # 上下10px; 左右20px;
div{
    padding-top:10px;
    padding-right:20px;
    padding-bottom:18px;
    padding-left:30px;
}
```

## 模型

> 包括流动模型/层模型/浮动模型

### 流动模型

> 默认的网页布局模式

特点:
* **块状元素**都会在所处的**包含元素**内自上而下按顺序垂直延伸
* **内联元素**都会在所处的**包含元素**内从左到右水平分布显示

### 浮动模型

>

### 层模型

> 层模型有三种形式: 绝对定位(position:absolute) 相对定位(position:relative) 固定定位(position:fixed)

* 绝对定位

> 相对于其最接近的一个具有定位属性的父包含块进行绝对定位。如果不存在这样的包含块，则相对于body元素，即相对于浏览器窗口。

* 相对定位

>

* 固定定位

>


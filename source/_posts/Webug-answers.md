---
title: Webug 漏洞练习平台V3.0 答案篇
date: 2018-07-05 22:58:39
categories: 
- 渗透测试
- 小试牛刀
tags: [渗透, 攻略]
---
> <p style=" color: red; "><b>【2018年9月17日更新】</b></p>虽然我已经就把基础的题目都过了一遍，但我还是决定停止更新本文，原因是 webug 里很多题目都设置不算很好，而且缺乏验证答案机制，不容易出题人意图，更不容易写成博客。顺便安利一下我在使用的一个国外汇总类 CTF 网站 [Wechall](http://www.wechall.net/)，感兴趣的小伙伴可以去那个网站里选择喜欢的进行学习，选择很多，而且很多质量都很高。

本文基于 Webug 3.0 版本，因为不是攻略详解，因此对于每关仅给出破解的图文过程（获得的 flag 我会打个码，希望小伙伴还是要自己实践一下），详细的漏洞原理会通过参考链接给出，供对于某一个漏洞有兴趣的小伙伴进一步学习。

<!-- More -->

## 第一关

![第一关截图](/Webug-answers/First/First.PNG)

这一关主要考察 GET 型 SQL 注入（因为知道肯定可以注入，我就省略注入点测试部分，详情可以参考链接）。

首先，通过 order by 语句猜测返回参数的个数（其实看到题目就可以猜到是4个了，保守起见可以试一下别的数字）。还有一种方法是直接使用 union select，与 order by 一样，返回没有报错就证明猜对了。在输入框填写如下语句：

`1' order by 4 #` // 这里所有的符号都是必须的，不然就会报错

这样实际执行的语句是 select * from goods where id='1' order by 4 #' ，超过4后就会报错，证明了该表只有4个属性。

然后，现在就能使用 union select 来进行爆库以获取本题的 flag。

1. 获取表名

`2' and 1=2 union select 1,2,3,group_concat(table_name) from information_schema.tables where table_schema='pentesterlab' #` // 这里我默认是知道 flag 表在 pentesterlab 库中，不然可以使用 database() 来获取当前库，或者 information_schema.schemata 的 schema_name 获取所有的库。其中的 “1=2”主要用来减少无关数据的输出而已，你可以删掉来看看效果

![获取表名](/Webug-answers/First/Table_name.PNG)

2. 获取目的表的字段

`2' and 1=2 union select 1,2,3,group_concat(column_name) from information_schema.columns where table_schema='pentesterlab' and table_name='flag' #`

![目的表的字段](/Webug-answers/First/Column_name.PNG)

3. 获取 flag

万事俱备，只欠东风了

`2' and 1=2 union select id,flag,null,null from flag #`

![第一关答案](/Webug-answers/First/Answer1.PNG)

至此，成功拿到第一个 flag（YEAH!!）。答案我就不直接给了，希望小伙伴们亲自体验一下过程，除了获取 flag 外，还可以拿到 root 用户密码等，大家可以自行发挥~

## 第二关

![第二关截图](/Webug-answers/Second/Second.PNG)

本关考察的是图片隐写术~~（比如图种什么的，嘿嘿嘿... ）~~，最简单的方法就是把下载的文件改后缀为 .rar，这样就会出现一个 123.txt，里面就保存着 flag。

但这样的确有点撞彩的感觉，所以提供一个专业一点的方法：通过编码分析器对图片进行分析，我这里使用的是 Kali 系统自带的 binwalk 工具，结果如下图：

![Binwalk 结果图](/Webug-answers/Second/Binwalk.PNG)

很明显，在图片偏移 7549 字节之后的内容就是一个 rar 压缩包，然后可以使用 dd(1) 指令进行文件分离：

![dd 指令分离文件图](/Webug-answers/Second/DD.PNG)

得到的结果如下，答案就在 123.txt 中：

![第二关答案图](/Webug-answers/Second/Answer2.PNG)

图片隐写术挺有意思的，我在参考链接会提供一个比较全面介绍这种技术的博文，感兴趣的小伙伴可以参阅一下。

<font color=red> **【注意】**Webug V3.0 里题目的解答系统并没有完善，所以答案并不能通过验证，这一点我参考过很多攻略文章，得到的回答就是官方说并没有做答案验证模块，所以大家只要能得到 flag 就好，不要太钻牛角尖. </font>

## 第三关

![第三关截图](/Webug-answers/Third/Third.PNG)

虽然我是不信的（但我身体很诚实），结果的确不是这个，查看一下页面源码（不过这道题其实在问题界面就给了提示）

![第三关源码](/Webug-answers/Third/Source.PNG)

由上图可知，这套题考察的就是扫目录。在解密的时候，由于题目所在目录并没有设定访问权限，所以可以使用一个偷懒的方法——直接打开父目录。

![目录结果图](/Webug-answers/Third/Directory.PNG)

本来这题如果使用了工具进行扫描估计只能扫出 test 目录，然后会得到这个内容：

![Test 目录内容](/Webug-answers/Third/WrongPage.PNG)

这里需要你将目录名（也就是 test）进行16位 md5 加密后在访问，也就是要打开上图所示的 4621d373cade4e83 目录，不过我通过偷懒的方法首先打开的就是第一个目录，轻而易举地获得 flag（按照惯例真正的答案我会隐藏）。

![第三关答案图](/Webug-answers/Third/Answer.PNG)

## 参考链接

第一题：[SQL注入系列之PHP+Mysql手动注入](https://blog.csdn.net/u011781521/article/details/53959201)

第二关：[图片隐写术总结](https://blog.csdn.net/riba2534/article/details/70544076)

第三关：[自动化扫描工具](https://wizardforcel.gitbooks.io/kali-linux-web-pentest-cookbook/content/ch5.html)

其他攻略推荐：

[Webug通关攻略](http://foreversong.cn/archives/630)
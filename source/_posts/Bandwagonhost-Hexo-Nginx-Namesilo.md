---
title: Bandwagonhost+Hexo+Nginx+Namesilo 搭建个人Blog经验总结
date: 2018-04-25 07:11:14
categories: 
- 经验总结
- 个人博客
tags: [Hexo, Nginx, Bandwagonhost, Namesilo]
comments: true
---
><font color=#FF0000><b>【2018年6月19日更新】</b></font><br> 本博客已经改为使用 Github Page 作为服务器，因为发现使用 VPS 作为服务器后，我科学上网后不断被封端口，估计和墙的特征识别有关系，所以如果你的 VPS 主要是作为科学上网的工具，就考虑别当个人博客的服务器了。

><font color=#FF0000><b>【2018年5月17日更新】</b></font><br>搬瓦工官网现在已经改为 [https://bwh1.net/](https://bwh1.net/) ~~(最主要是没有被墙了)~~。顺便安利一个[搬瓦工中文网](https://www.bandwagonhost.net/)，里面有很详细的选购方案攻略和最新可够买方案咨询，博主受益匪浅，所以也希望大家在提问前可以先去该网站浏览一下，应该能找到你想要的答案。

本文并不是从头开始带你搭建个人 Blog 的完整详细攻略，而是博主在搭建本 Blog 遇见的一些问题和经验的总结，毕竟技术是不断在进步，一些以往的经验可能在新版本已经不适用了，所以希望本文能给想自行搭建 Blog 的各位一些帮助，能让大家少走点弯路～

<!-- more -->

## 准备工具
1. 科学上网软件（Lantern、游戏加速器等）
2. 钱 ~~(废话)~~

## 搭建步骤
1. **购买并搭建好 VPS**
2. 在 VPS 上搭建 Hexo 环境
3. 在 VPS 上搭建 Nginx 
4. 将 Hexo 部署到 Nginx 上
5. 注册域名并将添加域名解析

**P.S. 以上步骤除了第一步是必要前提外，其它的顺序可以按照你喜欢的方式进行**

## 搭建 VPS
**<font color=#FF0000>【注】有点尴尬了，博主原来使用的教程好像已经被封了，所以下面提供的链接是找了个步骤基本一样的博文，按着做应该也没有问题</font>**

[搬瓦工Bandwagon一键搭建ShadowSocks翻墙教程](http://www.huizhanzhang.com/2017/05/bandwagon-one-key-shadowsocks.html)
***
~~搭建 VPS 期间遇到的最大的问题主要是搬瓦工的官网（和它的 Kiwivm 控制台网站）已经被墙了，所以你需要有一个能科学上网的软件才能购买 VPS 并进行 ss 的搭建(感觉像是一个悖论)。利用什么软件进行科学上网我这里就不推荐了，请大家自行 Google 吧。~~

整体的搭建过程还是很简单的，这里我就不浪费篇幅进行重复描述了，直接进入下一步了。

**<font color=#FF0000>【注2】搭建到安装系统时，最好选择 centos-7-x86_64(-bbr 带不带bbr都行)。因为博主之前时默认使用了centos-6-x86-bbr，然后在安装 Node.js 的时候显示系统版本不兼容。。。</font>**

## 在 VPS 上搭建 Hexo 环境
后面四步主要参考以下文章：
[在搬瓦工 VPS 上搭建 Hexo](https://www.jianshu.com/p/605c3d32cab9)

然而，这一步完全可以在官方文档处获得帮助，**官网还有中文哦～**

部署 Hexo 前，需要安装两个依赖—— Node.js 和 Git（建议大家在安装时候都先搭建好 ss，因为不清楚哪个的源会不会已经被墙掉）。其它按着官方文档的步骤走基本不会有什么大问题，搭建完 Hexo 就可以进入下一步了。

完成 Hexo 的部署后，可以开启其自带的本地服务器进行测试，指令如下：
``` bash
cd /Hexo-Path   # “/Hexo-Path”替换为你当时搭建 Hexo 的文件夹
hexo clean
hexo g
hexo s --debug
```
这样，Hexo 就可以通过本地的4000端口进行访问。然而，博主是使用 ssh 方式登陆 VPS，没有图形界面怎么打开浏览器并访问4000端口呢？

这里，可以采用将本地端口与远程服务器端口进行绑定的方法，然后用本地浏览器打开绑定端口即可，一行指令就能解决问题：
``` bash
ssh username@address_of_remote -p [ssh端口号] -L 127.0.0.1:1234:127.0.0.1:4000
```
-p 选项是选填的，因为有些 VPS 的 ssh 端口默认是22，如果不是就要填写正确的端口号。
这样，我们就将本地的1234端口与 VPS 的4000端口进行绑定，然后在本地浏览器输入 localhost:1234 就可以访问到测试的博客网站咯～


## 在 VPS 上搭建 Nginx
博主在安装到这一步的时候，按着之前提供的简书步骤安装，出现了找不到 nginx 安装包的问题。当时我使用的软件源是 epel-release-7-9.noarch，但我在写这篇博文前又测试了一次，这次却可以成功安装了，我猜测可能是当时软件源暂时下架的了该软件包吧。如果大家遇到找不到 nginx 软件的问题，可以参考一下 nginx 官方文档。

文档是英文的，为了方便大家，我就把 CentOS 的 Nginx 安装过程写在下面：

1、 在 /etc/yum.repos.d/ 目录内创建 nginx.repo 文件，在文件内添加如下内容：
``` bash
# 这里选择安装的是稳定版，需要其它版本的自行参考官方文档。
name=nginx repo
# 这里的“centos/7/”请按着自己系统进行调整
baseurl=http://nginx.org/packages/centos/7/$basearch/ 
gpgcheck=0
enabled=1
```
2、 执行以下指令即可完成安装：
``` bash
sudo yum -y update
sudo yum -y install nginx
```
官方文档链接在参考资料处。

## 将 Hexo 部署到 Nginx 上
安装完了 Hexo 和 Nginx 后，你离完成搭建也就不远了。

值得注意的是对 rsync 的配置：
``` bash
deploy:
  type: rsync
  host: 你 VPS 的 IP 地址或者域名
  user: root
  root: 你想将 Hexo 生成的静态文件存放在 VPS 中的目录 例如: /www/hexo/blog/
  port: 你 VPS 的 ssh 端口号
  delete: true
  verbose: true
  ignore_errors: false
```
这里的 root 项需要填写一个不同于你 Hexo 搭建时使用的文件夹，因为这个 root 是供 nginx 使用的，如果你这里填写了和 Hexo 搭建时一样文件夹会出现文件被覆盖的严重问题。

至此，你已经真正完成了个人博客的搭建，在浏览器中输入你的 VPS 地址就可以访问个人博客了，鼓掌👏👏👏

## 为 Hexo 更换主题
原本 Hexo 更换主题应该是一项十分轻松简单的任务，然而博主却在这一步耗费了大量时间。因此，本节主要是介绍 Hexo 更换主题的方法，以及我遇到的一些问题：

**1、下载主题**

[Hexo 官方主题站](https://hexo.io/themes/)上有很多主题供你挑选，选择一款你喜欢的。
例如，本博客使用了 black-blue 这款。

将它 clone 到 Hexo 的 themes 目录内：
``` bash
git clone https://github.com/maochunguang/black-blue /PATH_To_Blog/themes/
```

**2、配置主题**

在个人博客的根目录内有 _config.yml 文件，这是整个站点的配置文件，在文件内找到 themes 字段并将其从 landscape 修改为 black-blue。

至此，主题已经成功配置成功。

>**<div align="center"><font color=#FF0000 size="6">注意</font></div>**

> 博主之所以在更换主题这一步耗费了大量时间，主要是更换主题后，打开网站后出现了主题显示严重异常的问题。我一开始以为是在部署前没有调用 hexo clean 来清理缓存导致内容显示出错，然而重新部署后问题依然存在。然后，我想在本地端口进行测试，看看主题是否仍然显示错误，但在本地服务器运行的网站却能正确地显示更换后的主题。这就让我十分无语。。。我各种 Google 和逛论坛寻找答案皆无果，都已经准备放弃这个主题了。最后自己想了想，会不会是浏览器自身的缓存了原先网站的内容才导致了显示错误呢？
> 
> 于是我将浏览器的缓存清了一下，**接着就能正常显示了！！**这个问题实在让我哭笑不得，我暂不清楚这个是我使用的这个主题的问题，还是我本人的 chrome 浏览器的问题（但我在手机浏览器也遇到同样的问题）。所以在这里给需要自定义主题的朋友们提个醒，**<font size="5">在更换主题后可以先清一下浏览器的缓存再打开网站</font>**

## 注册域名并将添加域名解析
这一步并不是必须的，如果你想要别人能更加轻松地访问你的博客的话最好还是注册一个域名，其实也没有多贵，但能换来很多的便利。

博主在这一步主要参考这个博文：[域名购买及使用教程](https://www.jianshu.com/p/27b0ebdcec2c)

大家跟着这个博文进行注册理论上不会有什么大问题，我这里只是补充几点：

1. Namesilo 里标出的域名价格都是按一年算的（打折也只是首年打折），而且你一定要注意看最后结算的金额再给钱（有些域名是特别的，价格会很高）
2. 注册后设置域名解析的话，如果是国内访问的流量多，最好选择国内的 DNS 服务器（具体我就不推荐了，免得广告嫌疑）

## 结束语
这是博主的第一篇正式博文，可能在格式排版之类稍有不足，请大家谅解！如果大家有什么问题和建议，欢迎大家广泛留言，我会尽量回复的，谢谢大家支持！

## 参考资料
1. [ssh 建立本地localhost与远程服务器localhost的连接](http://frankchen.xyz/2017/07/06/ssh-web-tunnel/)
2. [Nginx 官方文档](https://nginx.org/en/linux_packages.html)
3. [Hexo 官方文档](https://hexo.io/zh-tw/docs/index.html)


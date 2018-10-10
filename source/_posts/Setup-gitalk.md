---
title: Hexo next 配置 Gitalk 总结
categories: 
- 经验总结
- 个人博客
tags: [Hexo, next, Gitalk]
date: 2018-06-17 00:42:36
---
经过再三考虑，我选择使用 Gitalk 作为本博客的评论系统，但在配置过程中还是遇到了不少问题，基本大多数问题我都遇到了◢▆▅▄▃崩╰(〒皿〒)╯溃▃▄▅▇◣，感觉官方提供的文档还是不够全面，所以这篇文章希望能帮助到想要使用 Gitalk 的朋友，少走点弯路。

<!-- more -->
## 主要配置步骤
我配置主要是参考了两篇文章：

1. [官方配置文档](https://github.com/iissnan/hexo-theme-next/pull/1814/files)：这其实不算是文档，是一个为 next 主题添加原生 Gitalk 的 pull request，但按着它的修改进行相应的改动就可以了；
2. [Hexo NexT主题中集成gitalk评论系统](https://asdfv1929.github.io/2018/01/20/gitalk/)：这篇就更加像是教程了，但是我按着配置最后还是出现了不少问题，感觉该教程还是有一些地方没有说清楚。

## 遇到的问题
**1. 评论框出现 "Error: Not Found" 错误 **

![Error: Not Found 错误](/Setup-gitalk/Error.png)

出现这个问题主要是因为没有正确配置 OAuth application 和站点配置文件（_config.yml），我这里针对第二个教程里的配置提供一些补充性说明：

![OAuth application 配置图](/Setup-gitalk/appSetting.png)

主题配置文件的补充说明（这里最好用教程1）:

```
gitalk:
  enable: true
  repo: # 仓库名称，例：asdfv1929.github.io（这里注意，不是仓库地址，所以不需要加上前面的https或github.com/之类的）
  ClientID:     # 之前注册的 OAuth 界面的提供的 ID
  ClientSecret: Client Secret # 同上
  owner: # github 帐号
  admin: # 同上，但可以添加额外的管理员用户，用逗号隔开
  pagerDirection: first
```

**2. 登录出现 404 错误**

刚配置 Gitalk 后，首先出现了下面的界面：

![需要初始化](/Setup-gitalk/NotFound.png)

根据 [issue-136](https://github.com/gitalk/gitalk/issues/136) 的 keveon 回答可知，点击 Login 按钮登录一下就可以了，然后我点击后就出现了这个下面这个界面：

![404错误](/Setup-gitalk/404.png)

这个问题花了我点时间去解决，但结果其实挺让我哭笑不得的。请求授权登录时使用的 Get 请求，但我发现我的 Get 请求中查询参数 clientID 并没有被传递（一直为空），这也是导致 404 错误的主要原因。但我对照了半天的配置文件还是没发现哪里错了，后来我发现了一个问题，我是先按着第二个教程配置的，但出现了一些问题后，我去参考了第一篇文章，然后发现它们的 gitalk.swig 文件有一点不同的地方，如下图所示：

![配置文件对比](/Setup-gitalk/Comparasion.png)

发现问题了没有？箭头所指的那两个变量的开头一个大写，一个小写。这看着不起眼的不同，在编程中可是非常严重的问题，因为在传递参数的时候，js 会在主题配置文件中寻找 clientID 的值，那如果你在主题配置文件中写的 ClientID 就会出现找不到，那就一直传递的是空值。。。感觉我犯得这个错误很低级，这里指出只是想给出现 404 错误的小伙伴提个醒，参考教程也要用脑~~，不然就会像我一样。。~~

**3. 出现 Error: Validation Failed 错误**

![Error: Validation Failed 错误](/Setup-gitalk/ValidationFailed.png)

错误原因可以参考 [issue-102](https://github.com/gitalk/gitalk/issues/102)，简言之，就是 Github 添加了对 issue label 的长度限制（50个字符），而 Gitalk 会用文章的标题创建一个 label 以方便日后检索，这样过长的文章标题创建 issue 时就会出现问题。

最简单的解决方法如下，将 layout/_third-party/comments/gitalk.swig 修改为如下：

```
{% if not (theme.duoshuo and theme.duoshuo.shortname) and not theme.duoshuo_shortname %}
    {% if theme.gitalk.enable %}
        {% if page.comments %}
        <script src="https://unpkg.com/gitalk/dist/gitalk.min.js"></script>
        <script src="https://cdn.bootcss.com/blueimp-md5/2.10.0/js/md5.js"></script>
        <script type="text/javascript">
            const gitalk = new Gitalk({
            clientID: '{{theme.gitalk.clientID}}',
            clientSecret: '{{theme.gitalk.clientSecret}}',
            repo: '{{theme.gitalk.repo}}',
            owner: '{{theme.gitalk.owner}}',
            admin: '{{theme.gitalk.admin}}'.split(','),
            pagerDirection: '{{theme.gitalk.pagerDirection}}',
            id: md5(window.location.pathname),
            distractionFreeMode: false
            })
            gitalk.render('gitalk-container')
        </script>
        {% endif %}
    {% endif %}
{% endif %}
```

懂一点 js 的应该知道是将 id 字段用 md5 进行了哈希，这样就保证了长度肯定不超过限制。

至此，我的评论系统就成功搭建好了，希望这篇文章能给所有使用 hexo next 主题的博主在搭建 Gitalk 作为自己评论系统时提供一点帮助~

## 参考资料
1. [官方配置文档](https://github.com/iissnan/hexo-theme-next/pull/1814/files)
2. [Hexo NexT主题中集成gitalk评论系统](https://asdfv1929.github.io/2018/01/20/gitalk/)
3. [各种 issue 帖, issues 是好东西](https://github.com/gitalk/gitalk/issues/)


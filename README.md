# 终端翻译

# TermTrans
to translate word in terminal


> 在terminal下运行的翻译工具

## About it

## 关于
This tools is work in terminal on (U)Linux.

It's used to translate English to Chinese.

> 本工具支持在Linux及Unix（统称类UNIX系统）下的终端内运行
支持中英文互译（默认还支持其他语言翻译成中文）


## Installation
## 安装
You can downdload it from github:
> 你可以从github直接下载

`git clone https://github.com/AmazingPoint/TermTrans`

Then run the install.sh
> 然后运行install.sh (可能需要添加执行权限)

`./install.sh`

## How to use it
## 如何使用

#### Translation
#### 翻译功能
Just run it in terminal like this :
> 安装完成之后，可以直接在终端运行，如翻译 words

`trans words`

Of course, You can also translate Chinese:
> 当然，你也可以用它来翻译中文

`trans 我想吃水果`

And also, You can translate a long words like this:
> 而且，你还可以翻译一整行的英文（注意要加上引号(双引号或者单引号)）
`trans 'Why people learn computer science?'`


#### Record
#### 记录功能
By default, trans will record the word witch has been chechked. you can use command like this to show words:
> trans会默认记录下你查询过的词条，你可以使用如下命令来查看：

`trans -l`

At the last, Every tool show have a help command like this:
> 最后，每一种工具都会有类似这样一个帮助命令：

`trans -h`

使用邮箱抓取头像
===

可以使用gravatar和qq抓取用户头像，优先大图，过滤掉default的图片。

失败后自动从失败位置继续抓取。

email_list 每行一个邮件

简单用法
---

pip install requests

1. 将scrapy_avatar.py放到某文件夹下例如`/opt/projects/scripts`

2. `mkdir /opt/projects/scripts/avatar`

3. 将你的文件列表放到email_list_0.json里面

4. `python scrapy_avatar.py gravatar 0` 或者 `python scrapy_avatar.py qq 0`

简单说明
---

当email_list比较大的时候， 为了使用更多的进程你可以将email_list拆分成多个list
例如 `email_list_0.json` `email_list_1.json`
你就可以使用 `python scrapy_avatar.py gravatar 0` `python scrapy_avatar.py gravatar 1`起两个进程来抓

其他feature请阅读代码，更改里面的两个hook方法

吐槽
---

1. 因为这是一个简单的脚本，因此懒得用click做脚本参数处理，只依赖于requests, 参数判断就懒得写了.

2. 本来在`scrapy_context`那个for循环里使用的是contextmanager yield来做的，但是有个奇怪的`RuntimeError generator didn't stop`, 无奈将yield改为hook的方法.

3. qq的头像有些奇怪的问题，例如不是没人都有100大小的图，但是没人都有40大小的图, 因此优先拿大图, 在qq那边就做了一次判断.

4. 没有把context以及hook的其他方法配到脚本里面去，需要的人请自行修改.

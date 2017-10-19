## 基于Django的宙斯盾后台系统：  
功能列表：  
&#160;&#160;&#160;&#160;1：主要提供宙斯盾系统的相关api；  
&#160;&#160;&#160;&#160;2：基于Celery提供基础的异步调用功能；  

注意项：  
&#160;&#160;&#160;&#160;1：`django_celery_results`的 celery 结果存储(可以选择非默认数据库):  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160; `python manage.py migrate django_celery_results --database apollo`  

&#160;&#160;&#160;&#160;2：mysql多库配置问题，使用 database_router 来分配各应用数据库。  

&#160;&#160;&#160;&#160;3：多机器分库时，`ForeignKeyFiels：django.db.utils.IntegrityError: (1215, 'Cannot add foreign key constraint')`，  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160; python manage.py migrate 失败;  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;目前建议：将`ForeignKeyField`、`ManyToManyField`、`OneToOneField` 放在同一个数据库里(同一数据库分库或许可行)



## 基于Celery的任务调度系统  
功能列表：  
&#160;&#160;&#160;&#160;1：文本邮件或附件适量大小 (`<=1024KB`) 的邮件发送功能；  
&#160;&#160;&#160;&#160;2：定时任务功能

#### Recommendation：About the distributed protocol:   
&#160;&#160;(1)： protocol, `Raft`. So far don't have python package  
&#160;&#160;(2)： a tool, `ZooKeeper` base on `paxos` protocol(`kazoo` package to python on github) so far.


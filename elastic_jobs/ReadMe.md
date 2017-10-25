####
使用Django + Celery + RabbitMQ + Flower 需要注意的地方：  
1：参考此目录结构  
2：在Linux安装 rabbit-mq (Windows中celery库不能使用)  
3：启动`rabbit-server`服务，可在浏览器检查服务是否启动  
&#160;&#160;&#160;&#160; link: http://localhost:15672/  
4：设置`vhost`，否则无法启动 celery worker 进程  
5：启动 celery worker: `celery -A apollo worker -l info` (`apollo/目录下必须有celery.py文件`) 或者  
&#160;&#160;&#160;&#160;&#160;`celery -A elastic_jobs.celery_app worker -l info` (`elastic_jobs/celery_app/目录下必须有celery.py文件文件`)  
6：关于task的监控: `celery -A elastic_jobs.celery_app flower`  
&#160;&#160;&#160;&#160;&#160;`http://xx.xx.xx.xx:5555/`

####
目前celery的目录结构：  
`elasric_jobs`  
&#160;&#160;&#160;&#160;`celery_app`  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`__init__.py`  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`celery.py`  `# 目前的工程中必须要命名为celery.py`  
&#160;&#160;&#160;&#160;`settings.py`  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`__init__.py`  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`settings.py`  
&#160;&#160;&#160;&#160;`tasks`  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`scrapyd.py`  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`tasks.py`  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`......`  

######
注意：  
一: 在 `apollo/` 目录下使用命令:  
&#160;&#160;&#160;&#160; `celery -A elastic_jobs.celery_app worker -l info` 或者   
&#160;&#160;&#160;&#160; `celery -A apollo worker -l info`  
出现如下情况：  
&#160;&#160;&#160;&#160; --------------- celery@localhost.localdomain v4.1.0 (latentcall)  
&#160;&#160;&#160;&#160; ---- **** -----   
&#160;&#160;&#160;&#160; --- * ***  * -- Linux-3.10.0-514.16.1.el7.x86_64-x86_64-with-centos-7.3.1611-Core 2017-09-26 15:24:22  
&#160;&#160;&#160;&#160; -- * - **** ---   
&#160;&#160;&#160;&#160; - ** ---------- [config]  
&#160;&#160;&#160;&#160; - ** ---------- .> app:         celery:0x2e82c10  
&#160;&#160;&#160;&#160; - ** ---------- .> transport:   amqp://guest:**@localhost:5672//  
&#160;&#160;&#160;&#160; - ** ---------- .> results:     disabled://  
&#160;&#160;&#160;&#160; - *** --- * --- .> concurrency: 2 (prefork)  
&#160;&#160;&#160;&#160; -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)  
&#160;&#160;&#160;&#160; --- ***** -----   
&#160;&#160;&#160;&#160;  -------------- [queues]  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160; .> celery           exchange=celery(direct) key=celery  

问题：  
(1)：症结在于`celery.py`中的`app`并没有加载`settings.py`中的配置，而是使用`celery` package中默认的配置，所以会出现  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;`amqp://guest:**@localhost:5672// `=> "`guest`"用户和"`/`" vhost(实际应该是`dingxutao`和`/celery_scrapy`)  

&#160;&#160;方案：参照`elastic_jobs/celery_app/celery.py`中的详细解释。  

(2)：基于(一)的目录结构，产生一下问题：  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;`RuntimeError: maximum recursion depth exceeded while calling a Python object`  

&#160;&#160;方案：将`elastic_jobs/celery_app/celery.py` 文件与`settings.py`(即: `elastic_jobs/celery_app/settings.py`)文件放在一起  
&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;`elastic_jobs/celery_app/celery.py`文件内容参考工程  

(3)：`celery.py` 加载django配置问题:  
 &#160;&#160;`os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apollo.settings.dev")`： 





# Celery 
> Celery is an asynchronous task queue/job queue based on distributed message 
passing. It is focused on real-time operation, but supports scheduling as well.
The execution units, called tasks, are executed concurrently on a single or more worker servers using multiprocessing, Eventlet, or gevent. Tasks can execute asynchronously (in the background) or synchronously (wait until ready).


> Celery 是一个基于分布式消息传递的异步任务队列/作业队列

## 教程
[教程链接](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html "Celery Tutorial")

比较简单，大体：

1. 实例化一个应用(app)，注册任务(task)
1. 使用celery开启一个服务
1. 引入任务(from module import task)，然后执行

## Celery in guokrplus: gkapp-asynx
### 实例化应用
	# app/__init__.py
	from celery import Celery
	from flask import Flask
	# 
	app = Flask('asynx')


	def make_celery(flask_app):
    	celery = Celery(flask_app.import_name,
        	broker=flask_app.config['BROKER_URL'])
        # 其他配置
    	return celery

	with app.app_context():
		# app的相关操作 	
    	celery = make_celery(app)

### 注册服务

	# app/tasks.py
	@celery.task
	def Task(url_=None, method_='GET', **kwargs):
    	from asynx import app as flask_app
    	with flask_app.app_context():
        url = url_
        method = method_
        # guokrplus的异步队列里面大多是api url 访问
        return HttpDispatch(url, method, kwargs).dispatch()
        
### 开启celery 服务
相关的代码卸载guokrplus 的manage命令模块里面，然后绑定在manage restart/start/stop里面

	# app/asynx_manage.py
	from sh import celery_multi
	
	def start():
		celeryd_multi.start(
			'asynx-celery',
            app=app,
            loglevel=loglevel,
            logfile=logfile,
            pidfile=pidfile,
            _out=sys.stdout,
            _err=sys.stderr,
            _tty_in=True,
            _tty_out=True
        )
     # bind 'start' into 'manage start'
     ...
### 引入服务，调用
	# app/api.py
	from app.tasks import Task
    def create(self, url_, method_, countdown_):
    	‘’‘
    	一个对外暴露的接口，用于创建异步任务
    	’‘’
        from . import celery
    
        try:
            result = Task.apply_async(
                countdown=countdown_,
                args=[url_, method_],
                connection=celery.connection(),
                kwargs=params
            )           
            return {'task_id': result.id}
        except:         
            # 吞掉错误, 避免搞挂前面的应用
            return      
### 其他
* 利用app config 配置celery
* 还是得以shell命令的形式启动celery 服务
* 使用的是自己包装的HttpDispatch 对象访问api url

## Celery 文档
[文档链接](http://docs.celeryproject.org/en/latest/ "Celery 文档")  接下来就是我自己的一些尝试了

### Rabbitmq
> 
### Celery


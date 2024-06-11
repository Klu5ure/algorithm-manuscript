## Django Project

```python
pip install django

# 安装django后，可以django-admin startproject用创建项目
django-admin startproject django_news


django_news
├── django_news              // 项目全局文件目录
│   ├── __init__.py
│   ├── settings.py          // 全局配置
│   ├── urls.py              // 全局路由
│   └── wsgi.py              // WSGI服务接口（暂时不用纠结这个是神马）
└── manage.py                // 项目管理脚本

# 运行项目
python manage.py runserver
```

## Django App

Django App 一般分为三大类（根据来源）：

- **内置**：即 Django 框架自带的应用，包括 admin（后台管理）、auth（身份鉴权）、sessions（会话管理）等等
- **自定义**：即用来实现我们自身业务逻辑的应用，这里我们将创建一个新闻展示应用
- **第三方**：即社区提供的应用，数量极其丰富，功能涵盖几乎所有方面，能够大大减少开发成本

### 创建自定义app

```python
# 创建app
python manage.py startapp news

news                     // news 应用目录
├── __init__.py          // 初始化模块
├── admin.py             // 后台管理配置
├── apps.py              // 应用配置
├── migrations           // 数据库迁移文件目录
│   └── __init__.py      // 数据库迁移初始化模块
├── models.py            // 数据模型
├── tests.py             // 单元测试
└── views.py             // 视图


# 将自定义 App 添加到全局配置
# 我们在 settings.py 中将 news 应用加入 `INSTALLED_APPS` 中：
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news',
]
```

### 视图

```python
# news/views.py

from django.http import HttpResponse
def index(request):
    return HttpResponse('Hello World!')
```

### 路由

```python
# news/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
]

--------------------------------------------

# django_news/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
]

# 直接访问127.0.0.1:8000就能看到Hello World!
```

## 模板语言

```python
# 创建templates/news文件夹，里面放index.html
{% if news_list %}
  <ul>
  {% for elem in news_list %}
    <li>
      <h3>{{ elem.title }}</h3>
      <p>{{ elem.content }}</p>
    </li>
  {% endfor %}
  </ul>
{% else %}
  <p>暂无新闻</p>
{% endif %}


# news/views.py
from django.shortcuts import render
def index(request):
    context = {
        'news_list': [
            {
                "title": "图雀写作工具推出了新的版本",
                "content": "随随便便就能写出一篇好教程，真的很神奇",
            },
            {
                "title": "图雀社区正式推出快速入门系列教程",
                "content": "一杯茶的功夫，让你快速上手，绝无担忧",
            },
        ]
    }

    return render(request, 'news/index.html', context=context)
```

访问localhost:8000，内容就显示出来了

## ORM

对数据库进行操作

### 数据库与django关联

需要三步，定义模型、创建数据库迁移文件、执行迁移

```python
# 自定义数据模型
# news/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
    
# 创建迁移文件，执行完这一步，会生成这么一个文件 news/migrations/0001_initial.py
python manage.py makemigrations

# 数据库迁移，根据0001_initial.py指令在数据库中创建表
python manage.py migrate
```

做完上面这三步，如果数据库中没有post表，就会创建一张，然后与django关联

如果想要对post表做增删改查，有两种方法，一种是登录django的后台，一种是用python的视图

### django后台对表进行增删改查

```python
# 配置后台管理接口
# news/admin.py
from django.contrib import admin
from .models import Post
admin.site.register(Post)

# 登录django后台
python manage.py createsuperuser
#设置账号密码
#访问 localhost:8000/admin，输入账号密码，进入后台管理页面，可以看到我们的 news 应用和 Post 模型了，同时可以对他们进行增删改查
```

### 视图中进行增删改查

```python
from django.shortcuts import render
from .models import Post
# 简单的查询
def index(request):
    context = { 'news_list': Post.objects.all() }
    return render(request, 'news/index.html', context=context)

# 如果要提交post请求，修改settings.py，禁用掉csrf
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# 新增
my_object = MyModel(name='John', age=30)
my_object.save()


# 查询对象
#获取所有对象：
objects = MyModel.objects.all()
#获取单个对象：
my_object = MyModel.objects.get(id=1)
#过滤：
johns = MyModel.objects.filter(name='John', age=17)
objects = MyModel.objects.filter(name='test') | MyModel.objects.filter(age=17)
#排除：
not_johns = MyModel.objects.exclude(name='John')
#排序：
sorted_objects = MyModel.objects.order_by('age')


# 更新对象
my_object.age = 31
my_object.save()
# 或者
MyModel.objects.filter(id=1).update(age=31)


# 删除对象
my_object.delete()
# 或者删除查询集中的所有对象
MyModel.objects.filter(name='John').delete()

```


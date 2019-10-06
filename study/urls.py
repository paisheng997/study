"""study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
# import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about),
    path('index/', views.index),
    path('listpic/',views.listpic),
    path('newslistpic/', views.newslistpic),
    re_path('newslistpic/(\d+)', views.newslistpic),
    path('app01/', include('app01.urls')),
    re_path('details/(\d+)',views.details),
    path('ckeditor/',include('ckeditor_uploader.urls')),

    path('reqtest',views.reqtest),
    # path('register/',views.register),
    path('ajax_get/',views.ajax_get),
    path('ajax_get_data/',views.ajax_get_data),
    path('ajax_post/',views.ajax_post),
    path('ajax_post_data/',views.ajax_post_data),
    path('one_cookie/',views.one_cookie),

    #########################后台路由
    path('register/',views.Register.as_view()),
    path('login/',views.Login.as_view()),
    path('h_index/',views.Index.as_view()),
    path('yanzhengma/',views.yanzhengma),
    path('logout/',views.logout),
    path('personal/',views.personal),
    re_path('myarticles/(\d+)',views.myarticles),
    re_path('myarticle/(\d+)',views.myarticle),
]

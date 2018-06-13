"""blog_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from . import view
from .views import articleView, tagView, categoryView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('publish_article/', articleView.publish_article),
    path('delete_article/', articleView.delete_article),
    path('modify_article/', articleView.modify_article),
    path('get_articleList/', articleView.get_articleList),
    path('get_article_page/', articleView.get_article_page),  # 后台获得文章分页数据
    path('get_articleList_tag/', articleView.get_articleList_tag),
    path('get_articleContent/', articleView.get_articleContent),
    path('get_commentImage/', articleView.get_commentImage),
    path('publish_comment/', articleView.publish_comment),
    path('get_commentList/', articleView.get_commentList),
    path('add_clickCount/', articleView.add_clickCount),
    path('add_likeCount/', articleView.add_likeCount),
    path('get_tags/', tagView.get_tags),
    path('add_tag/', tagView.add_tag),
    path('edit_tag/', tagView.edit_tag),
    path('delete_tag/', tagView.delete_tag),
    path('get_category/', categoryView.get_category),
    path('add_category/', categoryView.add_category),
    path('edit_category/', categoryView.edit_category),
    path('delete_category/', categoryView.delete_category),
    path('get_tagJson/', tagView.get_tagJson),
    path('upload/', articleView.upload),
]

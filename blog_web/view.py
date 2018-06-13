from django.http import HttpResponse
import json
from blog_model.models import tag, article, category
from django.forms.models import model_to_dict
from django.db import transaction


# 发布文章
def publish_article(request):
    resp = {
        'res': True
    }
    try:
        if request.method == 'POST':
            title = request.POST['title']
            desc = request.POST['desc']
            categoryItem = request.POST['category']
            content = request.POST['content']
            tags = request.POST['tags'].split(',')  # 可以保证已存在在数据库
            categoryItem = category.objects.get(name=categoryItem)
            isDraft = request.POST['isDraft']
            with transaction.atomic():  # 事务处理
                a = article(title=title, desc=desc, content=content, category=categoryItem, isDraft=isDraft)
                a.save()
                for tagItem in tags:  # 增加多对多关系
                    a.tag.add(tag.objects.get(tag=tagItem))
                a.save()
        else:
            resp = {'res': False}
    except Exception as e:
        resp = {
            'res': False
        }
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 删除文章
def delete_article(request):
    resp = {
        'res': True
    }
    if request.method == 'POST':
        aId = request.POST['delete_article_id']
        try:
            with transaction.atomic():
                a = article.objects.get(id=aId)
                a.delete()
        except Exception as e:
            resp = {
                'res': False
            }
    return HttpResponse(json.dumps(resp), content_type="application/json")


def modify_article(request):
    resp = {
        'res': True
    }
    if request.method == 'POST':
        id = request.POST['id']
        title = request.POST['title']
        desc = request.POST['desc']
        categoryItem = request.POST['category']
        content = request.POST['content']
        tags = request.POST['tags'].split(',')  # 可以保证已存在在数据库
        categoryItem = category.objects.get(name=categoryItem)
        try:
            with transaction.atomic():  # 事务处理
                a = article.objects.get(id=id)
                a.title = title
                a.desc = desc
                a.content = content
                a.category = categoryItem
                a.tag.clear()
                for t in tags:
                    a.tag.add(tag.objects.get(tag=t))
                for tagItem in tags:  # 增加多对多关系
                    a.tag.add(tag.objects.get(tag=tagItem))
                a.save()
        except Exception as e:
            resp = {
                'res': False
            }
    else:
        resp = {'res': False}
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 获得所有标签
def get_tags(request):
    resp = {'res': True}
    tagList = []
    if request.method == 'GET':
        tagItemList = tag.objects.all()
        for tagItem in tagItemList:
            tagItem = model_to_dict(tagItem)
            tagList.append(tagItem.get('tag'))
    resp['tags'] = tagList
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 添加标签
def add_tag(request):
    resp = {'res': True}
    if request.method == 'POST':
        newTag = request.POST['newTag']
        try:
            with transaction.atomic():
                tag.objects.create(tag=newTag)
        except Exception as e:
            resp = {
                'res': False
            }
    return HttpResponse(json.dumps(resp), content_type="application/json")


def edit_tag(request):
    resp = {'res': True}
    if request.method == 'POST':
        newTag = request.POST['newTag']
        oldTag = request.POST['oldTag']
        try:
            with transaction.atomic():
                tag.objects.filter(tag=oldTag).update(tag=newTag)
        except Exception as e:
            resp = {'res': False}
    else:
        resp = {'res': False}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def delete_tag(request):
    resp = {'res': True}
    if request.method == 'POST':
        tagItem = request.POST['tag']
        try:
            with transaction.atomic():
                tag.objects.filter(tag=tagItem).delete()
        except Exception as e:
            resp = {'res': False}
    else:
        resp = {'res': False}
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 获得所有分类
def get_category(request):
    resp = {}
    categoryList = []
    if request.method == 'GET':
        categoryItemList = category.objects.all()
        for categoryItem in categoryItemList:
            categoryList.append(model_to_dict(categoryItem).get('name'))
    resp['category'] = categoryList
    return HttpResponse(json.dumps(resp), content_type="application/json")


def get_articleList(request):
    from .package.commonUtil import getLocalFromDateTime
    resp = {'articleList': []}
    articleList = []
    if request.method == 'GET':
        articleItemList = article.objects.all()
        for index, a in enumerate(articleItemList):
            categoryName = model_to_dict(a.category)['name']
            a = model_to_dict(a)
            articleList.append({
                'id': a['id'],
                'title': a['title'],
                'desc': a['desc'],
                'date_publish': getLocalFromDateTime(a['date_publish']),
                'category': categoryName,
                'index': index + 1,
                'key': index + 1,
            })
    resp['articleList'] = articleList
    return HttpResponse(json.dumps(resp), content_type="application/json")


def get_articleContent(request):
    from .package.commonUtil import getLocalFromDateTime
    resp = {}
    if request.method == 'GET':
        aId = request.GET['aId']
        articleItem = article.objects.get(id=aId)
        categoryName = model_to_dict(articleItem.category)['name']
        tags = []
        for t in articleItem.tag.all():
            tags.append(model_to_dict(t)['tag'])
        a = model_to_dict(articleItem)
        resp = {
            'id': a['id'],
            'title': a['title'],
            'desc': a['desc'],
            'content': a['content'],
            'date_publish': getLocalFromDateTime(a['date_publish']),
            'category': categoryName,
            'tags': tags
        }
    return HttpResponse(json.dumps(resp), content_type="application/json")

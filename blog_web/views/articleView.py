from django.http import HttpResponse
import json
from blog_model.models import tag, article, category, comment
from django.db import transaction
from django.forms.models import model_to_dict


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
            isDraft = False
            with transaction.atomic():  # 事务处理
                a = article(title=title, desc=desc, content=content, category=categoryItem, isDraft=isDraft)
                a.save()
                for tagItem in tags:  # 增加多对多关系
                    a.tag.add(tag.objects.get(tag=tagItem))
                a.save()
        else:
            resp = {'res': False}
    except Exception as e:
        print(e)
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


# 修改文章
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


# 获得文章内容
def get_articleContent(request):
    from ..package.commonUtil import getLocalFromDateTime
    resp = {}
    if request.method == 'GET':
        aId = request.GET['aId']
        nextItem = {'id': None, 'title': None}
        prev = {'id': None, 'title': None}
        articleItem = article.objects.get(id=aId)
        try:
            prev = model_to_dict(articleItem.get_previous_by_date_publish())
        except Exception as e:
            print("没有上一篇")
        try:
            nextItem = model_to_dict(articleItem.get_next_by_date_publish())
        except Exception as e:
            print('没有下一篇')
        print('') if nextItem['id'] is None else print(nextItem['id'])
        print('') if prev['id'] is None else print(prev['id'])

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
            'click_count': a['click_count'],
            'like_count': a['like_count'],
            'date_publish': getLocalFromDateTime(a['date_publish']),
            'category': categoryName,
            'tags': tags,
            'prev': {'id': prev['id'], 'title': prev['title']},
            'next': {'id':nextItem['id'], 'title':nextItem['title']},
        }
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 博客获得单页文章列表
def get_articleList(request):
    from django.core.paginator import Paginator
    from ..package.commonUtil import pageSize
    import time
    resp = {'articleList': [], 'loadMoreFlag': False}
    articleList = []
    if request.method == 'GET':
        page = int(request.GET['page'])
        articleItemList = article.objects.all().order_by('id')
        articleOfPage = Paginator(articleItemList, pageSize)  # 分页
        if articleOfPage.num_pages == page:
            resp['loadMoreFlag'] = True
        articleItemList = articleOfPage.page(page)
        articleList = _getArticleList(articleItemList, page, pageSize)
    resp['articleList'] = articleList
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 增加点击数
def add_clickCount(request):
    resp = {
        "res": False,
    }
    if request.method == 'POST':
        try:
            aId = request.POST['aId']
            a = article.objects.get(id=aId)
            a.click_count = a.click_count + 1
            a.save()
            resp = {
                "res": True,
                "click_count": a.click_count
            }
        except Exception as e:
            resp = {
                "res": False,
            }
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 管理后台获得文章的单页数据
def get_article_page(request):
    from django.core.paginator import Paginator
    import time
    print("start:%s" % time.time())
    resp = {
        "articleList": [],
        "total": 100,
    }
    if request.method == 'GET':
        page = request.GET['page']
        pageSize = request.GET['pageSize']
        if 'sortField' in request.GET.keys():  # 如果进行了排序
            sortField = request.GET['sortField'] if request.GET['sortField'] != 'index' else 'id'
            sortOrder = request.GET['sortOrder']
        else:
            sortField = 'id'
            sortOrder = 'ascend'
        if sortOrder == 'descend':
            articleItemList = article.objects.all().order_by("-%s" % sortField)
        else:
            articleItemList = article.objects.all().order_by(sortField)
        # 如果进行了过滤操作
        if 'category' in request.GET.keys():
            articleItemList = article.objects.filter(category=category.objects.get(name=request.GET['category']))
        resp['total'] = articleItemList.count()
        articleOfPage = Paginator(articleItemList, pageSize)  # 分页
        articleItemList = articleOfPage.page(page)
        resp["articleList"] = _getArticleList(articleItemList, page, pageSize)
        print("end:%s" % time.time())
    return HttpResponse(json.dumps(resp), content_type="application/json")


#  获得某个tag的articleList
def get_articleList_tag(request):
    from urllib import parse
    from django.core.paginator import Paginator
    from ..package.commonUtil import pageSize
    resp = {'articleList': [], 'loadMoreFlag': False}
    articleList = []
    if request.method == 'GET':
        selectTag = request.GET['tag']
        page = int(request.GET['page'])
        selectTag = parse.unquote(selectTag)
        selectTag = tag.objects.get(tag=selectTag)
        articleItemList = selectTag.article_set.all().order_by('id')
        articleOfPage = Paginator(articleItemList, pageSize)  # 分页
        if articleOfPage.num_pages == page:
            resp['loadMoreFlag'] = True
        articleItemList = articleOfPage.page(page)
        articleList = _getArticleList(articleItemList, page, pageSize)
    resp['articleList'] = articleList
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 获得评论用的随机头像
def get_commentImage(request):
    import random
    from ..package.commonUtil import imageBedUrl
    resp = {
        'imageId': 'pig-1',
        'imageUrl': 'https://raw.githubusercontent.com/xconline/images/master/pig-1.jpg',
    }
    if request.method == 'GET':
        randomNum = random.randint(1, 7)
        resp['imageId'] = 'pig-%s' % randomNum
        resp['imageUrl'] = '%s%s.jpg' % (imageBedUrl, resp['imageId'])
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 发布评论
def publish_comment(request):
    resp = {
        'res': False,
    }
    try:
        if request.method == 'POST':
            aId = request.POST['articleId']
            name = request.POST['name']
            email = request.POST['email']
            website = request.POST['website']
            commentContent = request.POST['comment']
            imageId = request.POST['imageId']
            comment.objects.create(content=commentContent, name=name, email=email, website=website, image=imageId,
                                   article=article.objects.get(id=aId))
            resp['res'] = True
    except Exception as e:
        resp['res'] = False
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 获得文章的所有评论
def get_commentList(request):
    from ..package.commonUtil import imageBedUrl, getLocalFromDateTime
    resp = {
        'res': False,
    }
    commentListResp = []
    if request.method == 'GET':
        try:
            aId = request.GET['aId']
            print(aId)
            commentList = article.objects.get(id=aId).comment_set.all().order_by('date_publish')
            for c in commentList:
                c = model_to_dict(c)
                c['image'] = '%s%s.jpg' % (imageBedUrl, c['image'])
                c['date_publish'] = getLocalFromDateTime(c['date_publish'])
                c['email'] = ''
                commentListResp.append(c)
            resp['commentList'] = commentListResp
            resp['res'] = True
        except Exception as e:
            print(e.with_traceback())
            resp['res'] = False
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 增加点赞数
def add_likeCount(request):
    resp = {
        'res': False,
    }
    if request.method == 'POST':
        try:
            aId = request.POST['aId']
            a = article.objects.get(id=aId)
            a.like_count += 1
            a.save()
            resp['res'] = True
            resp['like_count'] = a.like_count
        except:
            resp['res'] = False
    return HttpResponse(json.dumps(resp), content_type="application/json")


# 返回前台需要的article的数据结构
def _getArticleList(articleItemList, page, pageSize):
    from ..package.commonUtil import getLocalFromDateTime
    comAndAriHash = {}
    articleList = []
    com = comment.objects.select_related().all().values('article__id', 'content')
    for c in com:  # comAndAriHash :{key:articleId,value:commentContent}
        if c['article__id'] in comAndAriHash.keys():
            comAndAriHash[c['article__id']].append(c['content'])
        else:
            comAndAriHash[c['article__id']] = [c['content']]
    for index, a in enumerate(articleItemList):
        categoryName = model_to_dict(a.category)['name']
        tags = []
        for t in a.tag.all():  # 获得文章所有tag
            tags.append(model_to_dict(t)['tag'])
        a = model_to_dict(a)
        articleList.append({
            'id': a['id'],
            'title': a['title'],
            'desc': a['desc'],
            'date_publish': getLocalFromDateTime(a['date_publish']),
            'category': categoryName,
            'click_count': a['click_count'],
            'like_count': a['like_count'],
            'content': '',
            'tags': tags,
            'comment': comAndAriHash[a['id']] if a['id'] in comAndAriHash.keys() else [],
            'index': (int(page) - 1) * int(pageSize) + index + 1,
            'key': index + 1,
        })
    return articleList


from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    # professionalfile = forms.FileField()


# 保存编辑文章时保存的图片
def upload(request):
    from ..package.commonUtil import static_path, get_fileType, server
    import os
    import time
    resp = {'url': 'test'}
    if request.method == 'POST':
        # form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES.get('file', '')
        filePath = r'%s/%d.%s' % (static_path, int(time.time()), get_fileType(file.content_type))
        if os.path.exists(filePath):
            os.remove(filePath)
        with open(filePath, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        fileName = os.path.basename(filePath)
        url = 'http://%s/static/images/%s' % (server, fileName)
    return HttpResponse(url, content_type="application/text")

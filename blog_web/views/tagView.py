from django.http import HttpResponse
import json
from blog_model.models import tag, article, category
from django.db import transaction
from django.forms.models import model_to_dict


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
        tagItem = request.POST['item']
        try:
            with transaction.atomic():
                tag.objects.filter(tag=tagItem).delete()
        except Exception as e:
            resp = {'res': False}
    else:
        resp = {'res': False}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def get_tagJson(request):
    resp = {'res': True}
    tagJson = []
    if request.method == 'GET':
        try:
            tagItemList = tag.objects.all()
            for tagItem in tagItemList:
                a = tagItem.article_set.values_list('id', flat=True).order_by('id')
                tagJson.append({
                    'tag': model_to_dict(tagItem)['tag'],
                    'num': a.count(),
                    'articleId': list(a)
                })
                resp['res'] = tagJson
        except Exception as e:
            resp = {'res':False}
    return HttpResponse(json.dumps(resp), content_type="application/json")

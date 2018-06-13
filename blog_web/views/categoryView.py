from django.http import HttpResponse
import json
from blog_model.models import  category
from django.db import transaction
from django.forms.models import model_to_dict


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


# 添加标签
def add_category(request):
    res = True
    if request.method == 'POST':
        newCategory = request.POST['newCategory']
        try:
            with transaction.atomic():
                category.objects.create(name=newCategory)
        except Exception as e:
            res = False
    else:
        res = False
    resp = {'res': res}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def edit_category(request):
    res = True
    if request.method == 'POST':
        newCategory = request.POST['newCategory']
        oldCategory = request.POST['oldCategory']
        try:
            with transaction.atomic():
                category.objects.filter(name=oldCategory).update(name=newCategory)
        except Exception as e:
            res = False
    else:
        res = False
    resp = {'res': res}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def delete_category(request):
    res = True
    if request.method == 'POST':
        categoryItem = request.POST['item']
        print(categoryItem)
        try:
            with transaction.atomic():
                category.objects.filter(name=categoryItem).delete()
        except Exception as e:
            res = False
    else:
        res = False
    resp = {'res': res}
    return HttpResponse(json.dumps(resp), content_type="application/json")

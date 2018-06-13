from django.db import models
import django.utils.timezone as timezone
# Create your models here.


# 文章表
class article(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    content = models.TextField()
    click_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    is_recommend = models.BooleanField(default=False)
    date_publish = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('category', null=True, on_delete=models.SET_NULL)
    tag = models.ManyToManyField('tag')
    isDraft = models.BooleanField(default=False)

# 标签表
class tag(models.Model):
    tag = models.CharField(max_length=255,unique=True)



# 文章分类表：博客，debug记录，随笔
class category(models.Model):
    name = models.CharField(max_length=255,unique=True)


# 评论表
class comment(models.Model):
    content = models.CharField(max_length=255)
    date_publish = models.DateTimeField(default = timezone.now)
    pid = models.IntegerField(default=0)
    article = models.ForeignKey('article', models.CASCADE)
    image = models.CharField(max_length=255,default='pig-1')
    name = models.CharField(max_length=255,default='xxx')
    email = models.CharField(max_length=255, default='xxx')
    website = models.CharField(max_length=255, default='xxx')

# Generated by Django 2.0.5 on 2018-05-08 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_model', '0002_remove_blog_tag_blog_article_tag'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='blog_article',
            new_name='article',
        ),
        migrations.RenameModel(
            old_name='blog_category',
            new_name='category',
        ),
        migrations.RenameModel(
            old_name='blog_comment',
            new_name='comment',
        ),
        migrations.RenameModel(
            old_name='blog_tag',
            new_name='tag',
        ),
    ]
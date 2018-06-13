# Generated by Django 2.0.5 on 2018-05-08 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_model', '0004_tag_article_blog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='article_blog',
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(to='blog_model.tag'),
        ),
    ]

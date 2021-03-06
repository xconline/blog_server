# Generated by Django 2.0.5 on 2018-05-11 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_model', '0005_auto_20180508_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='isDraft',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='click_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='is_recommend',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-10 14:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('end', models.DateTimeField(verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='OrderData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_id', models.IntegerField(verbose_name='数据编号')),
                ('name', models.CharField(max_length=40, verbose_name='名称')),
                ('price', models.FloatField(verbose_name='价格')),
                ('comments', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_data', to='payment.Order', verbose_name='订单')),
            ],
        ),
        migrations.CreateModel(
            name='WxUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_id', models.CharField(max_length=30)),
                ('nick_name', models.CharField(max_length=30, verbose_name='昵称')),
                ('city', models.CharField(blank=True, max_length=30, null=True, verbose_name='城市')),
                ('gender', models.IntegerField(default=1, verbose_name='性别')),
                ('province', models.CharField(blank=True, max_length=20, null=True, verbose_name='省份')),
                ('avatarUrl', models.CharField(blank=True, max_length=150, null=True, verbose_name='头像URL')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='WxUser', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='wxuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='payment.WxUser', to_field='user', verbose_name='微信用户'),
        ),
        migrations.AlterUniqueTogether(
            name='orderdata',
            unique_together=set([('order', 'data_id')]),
        ),
    ]

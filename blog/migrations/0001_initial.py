# Generated by Django 3.2 on 2021-07-17 05:45

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='文章标题')),
                ('author', models.CharField(max_length=30, verbose_name='文章作者')),
                ('content', models.TextField(max_length=2000, verbose_name='文章内容')),
                ('status', models.SmallIntegerField(choices=[(0, '正常'), (1, '被删除')], default=0, verbose_name='文章状态')),
                ('user_id', models.IntegerField(verbose_name='用户id')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='修改日期')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=2000, verbose_name='评论')),
                ('status', models.SmallIntegerField(choices=[(0, '正常'), (1, '被删除')], default=0, verbose_name='评论状态')),
                ('article_id', models.IntegerField(verbose_name='文章id')),
                ('user_id', models.IntegerField(verbose_name='用户id')),
                ('username', models.CharField(max_length=30, verbose_name='用户名')),
                ('parent_comment_id', models.IntegerField(blank=True, verbose_name='父评论id')),
                ('parent_comment_username', models.CharField(blank=True, max_length=30, verbose_name='用户名')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
            ],
        ),
        migrations.CreateModel(
            name='EmailCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=128, verbose_name='邮箱')),
                ('email_code', models.CharField(max_length=12, verbose_name='邮箱验证码')),
                ('created_time', models.IntegerField(verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=1000, verbose_name='token')),
                ('user_id', models.IntegerField(verbose_name='用户id')),
                ('client', models.SmallIntegerField(choices=[(1, 'android'), (2, 'ios'), (3, 'pc')], verbose_name='客户端')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.CharField(blank=True, max_length=128, unique=True, verbose_name='邮箱')),
                ('gender', models.SmallIntegerField(choices=[(0, '男'), (1, '女'), (-1, '保密')], default=-1, verbose_name='性别')),
                ('description', models.TextField(blank=True, max_length=2000, verbose_name='个人介绍')),
                ('status', models.SmallIntegerField(choices=[(0, '正常'), (1, '被封禁'), (-1, '已注销')], default=0, verbose_name='用户状态')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    gender_types = (
        (0, '男'),
        (1, '女'),
        (-1, '保密')
    )
    status_types = (
        (0, '正常'),
        (1, '被封禁'),
        (-1, '已注销')
    )
    email = models.CharField(max_length=128, unique=True, blank=True, verbose_name='邮箱')
    # password = models.CharField(max_length=200, blank=True, verbose_name='密码')
    # name = models.CharField(max_length=30, unique=True, blank=True, verbose_name='昵称')
    gender = models.SmallIntegerField(choices=gender_types, blank=False, default=-1, verbose_name='性别')
    description = models.TextField(max_length=2000, blank=True, verbose_name='个人介绍')
    status = models.SmallIntegerField(choices=status_types, blank=False, default=0, verbose_name='用户状态')
    # created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    # modified_date = models.DateTimeField(auto_now=True, verbose_name='修改日期')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailCode(models.Model):
    email = models.CharField(max_length=128, blank=False, verbose_name='邮箱')
    email_code = models.CharField(max_length=12, blank=False, verbose_name='邮箱验证码')
    created_time = models.IntegerField(blank=False, verbose_name='创建时间')


class UserLogin(models.Model):
    client_types = (
        (1, 'android'),
        (2, 'ios'),
        (3, 'pc')
    )
    token = models.CharField(max_length=1000, blank=False, verbose_name='token')
    user_id = models.IntegerField(blank=False, verbose_name='用户id')
    client = models.SmallIntegerField(choices=client_types, blank=False, verbose_name='客户端')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')


class Article(models.Model):
    status_types = (
        (0, '正常'),
        (1, '被删除'),
    )
    title = models.CharField(max_length=100, blank=False, verbose_name='文章标题')
    author = models.CharField(max_length=30, blank=False, verbose_name='文章作者')
    content = models.TextField(max_length=2000, blank=False, verbose_name='文章内容')
    status = models.SmallIntegerField(choices=status_types, blank=False, default=0, verbose_name='文章状态')
    user_id = models.IntegerField(blank=False, verbose_name='用户id')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='修改日期')


class Comment(models.Model):
    status_types = (
        (0, '正常'),
        (1, '被删除'),
    )
    comment = models.CharField(max_length=2000, blank=False, verbose_name='评论')
    status = models.SmallIntegerField(choices=status_types, blank=False, default=0, verbose_name='评论状态')
    article_id = models.IntegerField(blank=False, verbose_name='文章id')
    user_id = models.IntegerField(blank=False, verbose_name='用户id')
    username = models.CharField(max_length=30, blank=False, verbose_name='用户名')
    parent_comment_id = models.IntegerField(blank=True, verbose_name='父评论id')
    parent_comment_username = models.CharField(max_length=30, blank=True, verbose_name='用户名')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')

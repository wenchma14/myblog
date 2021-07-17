from django.contrib import admin
from blog.models import User, Article, Comment, UserLogin, EmailCode

# Register your models here.

admin.site.register([User, Article, Comment, UserLogin, EmailCode])

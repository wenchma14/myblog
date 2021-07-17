from django.contrib import auth
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from blog.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from blog.dao import blog as blog_dao
from django.core.exceptions import ObjectDoesNotExist
from blog.business.blog import logger


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    try:
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(username=email, password=password)
        if user:
            auth.login(request, user)
            return redirect(reverse('blog:user_index', kwargs={'username': user.username}))
        error = {'msg': '错误的账户名或密码'}
        return render(request, 'login.html', error)
    except KeyError:
        error = {'msg': '格式不正确'}
        return render(request, 'register.html', error)
    except Exception as e:
        logger.error(e)
        return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    try:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error = {'msg': '两次输入密码不一致'}
            return render(request, 'register.html', error)
        user = blog_dao.get_user_by_email(email)
        if user:
            error = {'msg': '该邮箱已被注册'}
            return render(request, 'register.html', error)
        user = blog_dao.get_user_by_username(username)
        if user:
            error = {'msg': '该用户名已存在'}
            return render(request, 'register.html', error)
        blog_dao.insert_user(username, email, password2)
        return redirect(reverse('blog:user_login'))
    except KeyError:
        error = {'msg': '格式不正确'}
        return render(request, 'register.html', error)
    except Exception as e:
        logger.error(e)
        return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


def change_user_password(request):
    if request.method == 'GET':
        return render(request, 'forgot-password.html')
    try:
        email = request.POST.get('email')
        email_code = request.POST.get('email_code')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            error = {'msg': '两次输入密码不一致'}
            return render(request, 'forgot-password.html', error)
        user = blog_dao.get_user_by_email(email)
        if not user:
            error = {'msg': '用户不存在，请输入正确的邮箱'}
            return render(request, 'forgot-password.html', error)
        email_code_obj = blog_dao.get_email_code_by_email(email)
        if email_code != email_code_obj.email_code:
            error = {'msg': '验证码错误'}
            return render(request, 'forgot-password.html', error)
        blog_dao.update_user_password(user, password2)
        return redirect(reverse('blog:user_login'))
    except KeyError:
        error = {'msg': '格式不正确'}
        return render(request, 'forgot-password.html', error)
    except Exception as e:
        logger.error(e)
        return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


@login_required
def logout(request):
    try:
        auth.logout(request)
        return redirect(reverse('blog:user_login'))
    except Exception as e:
        logger.error(e)
        return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


def user_index(request, username):
    if request.method == 'GET':
        try:
            user = blog_dao.get_user_by_username(username)
            if not user:
                return render(request, '404.html', {'msg': '用户不存在'})
            user_auth = request.user
            articles = blog_dao.get_articles_by_username(username)
            return render(request, 'index.html', {'articles': articles, 'username': username, 'user': user_auth})
        except Exception as e:
            logger.error(e)
            return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


def user_about(request, username):
    if request.method == 'GET':
        try:
            user = blog_dao.get_user_by_username(username)
            if not user:
                return render(request, '404.html', {'msg': '用户不存在'})
            user_auth = request.user
            return render(request, 'about.html', {'username': user.username, 'email': user.email,
                                                  'description': user.description, 'user': user_auth})
        except Exception as e:
            logger.error(e)
            return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


def article(request, article_id):
    if request.method == 'GET':
        try:
            article_obj = blog_dao.get_article_by_id(article_id)
            comments = blog_dao.get_comments_by_article_id(article_id)
            user_auth = request.user
            return render(request, 'article.html', {'article': article_obj, 'comments': comments,
                                                    'user': user_auth})
        except ObjectDoesNotExist:
            return render(request, '404.html', {'msg': '帖子不存在'})
        except Exception as e:
            logger.error(e)
            return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


@login_required
def add_comment(request):
    if request.method == 'POST':
        try:
            username = request.user.username
            comment = request.POST.get('comment')
            article_id = int(request.POST.get('article_id'))
            parent_comment_id = int(request.POST.get('parent_comment_id'))
            user = blog_dao.get_user_by_username(username)
            parent_comment_username = ''
            if parent_comment_id != 0:
                comment_obj = blog_dao.get_comment_by_id(parent_comment_id)
                parent_comment_username = comment_obj.username
            blog_dao.insert_comment(comment, article_id, user.id, user.username,
                                    parent_comment_id, parent_comment_username)
            return redirect(reverse('blog:article', kwargs={'article_id': article_id}))
        except KeyError:
            error = {'msg': '格式不正确'}
            return render(request, 'forgot-password.html', error)
        except Exception as e:
            logger.error(e)
            return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


@login_required
def add_article(request):
    if request.method == 'GET':
        user_auth = request.user
        return render(request, 'post_blog.html', {'username': user_auth.username})
    try:
        user_auth = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        blog_dao.insert_article(title, user_auth.username, content, user_auth.id)
        return redirect(reverse('blog:user_index', kwargs={'username': user_auth.username}))
    except KeyError:
        error = {'msg': '格式不正确'}
        return render(request, 'forgot-password.html', error)
    except Exception as e:
        logger.error(e)
        return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


@login_required
def change_user_info(request):
    if request.method == 'POST':
        try:
            user_auth = request.user
            user_description = request.POST.get('description')
            blog_dao.update_user_info_by_id(user_auth.id, user_description)
            return redirect(reverse('blog:user_about', kwargs={'username': user_auth.username}))
        except ObjectDoesNotExist:
            return render(request, '404.html', {'msg': '用户不存在'})
        except KeyError:
            error = {'msg': '格式不正确'}
            return render(request, 'forgot-password.html', error)
        except Exception as e:
            logger.error(e)
            return render(request, '404.html', {'msg': '系统错误，请稍后重试'})


def contact_user(request, username):
    if request.method == 'GET':
        try:
            user = blog_dao.get_user_by_username(username)
            if not user:
                return render(request, '404.html', {'msg': '用户不存在'})
            user_auth = request.user
            return render(request, 'contact.html', {'username': user.username, 'user': user_auth})
        except Exception as e:
            logger.error(e)
            return render(request, '404.html', {'msg': '系统错误，请稍后重试'})

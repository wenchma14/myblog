from common.response_helper import *
from common.errors import *
from django.core.exceptions import ObjectDoesNotExist
from blog.models import User
from blog.dao import blog as blog_dao
from blog.business.blog import check_token, logger
import json


def get_current_user_for_api(request) -> User:
    return getattr(request, "_current_user")


def send_email_code(request):
    if request.method == 'POST':
        try:
            email = json.loads(request.body).get('email')
        except (json.JSONDecodeError, KeyError):
            return error_response(ParamsError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        try:
            mc_1min = blog_dao.get_mc_1min(email)
            if mc_1min:
                return error_response(SendCodeFrequentlyError)
            mc_1day = blog_dao.get_mc_1day(email)
            if mc_1day.count() > 10:
                return error_response(SendCodeTooFrequentlyError)
            blog_dao.send_email_code(email)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        return success_response({'message': '发送成功'})


def login_by_email_code(request):
    if request.method == 'POST':
        try:
            email = json.loads(request.body).get('email')
            email_code = json.loads(request.body).get('email_code')
        except (json.JSONDecodeError, KeyError):
            return error_response(ParamsError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        try:
            email_code_obj = blog_dao.get_email_code_by_email(email)
            if email_code != email_code_obj.email_code:
                return error_response(CodeError)
            user = blog_dao.get_user_by_email(email)
            if not user:
                blog_dao.insert_user_by_email(email)
                user = blog_dao.get_user_by_email(email)
            token = blog_dao.insert_token(user.id, 1)
        except ObjectDoesNotExist:
            return error_response(RecordNotFoundError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        return success_response({'message': '登录成功', 'token': token})


def login_by_password(request):
    if request.method == 'POST':
        try:
            email = json.loads(request.body).get('email')
            password = json.loads(request.body).get('password')
        except (json.JSONDecodeError, KeyError):
            return error_response(ParamsError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        try:
            user = blog_dao.get_user_by_email(email)
            if password == user.password:
                token = blog_dao.insert_token(user.id, 1)
                return success_response({'message': '登录成功', 'token': token})
            return error_response(PasswordError)
        except ObjectDoesNotExist:
            return error_response(RecordNotFoundError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)


@check_token
def add_article(request):
    if request.method == 'POST':
        try:
            title = json.loads(request.body).get('title')
            content = json.loads(request.body).get('content')
            user = get_current_user_for_api(request)
            blog_dao.insert_article(title, user.username, content, user.id)
        except (json.JSONDecodeError, KeyError):
            return error_response(ParamsError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        return success_response({'message': '创建文章成功'})


@check_token
def delete_article(request):
    if request.method == 'POST':
        try:
            article_id = json.loads(request.body).get('article_id')
            article = blog_dao.get_article_by_id(article_id)
            user = get_current_user_for_api(request)
            if article.user_id != user.id:
                return error_response(UserNoPermission)
            blog_dao.delete_article(article)
        except (json.JSONDecodeError, KeyError):
            return error_response(ParamsError)
        except ObjectDoesNotExist:
            return error_response(RecordNotFoundError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        return success_response({'message': '删除文章成功'})


@check_token
def get_user_articles(request):
    if request.method == 'GET':
        try:
            page = json.loads(request.body).get('page')
            limit = json.loads(request.body).get('limit')
            user = get_current_user_for_api(request)
            blogs, count = blog_dao.get_user_articles(user.id, page, limit)
        except (json.JSONDecodeError, KeyError):
            return error_response(ParamsError)
        except ObjectDoesNotExist:
            return error_response(RecordNotFoundError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        return success_response({
            'data': blogs,
            'count': count
        })


@check_token
def add_comment(request):
    if request.method == 'POST':
        try:
            comment = json.loads(request.body).get('comment')
            article_id = json.loads(request.body).get('article_id')
            parent_comment_id = json.loads(request.body).get('parent_comment_id')
            user = get_current_user_for_api(request)
            blog_dao.insert_comment(comment, article_id, user.id, parent_comment_id)
        except (json.JSONDecodeError, KeyError):
            return error_response(ParamsError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
        return success_response({'message': '评论成功'})

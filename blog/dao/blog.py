from blog.models import User, UserLogin, EmailCode, Article, Comment
import time
import datetime
import random
import jwt
from blog.business.blog import secret


def get_user_by_id(user_id: int):
    user = User.objects.get(id=user_id)
    return user


def get_user_by_email(email: str):
    user = User.objects.filter(email=email).first()
    return user


def get_user_by_username(username: str):
    user = User.objects.filter(username=username).first()
    return user


def insert_user(username: str, email: str, password: str):
    User.objects.create_user(username=username, password=password, email=email)


def insert_user_by_email(email: str, password: str = '1234'):
    username = email.split('@')[0]
    user_obj = get_user_by_username(username)
    while user_obj:
        username += str(random.randint(0, 999999))
        user_obj = get_user_by_username(username)
    User.objects.create_user(username=username, password=password, email=email)


def update_user_password(user: User, password: str):
    user.set_password(password)
    user.save()


def update_user_info_by_id(user_id: int, description: str):
    user = User.objects.get(id=user_id)
    user.description = description
    user.save()


def get_mc_1min(email: str):
    last_1min_sec = int(time.time()) - 60
    mc_1min = EmailCode.objects.filter(email__exact=email, created_time__gt=last_1min_sec).first()
    return mc_1min


def get_mc_1day(email: str):
    datetime_now = datetime.datetime.utcnow()
    everyday_0 = datetime.datetime(datetime_now.year, datetime_now.month, datetime_now.day, 0, 0, 0)
    everyday_0_time = int(everyday_0.timestamp())
    mc_1day = EmailCode.objects.filter(email__exact=email, created_time__gte=everyday_0_time)
    return mc_1day


def send_email_code(email: str):
    n = random.randint(0, 999999)
    email_code = "%06d" % n
    '''
    send_mail(
        '个人博客系统',
        '您的验证码是：' + email_code,
        'wenchma@qq.com',
        [email],
        fail_silently=False
    )
    '''
    code_time = int(time.time())
    email_code_obj = EmailCode(email=email, email_code=email_code, created_time=code_time)
    email_code_obj.save()


def get_email_code_by_email(email: str):
    email_code_obj = EmailCode.objects.filter(email=email).order_by('-id').first()
    return email_code_obj


def insert_token(user_id: int, client: int):
    payload = {'id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}
    token = str(jwt.encode(payload=payload, key=secret, algorithm='HS256'), encoding='utf-8')
    user_login_obj = UserLogin(token=token, user_id=user_id, client=client)
    user_login_obj.save()
    return token


def insert_article(title: str, author: str, content: str, user_id: int):
    article_obj = Article(title=title, author=author, content=content, user_id=user_id)
    article_obj.save()


def get_article_by_id(article_id: int):
    article = Article.objects.get(id=article_id)
    return article


def get_articles_by_username(username: str):
    articles = Article.objects.filter(author=username).exclude(status__exact=1).all()
    return articles


def delete_article(article: Article):
    article.status = 1
    article.save()


def get_user_articles(user_id: int, page: int, limit: int):
    offset = (page - 1) * limit
    query = Article.objects.filter(user_id__exact=user_id).exclude(status__exact=1)
    count = query.count()
    articles = query.order_by('-id').all()[offset:limit]
    blogs = []
    for article in articles:
        d = {'article_id': article.id, 'title': article.title, 'author': article.author,
             'content': article.content, 'created_date': article.created_date}
        blogs.append(d)
    return blogs, count


def insert_comment(comment: str, article_id: int, user_id: int, username: str,
                   parent_comment_id: int, parent_comment_username: str):
    comment_obj = Comment(comment=comment, article_id=article_id, user_id=user_id, username=username,
                          parent_comment_id=parent_comment_id, parent_comment_username=parent_comment_username)
    comment_obj.save()


def get_comments_by_article_id(article_id: int):
    comments = Comment.objects.filter(article_id__exact=article_id).exclude(status__exact=1).all()
    return comments


def get_comment_by_id(comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    return comment

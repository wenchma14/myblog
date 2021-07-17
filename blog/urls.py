from django.urls import path, re_path
from blog.apis import blog as blog_apis
from blog.views import blog as blog_views

urlpatterns = [
    path('api/send_email_code', blog_apis.send_email_code, name='send_email_code'),
    path('api/login_by_email_code', blog_apis.login_by_email_code, name='api_login_by_email_code'),
    path('api/login_by_password', blog_apis.login_by_password, name='api_login_by_password'),
    path('api/add_article', blog_apis.add_article, name='api_add_article'),
    path('api/get_user_articles', blog_apis.get_user_articles, name='api_get_user_articles'),
    path('api/add_comment', blog_apis.add_comment, name='api_add_comment'),
    path('user_login/', blog_views.login, name='user_login'),
    path('user_register/', blog_views.register, name='user_register'),
    path('user_logout', blog_views.logout, name='user_logout'),
    path('user_index/<str:username>', blog_views.user_index, name='user_index'),
    path('user_index/<str:username>/about', blog_views.user_about, name='user_about'),
    path('article/<int:article_id>', blog_views.article, name='article'),
    path('add_comment', blog_views.add_comment, name='add_comment'),
    path('add_article/', blog_views.add_article, name='add_article'),
    path('change_user_info', blog_views.change_user_info, name='change_user_info'),
    path('user_index/<str:username>/contact', blog_views.contact_user, name='contact_user'),
]

from common.response_helper import *
from common.errors import *
from blog.dao import blog as blog_dao
from functools import wraps
import jwt
from jwt import exceptions
import logging

secret = 'ad38dfr8efhqwcvg7'
logger = logging.getLogger(__name__)


def check_token(func):
    @wraps(func)
    def wrapper(request):
        token = request.META.get('HTTP_TOKEN')
        try:
            payload = jwt.decode(jwt=token, key=secret, verify=True, algorithms=['HS256'])
            user_id = payload['id']
            user = blog_dao.get_user_by_id(user_id)
            if user.status == 1:
                return error_response(UserStatusError)
            setattr(request, '_current_user', user)
            return func(request)
        except (exceptions.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
            return error_response(TokenError)
        except Exception as e:
            logger.error(e)
            return error_response(ServiceError)
    return wrapper

from common.errors import *
from django.http import JsonResponse


def success_response(data: dict):
    res_dict = {
        'code': NOError.code,
        'message': data
    }
    return JsonResponse(res_dict)


def error_response(me: MyBlogError):
    return JsonResponse(dict(me))

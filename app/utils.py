import re

from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from app.models import User, Log


def get_page_info(queryset, serializer, page, limit=10):
    """
    对queryset 进行分页
    eg: queryset = AuthUser.objects.values('id', 'name').all()
    :param queryset:
    :param page: 获取的页数
    :param page_size: 每页大小，默认为1   :return:
    :return dict
    """
    paginator = Paginator(queryset, limit)
    query_set = paginator.page(page)
    if int(page) > paginator.num_pages:
        return {}
    data = {
        'code': 0,
        'page': page,
        'data': serializer(query_set, many=True).data,
        'count': paginator.count
    }
    return data


EXCLUDE_URL = ('/login/', '/register/', '/gender_captcha/', '/find_password/'
               )


class UserLoginRequiredMiddleware(MiddlewareMixin):
    """验证用户登录中间件
    """

    def process_request(self, request):
        if request.path not in EXCLUDE_URL and not re.match(r'.*admin.*', request.path) and not re.match(r'.*captcha.*',
                                                                                                         request.path):
            user_id = request.session.get('user_id', '')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except (User.DoesNotExist, User.MultipleObjectsReturned) as e:
                    return redirect('/login/')
                request.user_login = user
            else:
                return redirect('/login/')

    pass


def log_record(user, message):
    Log.objects.create(user=user, message=message)

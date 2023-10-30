import codecs
import datetime
import sys
import os
from io import StringIO
import string
import random
import csv

import pandas as pd
from captcha.fields import CaptchaField
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.forms import forms

from app.models import *
from app.serializers import *
from app.utils import get_page_info, log_record

import json
import random
from functools import wraps
from django.db.models import Avg, Q, Sum
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate

from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail


def home(request):
    """首页"""
    return render(request, 'index.html')


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField(label='')


def login(request):
    """登录"""
    if request.method == "GET":
        form = CaptchaTestForm()
        return render(request, 'page/login-3.html', {'form': form})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        keep_login = request.POST.get('keep_login')
        form = CaptchaTestForm(request.POST)
        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():
            human = True
        else:
            human = False
        if not human:
            return JsonResponse({'code': 400, 'msg': '验证码错误'})
        user = User.objects.filter(Q(username=username) | Q(email=username) | Q(phone=username))
        if not user.exists():
            return JsonResponse({'code': 400, 'msg': '用户不存在'})
        user = user.first()
        if not check_password(password, user.password):
            return JsonResponse({'code': 400, 'msg': '密码不正确'})
        res = JsonResponse({'code': 200, 'msg': 'success'})
        request.session['user_id'] = user.id
        request.user_login = user
        if not keep_login == 'false':
            request.session.set_expiry(0)
        log_record(user, f'{user.username}在{datetime.datetime.now()}登录平台')
        return res


def register(request):
    """注册"""
    if request.method == "GET":
        return render(request, 'page/register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # area = request.POST.get('area', '')
        # captcha = request.POST.get('captcha')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        nickname = request.POST.get('nickname')
        role = request.POST.get('role')

        # cache_captcha = cache.get(email, None)
        # if not cache_captcha:
        #     return JsonResponse({'code': 400, 'msg': '验证码已过期'})
        # else:
        #     if not cache_captcha == captcha:
        #         return JsonResponse({'code': 400, 'msg': '验证码错误'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'code': 400, 'msg': '用户名已存在'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'code': 400, 'msg': '邮箱已存在'})
        if User.objects.filter(phone=phone).exists():
            return JsonResponse({'code': 400, 'msg': '电话已存在'})
        cache.delete(email, version=None)
        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            phone=phone,
            birth_date=birth_date,
            gender=gender,
            nickname=nickname,
            role=role
        )
        return JsonResponse({'code': 200, 'msg': 'success'})


def find_password(request):
    if request.method == "GET":
        return render(request, 'page/find_password.html')
    else:
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        captcha = request.POST.get('captcha')
        cache_captcha = cache.get(email, None)
        if not cache_captcha:
            return JsonResponse({'code': 400, 'msg': '验证码已过期'})
        else:
            if not cache_captcha == captcha:
                return JsonResponse({'code': 400, 'msg': '验证码错误'})
        try:
            user = User.objects.get(email=email)
        except:
            return JsonResponse({'code': 400, 'msg': '邮箱未注册'})
        user.password = make_password(new_password)
        user.save()
        return JsonResponse({'code': 200})


def user_info(request):
    user = request.user_login
    if request.method == 'GET':
        return render(request, 'page/user_info.html', locals())
    else:
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # area = request.POST.get('area', '')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        nickname = request.POST.get('nickname')
        id = request.POST.get('id')

        if User.objects.filter(username=username).exclude(id=id).exists():
            return JsonResponse({'code': 400, 'msg': '用户名已存在'})
        if User.objects.filter(email=email).exclude(id=id).exists():
            return JsonResponse({'code': 400, 'msg': '邮箱已存在'})
        if User.objects.filter(phone=phone).exclude(id=id).exists():
            return JsonResponse({'code': 400, 'msg': '电话已存在'})

        User.objects.filter(id=id).update(username=username, gender=gender, email=email,
                                          phone=phone, nickname=nickname, birth_date=birth_date,
                                          )
        if new_password:
            user.password = make_password(new_password)
            user.save()
        return JsonResponse({'code': 200})


@csrf_exempt
def upload_img(request):
    user = request.user_login
    file = request.FILES.get('file')
    user.img = file
    user.save()
    return JsonResponse({
        "code": 0,
        "msg": "",
        "data": {
            "file_src": user.img.url,

        }
    })


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def logout(request):
    user = request.user_login
    log_record(user, f'{user.username}在{datetime.datetime.now()}退出平台')
    request.session.clear()
    return JsonResponse({'code': 200})


def change_password(request):
    user = request.user_login
    if request.method == 'GET':
        return render(request, 'page/user-password.html')
    else:
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        if not check_password(old_password, user.password):
            return JsonResponse({'code': 500, 'msg': '原密码不正确'})
        else:
            user.password = make_password(new_password)
            user.save()
            return JsonResponse({'code': 200})


def user_manage(request):
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/user_table.html')
    user = User.objects.filter(is_delete=False).order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        username = eval(searchParams).get('username', '')
        if username:
            user = user.filter(username__contains=username)
    limit = request.GET.get('limit', 10)
    data = get_page_info(user, UserSerializers, page, limit)
    return JsonResponse(data)


def add_user(request):
    if request.method == 'GET':
        return render(request, 'page/user_add.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # area = request.POST.get('area', '')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        nickname = request.POST.get('nickname')
        role = request.POST.get('role')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'code': 400, 'msg': '用户名已存在'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'code': 400, 'msg': '邮箱已存在'})
        if User.objects.filter(phone=phone).exists():
            return JsonResponse({'code': 400, 'msg': '电话已存在'})
        # cache.delete(email, version=None)
        if str(role) == '2':
            if User.objects.filter(role=2).count() >= 3:
                return JsonResponse({'code': 400, 'msg': '管理员数量超出3个'})
        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            phone=phone,
            birth_date=birth_date,
            gender=gender,
            nickname=nickname,
            role=role,
        )
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_user(request):
    """删除"""
    id = request.GET.get('id')
    User.objects.filter(id=id).update(is_delete=True)
    return JsonResponse({'code': 200})


def edit_user(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        user = User.objects.get(id=id)
        return render(request, 'page/user_edit.html', {'user': user})
    else:
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # area = request.POST.get('area', '')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        nickname = request.POST.get('nickname')
        role = request.POST.get('role')
        id = request.POST.get('id')

        if User.objects.filter(username=username).exclude(id=id).exists():
            return JsonResponse({'code': 400, 'msg': '用户名已存在'})
        if User.objects.filter(email=email).exclude(id=id).exists():
            return JsonResponse({'code': 400, 'msg': '邮箱已存在'})
        if User.objects.filter(phone=phone).exclude(id=id).exists():
            return JsonResponse({'code': 400, 'msg': '电话已存在'})

        User.objects.filter(id=id).update(username=username, gender=gender, email=email,
                                          phone=phone, nickname=nickname, birth_date=birth_date,
                                          role=role)
        if new_password:
            User.objects.filter(id=id).update(password=make_password(new_password))
        return JsonResponse({'code': 200})


def api_init(request):
    user = request.user_login
    data = user.menu()
    return JsonResponse(data)


@csrf_exempt
def upload(request):
    file = request.FILES['file']
    csv_file = file.read().decode('utf-8')
    csv_data = csv.DictReader(StringIO(csv_file), delimiter=',')
    data = []
    for i in csv_data:
        data.append(i)
    if not data:
        return JsonResponse({
            'code': 1,
            'msg': '数据为空',
            'data': []
        })
    return JsonResponse({
        "code": 0
        , "msg": ""
        , "data": data
    }
    )


def welcome(request):
    all_broadcaster = Broadcaster.objects.all().count()
    all_product = Product.objects.all().count()
    all_monthly_sales = sum([i.monthly_sales for i in Product.objects.all()])
    all_live_count = LiveBroadcastInfo.objects.all().count()
    all_sales = Sales.objects.all().count()
    top_fan_count = OperatingAccount.objects.values('platform').annotate(tall_fan=Sum('fan_count')).order_by(
        '-tall_fan')[:10]
    top_fan_data = []
    top5_dx = []
    for i in top_fan_count:
        top5_dx.append(i['platform'])
        top_fan_data.append({'name': i['platform'], 'value': i['tall_fan']})

    top_p = Product.objects.values('product_name').annotate(total_v= Sum('monthly_sales')).order_by('-total_v')[:20]
    top_p_dx = []
    top_p_dy = []
    for i in top_p:
        top_p_dx.append(i['product_name'])
        top_p_dy.append(i['total_v'])

    return render(request, 'page/welcome-3.html', locals())


def log_table(request):
    """登录日志"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/log_table.html')
    predict_logs = Log.objects.order_by('id')
    limit = request.GET.get('limit', 10)
    data = get_page_info(predict_logs, LogSerializers, page, limit)
    return JsonResponse(data)


def operating_account_table(request):
    """运营账号表"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/operating_account_table.html')
    oa = OperatingAccount.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        account_number = eval(searchParams).get('account_number', '')
        if account_number:
            oa = oa.filter(account_number__contains=account_number)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, OperatingAccountSerializers, page, limit)
    return JsonResponse(data)


def add_operating_account(request):
    if request.method == 'GET':
        return render(request, 'page/operating_account_add.html', locals())
    else:
        account_number = request.POST.get('account_number')
        platform = request.POST.get('platform')
        account_homepage = request.POST.get('account_homepage')
        fan_count = request.POST.get('fan_count')
        establishment_date = request.POST.get('establishment_date')
        operator_number = request.POST.get('operator_number')
        account_content = request.POST.get('account_content')
        total_videos = request.POST.get('total_videos')
        total_views = request.POST.get('total_views')

        # 创建OperatingAccount对象并保存数据
        account = OperatingAccount.objects.create(
            account_number=account_number,
            platform=platform,
            account_homepage=account_homepage,
            fan_count=fan_count,
            establishment_date=establishment_date,
            operator_number=operator_number,
            account_content=account_content,
            total_videos=total_videos,
            total_views=total_views
        )
        return JsonResponse({'code': 200, 'msg': 'success'})


def edit_operating_account(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        oa = OperatingAccount.objects.get(id=id)
        return render(request, 'page/operating_account_edit.html', {'oa': oa})
    else:
        oa_id = request.POST.get('id')
        account_number = request.POST.get('account_number')
        platform = request.POST.get('platform')
        account_homepage = request.POST.get('account_homepage')
        fan_count = request.POST.get('fan_count')
        establishment_date = request.POST.get('establishment_date')
        operator_number = request.POST.get('operator_number')
        account_content = request.POST.get('account_content')
        total_videos = request.POST.get('total_videos')
        total_views = request.POST.get('total_views')
        OperatingAccount.objects.filter(id=oa_id).update(account_number=account_number,
                                                         platform=platform,
                                                         account_homepage=account_homepage,
                                                         fan_count=fan_count,
                                                         establishment_date=establishment_date,
                                                         operator_number=operator_number,
                                                         account_content=account_content,
                                                         total_videos=total_videos,
                                                         total_views=total_views)
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_operating_account(request):
    """删除"""
    id = request.GET.get('id')
    OperatingAccount.objects.filter(id=id).delete()
    return JsonResponse({'code': 200})


def product_table(request):
    """商品信息表"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/product_table.html')
    oa = Product.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        product_code = eval(searchParams).get('product_code', '')
        if product_code:
            oa = oa.filter(product_code__contains=product_code)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, ProductSerializers, page, limit)
    return JsonResponse(data)


def see_supplier(request):
    if request.method == 'GET':
        product_code = request.GET.get('product_code')
        oa = Supplier.objects.filter(product_code=product_code).first()
        return render(request, 'page/product_see.html', {'oa': oa})


def purchase_order_table(request):
    """采购信息表"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/purchase_order_table.html')
    oa = PurchaseOrder.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        account_number = eval(searchParams).get('account_number', '')
        if account_number:
            oa = oa.filter(order_code__contains=account_number)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, PurchaseOrderSerializers, page, limit)
    return JsonResponse(data)


def add_purchase_order(request):
    if request.method == 'GET':
        return render(request, 'page/purchase_order_add.html', locals())
    else:
        order_code = request.POST.get('order_code')
        product_code = request.POST.get('product_code')
        supplier_code = request.POST.get('supplier_code')
        quantity = request.POST.get('quantity')
        purchaser = request.POST.get('purchaser')
        warehouse = request.POST.get('warehouse')
        purchase_time = request.POST.get('purchase_time')
        arrival_time = request.POST.get('arrival_time')

        # 创建OperatingAccount对象并保存数据
        account = PurchaseOrder.objects.create(
            order_code=order_code,
            product_code=product_code,
            supplier_code=supplier_code,
            quantity=quantity,
            purchaser=purchaser,
            warehouse=warehouse,
            purchase_time=purchase_time,
            arrival_time=arrival_time,
        )
        return JsonResponse({'code': 200, 'msg': 'success'})


def edit_purchase_order(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        op = PurchaseOrder.objects.get(id=id)
        return render(request, 'page/purchase_order_edit.html', {'op': op})
    else:
        op_id = request.POST.get('id')
        order_code = request.POST.get('order_code')
        product_code = request.POST.get('product_code')
        supplier_code = request.POST.get('supplier_code')
        quantity = request.POST.get('quantity')
        purchaser = request.POST.get('purchaser')
        warehouse = request.POST.get('warehouse')
        purchase_time = request.POST.get('purchase_time')
        arrival_time = request.POST.get('arrival_time')
        PurchaseOrder.objects.filter(id=op_id).update(order_code=order_code,
                                                      product_code=product_code,
                                                      supplier_code=supplier_code,
                                                      quantity=quantity,
                                                      purchaser=purchaser,
                                                      warehouse=warehouse,
                                                      purchase_time=purchase_time,
                                                      arrival_time=arrival_time, )
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_purchase_order(request):
    """删除"""
    id = request.GET.get('id')
    PurchaseOrder.objects.filter(id=id).delete()
    return JsonResponse({'code': 200})


def stock_table(request):
    """采购信息表"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/stock_table.html')
    oa = Stock.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        a1 = eval(searchParams).get('account_number', '')
        a2 = eval(searchParams).get('account_number', '')
        if a1:
            oa = oa.filter(product_code__contains=a1)
        if a2:
            oa = oa.filter(warehouse_code__contains=a2)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, StockSerializers, page, limit)
    return JsonResponse(data)


def add_stock(request):
    if request.method == 'GET':
        return render(request, 'page/stock_add.html', locals())
    else:
        product_code = request.POST.get('product_code')
        product_name = request.POST.get('product_name')
        specification = request.POST.get('specification')
        warehouse_code = request.POST.get('warehouse_code')
        stock_quantity = request.POST.get('stock_quantity')
        warehouse_manager = request.POST.get('warehouse_manager')

        # Stock
        account = Stock.objects.create(
            product_code=product_code,
            product_name=product_name,
            specification=specification,
            warehouse_code=warehouse_code,
            stock_quantity=stock_quantity,
            warehouse_manager=warehouse_manager
        )
        return JsonResponse({'code': 200, 'msg': 'success'})


def edit_stock(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        stock = Stock.objects.get(id=id)
        return render(request, 'page/stock_edit.html', {'stock': stock})
    else:
        op_id = request.POST.get('id')
        product_code = request.POST.get('product_code')
        product_name = request.POST.get('product_name')
        specification = request.POST.get('specification')
        warehouse_code = request.POST.get('warehouse_code')
        stock_quantity = request.POST.get('stock_quantity')
        warehouse_manager = request.POST.get('warehouse_manager')

        Stock.objects.filter(id=op_id).update(product_code=product_code,
                                              product_name=product_name,
                                              specification=specification,
                                              warehouse_code=warehouse_code,
                                              stock_quantity=stock_quantity,
                                              warehouse_manager=warehouse_manager)
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_stock(request):
    """删除"""
    id = request.GET.get('id')
    Stock.objects.filter(id=id).delete()
    return JsonResponse({'code': 200})


def broadcaster_table(request):
    """主播信息"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/broadcaster_table.html')
    oa = Broadcaster.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        a1 = eval(searchParams).get('account_number', '')
        if a1:
            oa = oa.filter(broadcaster_code__contains=a1)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, BroadcasterSerializers, page, limit)
    return JsonResponse(data)


def add_broadcaster(request):
    if request.method == 'GET':
        return render(request, 'page/broadcaster_add.html', locals())
    else:
        broadcaster_code = request.POST.get('broadcaster_code')
        broadcaster_name = request.POST.get('broadcaster_name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        signed_platform = request.POST.get('signed_platform')
        operating_company = request.POST.get('operating_company')
        personal_homepage = request.POST.get('personal_homepage')
        expertise = request.POST.get('expertise')

        broadcaster = Broadcaster(
            broadcaster_code=broadcaster_code,
            broadcaster_name=broadcaster_name,
            gender=gender,
            age=age,
            signed_platform=signed_platform,
            operating_company=operating_company,
            personal_homepage=personal_homepage,
            expertise=expertise
        )

        broadcaster.save()

        return JsonResponse({'code': 200, 'msg': 'success'})


def edit_broadcaster(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        broadcaster = Broadcaster.objects.get(id=id)
        return render(request, 'page/broadcaster_edit.html', {'broadcaster': broadcaster})
    else:
        op_id = request.POST.get('id')
        broadcaster_code = request.POST.get('broadcaster_code')
        broadcaster_name = request.POST.get('broadcaster_name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        signed_platform = request.POST.get('signed_platform')
        operating_company = request.POST.get('operating_company')
        personal_homepage = request.POST.get('personal_homepage')
        expertise = request.POST.get('expertise')

        Broadcaster.objects.filter(id=op_id).update(broadcaster_code=broadcaster_code,
                                                    broadcaster_name=broadcaster_name,
                                                    gender=gender,
                                                    age=age,
                                                    signed_platform=signed_platform,
                                                    operating_company=operating_company,
                                                    personal_homepage=personal_homepage,
                                                    expertise=expertise)
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_broadcaster(request):
    """删除"""
    id = request.GET.get('id')
    Broadcaster.objects.filter(id=id).delete()
    return JsonResponse({'code': 200})


def live_broadcaster_table(request):
    """主播排期"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/live_broadcaster_table.html')
    oa = LiveBroadcast.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        a1 = eval(searchParams).get('account_number', '')
        if a1:
            oa = oa.filter(broadcaster_code__contains=a1)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, LiveBroadcastSerializers, page, limit)
    return JsonResponse(data)


def add_live_broadcaster(request):
    if request.method == 'GET':
        return render(request, 'page/live_broadcaster_add.html', locals())
    else:
        broadcaster_code = request.POST.get('broadcaster_code')
        broadcast_code = request.POST.get('broadcast_code')
        broadcast_time = request.POST.get('broadcast_time')
        working_minutes = request.POST.get('working_minutes')
        product_code = request.POST.get('product_code')
        product_order = request.POST.get('product_order')

        live_broadcast = LiveBroadcast(
            broadcaster_code=broadcaster_code,
            broadcast_code=broadcast_code,
            broadcast_time=broadcast_time,
            working_minutes=working_minutes,
            product_code=product_code,
            product_order=product_order
        )

        live_broadcast.save()

        return JsonResponse({'code': 200, 'msg': 'success'})


def edit_live_broadcaster(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        live_broadcaster = LiveBroadcast.objects.get(id=id)
        return render(request, 'page/live_broadcaster_edit.html', {'live_broadcast': live_broadcaster})
    else:
        op_id = request.POST.get('id')
        broadcaster_code = request.POST.get('broadcaster_code')
        broadcast_code = request.POST.get('broadcast_code')
        broadcast_time = request.POST.get('broadcast_time')
        working_minutes = request.POST.get('working_minutes')
        product_code = request.POST.get('product_code')
        product_order = request.POST.get('product_order')

        LiveBroadcast.objects.filter(id=op_id).update(broadcaster_code=broadcaster_code,
                                                      broadcast_code=broadcast_code,
                                                      broadcast_time=broadcast_time,
                                                      working_minutes=working_minutes,
                                                      product_code=product_code,
                                                      product_order=product_order)
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_live_broadcaster(request):
    """删除"""
    id = request.GET.get('id')
    LiveBroadcast.objects.filter(id=id).delete()
    return JsonResponse({'code': 200})


def broadcaster_pf_table(request):
    """主播绩效"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/broadcaster_pf_table.html')
    oa = BroadcastPerformance.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        a1 = eval(searchParams).get('account_number', '')
        if a1:
            oa = oa.filter(broadcaster_code__contains=a1)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, BroadcastPerformanceSerializers, page, limit)
    return JsonResponse(data)


def add_broadcaster_pf(request):
    if request.method == 'GET':
        return render(request, 'page/broadcaster_pf_add.html', locals())
    else:
        broadcaster_code = request.POST.get('broadcaster_code')
        monthly_broadcasts = request.POST.get('monthly_broadcasts')
        monthly_featured_products = request.POST.get('monthly_featured_products')
        revenue = request.POST.get('revenue')
        tips_income = request.POST.get('tips_income')
        standard_salary = request.POST.get('standard_salary')
        reward_weight = request.POST.get('reward_weight')

        broadcast_performance = BroadcastPerformance(
            broadcaster_code=broadcaster_code,
            monthly_broadcasts=monthly_broadcasts,
            monthly_featured_products=monthly_featured_products,
            revenue=revenue,
            tips_income=tips_income,
            standard_salary=standard_salary,
            reward_weight=reward_weight
        )

        broadcast_performance.save()

        return JsonResponse({'code': 200, 'msg': 'success'})


def edit_broadcaster_pf(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        instance = BroadcastPerformance.objects.get(id=id)
        return render(request, 'page/broadcaster_pf_edit.html', {'instance': instance})
    else:
        op_id = request.POST.get('id')
        broadcaster_code = request.POST.get('broadcaster_code')
        monthly_broadcasts = request.POST.get('monthly_broadcasts')
        monthly_featured_products = request.POST.get('monthly_featured_products')
        revenue = request.POST.get('revenue')
        tips_income = request.POST.get('tips_income')
        standard_salary = request.POST.get('standard_salary')
        reward_weight = request.POST.get('reward_weight')

        BroadcastPerformance.objects.filter(id=op_id).update(broadcaster_code=broadcaster_code,
                                                             monthly_broadcasts=monthly_broadcasts,
                                                             monthly_featured_products=monthly_featured_products,
                                                             revenue=revenue,
                                                             tips_income=tips_income,
                                                             standard_salary=standard_salary,
                                                             reward_weight=reward_weight)
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_broadcaster_pf(request):
    """删除"""
    id = request.GET.get('id')
    BroadcastPerformance.objects.filter(id=id).delete()
    return JsonResponse({'code': 200})


def live_broadcaster_pl_table(request):
    """直播计划"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/live_broadcaster_pl_table.html')
    oa = LiveBroadcastPlan.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        a1 = eval(searchParams).get('account_number', '')
        if a1:
            oa = oa.filter(broadcast_code__contains=a1)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, LiveBroadcastPlanSerializers, page, limit)
    return JsonResponse(data)


def add_live_broadcaster_pl(request):
    if request.method == 'GET':
        return render(request, 'page/live_broadcaster_pl_add.html', locals())
    else:
        broadcast_code = request.POST.get('broadcast_code')
        broadcast_name = request.POST.get('broadcast_name')
        broadcast_platform = request.POST.get('broadcast_platform')
        broadcast_link = request.POST.get('broadcast_link')
        broadcast_description = request.POST.get('broadcast_description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        live_broadcast_plan = LiveBroadcastPlan(
            broadcast_code=broadcast_code,
            broadcast_name=broadcast_name,
            broadcast_platform=broadcast_platform,
            broadcast_link=broadcast_link,
            broadcast_description=broadcast_description,
            start_time=start_time,
            end_time=end_time
        )

        live_broadcast_plan.save()

        return JsonResponse({'code': 200, 'msg': 'success'})


def edit_live_broadcaster_pl(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        instance = LiveBroadcastPlan.objects.get(id=id)
        return render(request, 'page/live_broadcaster_pl_edit.html', {'instance': instance})
    else:
        op_id = request.POST.get('id')
        broadcast_code = request.POST.get('broadcast_code')
        broadcast_name = request.POST.get('broadcast_name')
        broadcast_platform = request.POST.get('broadcast_platform')
        broadcast_link = request.POST.get('broadcast_link')
        broadcast_description = request.POST.get('broadcast_description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        LiveBroadcastPlan.objects.filter(id=op_id).update(broadcast_code=broadcast_code,
                                                          broadcast_name=broadcast_name,
                                                          broadcast_platform=broadcast_platform,
                                                          broadcast_link=broadcast_link,
                                                          broadcast_description=broadcast_description,
                                                          start_time=start_time,
                                                          end_time=end_time)
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_live_broadcaster_pl(request):
    """删除"""
    id = request.GET.get('id')
    LiveBroadcastPlan.objects.filter(id=id).delete()
    return JsonResponse({'code': 200})


def after_sales_table(request):
    """售后"""
    page = request.GET.get('page')
    if not page:
        return render(request, 'page/after_sales_table.html')
    oa = AfterSales.objects.order_by('id')
    searchParams = request.GET.get('searchParams', '')
    if searchParams:
        a1 = eval(searchParams).get('account_number', '')
        if a1:
            oa = oa.filter(after_sales_code__contains=a1)
    limit = request.GET.get('limit', 10)
    data = get_page_info(oa, AfterSalesSerializers, page, limit)
    return JsonResponse(data)


def add_after_sales(request):
    if request.method == 'GET':
        return render(request, 'page/after_sales_add.html', locals())
    else:
        after_sales_code = request.POST.get('after_sales_code')
        sales_code = request.POST.get('sales_code')
        user_account = request.POST.get('user_account')
        phone_number = request.POST.get('phone_number')
        after_sales_type = request.POST.get('after_sales_type')
        reason = request.POST.get('reason')
        initiation_time = request.POST.get('initiation_time')
        status = request.POST.get('status')

        after_sales = AfterSales(
            after_sales_code=after_sales_code,
            sales_code=sales_code,
            user_account=user_account,
            phone_number=phone_number,
            after_sales_type=after_sales_type,
            reason=reason,
            initiation_time=initiation_time,
            status=status
        )

        after_sales.save()

        return JsonResponse({'code': 200, 'msg': 'success'})


def edit_after_sales(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        instance = AfterSales.objects.get(id=id)
        return render(request, 'page/after_sales_edit.html', {'instance': instance})
    else:
        op_id = request.POST.get('id')
        after_sales_code = request.POST.get('after_sales_code')
        sales_code = request.POST.get('sales_code')
        user_account = request.POST.get('user_account')
        phone_number = request.POST.get('phone_number')
        after_sales_type = request.POST.get('after_sales_type')
        reason = request.POST.get('reason')
        initiation_time = request.POST.get('initiation_time')
        status = request.POST.get('status')

        AfterSales.objects.filter(id=op_id).update(after_sales_code=after_sales_code,
                                                   sales_code=sales_code,
                                                   user_account=user_account,
                                                   phone_number=phone_number,
                                                   after_sales_type=after_sales_type,
                                                   reason=reason,
                                                   initiation_time=initiation_time,
                                                   status=status)
        return JsonResponse({'code': 200, 'msg': 'success'})


def del_after_sales(request):
    """删除"""
    id = request.GET.get('id')
    LiveBroadcastPlan.objects.filter(id=id).delete()
    return JsonResponse({'code': 200})


def review(request):
    """
    直播复盘页面
    :param request:
    :return:
    """
    broadcast_code = request.GET.get('broadcast_code')
    if broadcast_code:
        instance = LiveBroadcastInfo.objects.filter(broadcast_code=broadcast_code).first()
        sales = Sales.objects.filter(broadcast_code=broadcast_code).first()
        if not sales:
            sales = Sales.objects.order_by('?').first()
    else:
        instance = LiveBroadcastInfo.objects.last()
        sales = Sales.objects.last()

    # 实时人数top5
    top_5_data_ = LiveBroadcastInfo.objects.values('broadcast_name').annotate(
        total_live_viewers=Sum('live_viewers')).order_by('-total_live_viewers')[:5]
    top5_dx = []
    top_5_pie = []
    for i in top_5_data_:
        key = i['broadcast_name']
        val = i['total_live_viewers']
        top5_dx.append(key)
        top_5_pie.append({'name': key, 'value': val})

    # 热销商品top10
    top_sales_ = Sales.objects.values('product_code', 'quantity').order_by('-quantity')[:10]
    top_sales_x = []
    top_sales_y = []
    for i in top_sales_:
        top_sales_x.append(i['product_code'])
        top_sales_y.append(i['quantity'])
    live_set = LiveBroadcastInfo.objects.order_by('-record_time')[:8]
    dx_name = ['实时人数', '粉丝平均停留时间', '功能点击数', '打赏金额', '互动数']
    d_time = []
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    for i in live_set:
        d_time.append(i.record_time.strftime("%Y-%m-%d %H:%M:%S"))
        x1.append(i.live_viewers)
        x2.append(i.average_fan_duration)
        x3.append(i.click_count)
        x4.append(float(i.tips_amount))
        x5.append(i.interaction_count)
    return render(request, 'page/review.html', locals())


def kanban(request):
    lbpls = LiveBroadcastPlan.objects.values().order_by('-start_time')[:10]
    for i in lbpls:
        broadcast_code = i['broadcast_code']
        lvi_set = LiveBroadcastInfo.objects.filter(broadcast_code=broadcast_code)
        lvi_obj = lvi_set.first() if lvi_set.exists() else LiveBroadcastInfo.objects.order_by('?').first()
        i['live_viewers'] = lvi_obj.live_viewers
        i['tips_amount'] = lvi_obj.tips_amount
        i['click_count'] = lvi_obj.click_count

    return render(request, 'page/kanban.html', locals())


def kanban_tu(request):
    dx_name = ['实时人数', '粉丝平均停留时间', '功能点击数', '打赏金额', '互动数']
    d_time = []
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    x5 = []
    s = random.randint(1, 15)
    e = random.randint(15, 30)

    live_set = LiveBroadcastInfo.objects.order_by('-record_time')[s:e]
    for i in live_set:
        d_time.append(i.record_time.strftime("%Y-%m-%d %H:%M:%S"))
        x1.append(i.live_viewers)
        x2.append(i.average_fan_duration)
        x3.append(i.click_count)
        x4.append(float(i.tips_amount))
        x5.append(i.interaction_count)
    return render(request, 'page/kanban_tu.html', locals())
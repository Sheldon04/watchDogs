# -*- coding: utf-8 -*-
# Create your views here.
import datetime
import json
import os
import time

import cv2
from django.contrib import auth
from django.core import serializers
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse

from django.contrib.auth.models import User
from django.urls import path

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from datamodel import models
from datamodel.models import invationRecord, WhiteList, mypicture
from monitor.motion_detect_MOG2 import Detector
from django.views.decorators.http import require_http_methods

#日期转码
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

#登陆
@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def login(request):
    """登录"""
    result = True
    errorInfo = u''
    detail = {}
    data = request.data
    username = data.get('username')
    password = data.get('password')
    is_superuser = data.get('is_superuser')

    # 调用django进行用户认证
    # 验证成功 user返回<class 'django.contrib.auth.models.User'>
    # 验证失败 user返回None
    user = auth.authenticate(username=username, password=password)
    print("user", user)
    if user == None:
        result = False
        errorInfo = u'用户名或密码错误'
        return Response({"result": result, "detail": detail, "errorInfo": errorInfo})

    if user.is_superuser == False and is_superuser == '1':
        result = False
        errorInfo = u'权限不足'
        return Response({"result": result, "detail": detail, "errorInfo": errorInfo})
    # 用户名和密码验证成功
    # 获取用户的token 如果没有token ，表示时用户首次登录，则进行创建，并且返回token
    try:
        tokenObj = Token.objects.get(user_id=user.id)
    except Exception as e:
        # token 不存在 说明是首次登录
        tokenObj = Token.objects.create(user=user)
    # 获取token字符串
    token = tokenObj.key
    user.last_login = datetime.datetime.now()
    return Response({"result": result, "detail": {'token': token}, "errorInfo": errorInfo})

#获取所有用户信息
@api_view(['GET'])
def get_all_users(request):
    userList = User.objects.values("id", "username", "email", "is_superuser", "last_login", "first_name", "last_name")
    response_data = json.dumps(list(userList.values("id", "username", "email", "is_superuser", "last_login", "first_name", "last_name")),
                               cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

#删除用户
@api_view(['POST'])
def user_delete(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    User.objects.filter(id=id).delete()

    if(User.objects.filter(id=id).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#编辑用户
@api_view(['POST'])
def user_update(request):
    detail = {}
    error_info=''
    id = request.POST.get("id")
    username = request.POST.get('username')
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    if(User.objects.filter(id=id).update(username=username, email=email, first_name=first_name, last_name=last_name)):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '编辑失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#增加用户
@api_view(['POST'])
def user_reg(request):
    id = request.POST.get("id")

def gen(d):
    while True:
        for frame, _, _, _ in d.run():
            time.sleep(.1)
            cv2.imwrite('./1.jpg', frame)
            flag, buffer = cv2.imencode('.jpg', frame)
            if not flag:
                continue
            print('send video')
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n')

#处理过后视频推流
@api_view(['GET'])
def send_video(request):
    d = Detector(1)
    return StreamingHttpResponse(gen(d), content_type="multipart/x-mixed-replace; boundary=frame")

#视频回放调取视频
@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes(())
def get_video(request):
    date = request.GET.get('date')
    time = request.GET.get('time')
    time = time.split(':')
    filepath = date + '-' + time[0] + '-' + time[1] + '-' + time[2]
    filepath = './monitor/video/' + filepath + '.avi'
    return StreamingHttpResponse(file_iterator(filepath), content_type="multipart/x-mixed-replace; boundary=frame")


#人脸接受保存
@api_view(['POST'])
#@permission_classes((AllowAny,))
def upload_face(request):
    img = request.FILES.get('face')
    phone = request.POST.get('phone')
    #phone = '222'
    print(phone)
    print(img)
    img_model = models.mypicture(
        photo=img,  # 拿到图片路径
        phone=phone # 拿到图片对应手机号
    )
    img_model.save()  # 保存图片
    print(img_model.photo.name)
    return HttpResponse('media/' + img_model.photo.name)

@api_view(['POST'])
#@permission_classes((AllowAny,))
def get_face(request):
    phone = request.POST.get('phone_number')
    #phone = '222'
    print(phone)
    qset = mypicture.objects.filter(phone=phone)
    print(qset.count())
    mypic = qset.first()
    return HttpResponse('media/' + mypic.photo.name)

@api_view(['POST'])
#@permission_classes((AllowAny,))
def update_face(request):
    phone = request.POST.get('phone_number')
    img = request.FILES.get('face')
    #phone = '222'
    print(phone)
    try:
        old = mypicture.objects.filter(phone=phone).first()
        del_path = './media/' + old.photo.name
        os.remove(del_path)
    except:
        print('delete failed')
    print(del_path)
    mypicture.objects.filter(phone=phone).delete()
    img_model = models.mypicture(
        photo=img,  # 拿到图片路径
        phone=phone # 拿到图片对应手机号
    )
    img_model.save()  # 保存图片
    return HttpResponse('media/' + img_model.photo.name)

@api_view(['POST'])
#获取某一天某段时间内的入侵记录
def get_specific_invation_records(request):
    date_choose_str= request.POST.get('date')
    time_span_str=request.POST.get('time_span')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")
    time_str_list=time_span_str.split(',')
    time_from_str=time_str_list[0]
    time_to_str=time_str_list[1]
    time_from=datetime.datetime.strptime(time_from_str,'%H:%M:%S')
    time_to = datetime.datetime.strptime(time_to_str, '%H:%M:%S')


    invation_list1 = invationRecord.objects.filter(date__range=(date_choose, date_choose))
    invation_list = invation_list1.filter(time__range=(time_from,time_to)).values("date", "time", "level", "camera_id", 'area', 'invation_num')

    response_data =json.dumps(
        list(invation_list.values("date", "time", "level", "camera_id", 'area', 'invation_num')), cls=DateEncoder)
    return JsonResponse(json.loads(response_data), safe=False)

@api_view(['GET'])
#获得全部入侵记录
def get_invation_records(request):

    recordList = invationRecord.objects.values("date", "time", "level", "camera_id",'area','invation_num')
    response_data = json.dumps(list(recordList.values("date", "time", "level", "camera_id",'area','invation_num')), cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)


@api_view(['POST'])
#获取一个月的入侵记录
#request: Year-month
#return [{'day1':count1},{'day2':count2},...]
#url:'api/invationrecord/getmonth'
def get_month_records(request):
    month_choose_str = request.POST.get('month')
    month_choose = datetime.datetime.strptime(month_choose_str,'%Y-%m')
    invation_m_list1 = invationRecord.objects.filter(date__year=month_choose.year)
    invation_m_list =invation_m_list1.filter(date__month=month_choose.month)
    invation_list=[]
    dict = {}
    for i in range(1,31):
        invation_d_list =invation_m_list.filter(date__day=i)
        if invation_d_list.count() !=0:
            # dict={i:invation_d_list.count()}
            dict[i] = invation_d_list.count()
            invation_list.append(dict)

    response_data =json.dumps(list(invation_list),cls=DateEncoder,indent= 4)
    return Response(dict)

def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    camera = cv2.VideoCapture(file_name)
    if camera.isOpened():
        while True:
            ret, frame = camera.read()
            if not ret:
                break
            flag, buffer = cv2.imencode('.jpg', frame)
            if not flag:
                continue
            # print('send video')
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n')


#白名单
#增
@api_view(['POST'])
def whitelist_add(request):
    result = True
    detail = {}
    error_info=''

    name = request.POST.get('name')
    level = request.POST.get('level')
    phone_number = request.POST.get('phone_number')
    time_span_str = request.POST.get('time_span')
    time_str_list = time_span_str.split(',')
    time_start_str = time_str_list[0]
    time_end_str = time_str_list[1]

    whitelist = WhiteList.objects
    if whitelist.filter(name__exact=name).count()!=0:
        print('name')
        result = False
        error_info='名称重复'
    elif name =='' or level =='' or phone_number =='' or time_start_str =='' or time_end_str =='':
        print('empty')
        result =False
        error_info = '所填项不能为空'
    elif not phone_number.isdigit():
        print('phone')
        result = False
        error_info = '手机号码格式错误'
    else:
        print('sucsuc')
        time_start = datetime.datetime.strptime(time_start_str, '%H:%M:%S')
        time_end = datetime.datetime.strptime(time_end_str, '%H:%M:%S')
        whitelist.create(name=name,level=level,phone_number=phone_number,time_start=time_start,time_end=time_end)


    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

@api_view(['POST'])
#获取某一天某段时间内的入侵记录
def get_specific_invation_time(request):
    date_choose_str= request.POST.get('date')

    date_choose =datetime.datetime.strptime(date_choose_str,"%Y-%m-%d")

    invation_list1 = invationRecord.objects.filter(date__range=(date_choose, date_choose))
    invation_list = list(invation_list1.values("time"))
    print(invation_list)

    # response_data =json.dumps(
    #     list(invation_list.values("date", "time", "level", "camera_id", 'area', 'invation_num')), cls=DateEncoder)
    return Response(invation_list)

@api_view(['GET'])
#返回所有白名单信息
def whitelist_all(request):
    recordList = WhiteList.objects.values('name','level','phone_number','time_start','time_end')
    response_data = json.dumps(list(recordList.values('name','level','phone_number','time_start','time_end')),
                               cls=DateEncoder)

    return JsonResponse(json.loads(response_data), safe=False)

#白名单
#编辑
@api_view(['POST'])
def whitelist_edit(request):
    result = True
    detail = {}
    error_info=''

    name = request.POST.get('name')
    level = request.POST.get('level')
    phone_number = request.POST.get('phone_number')
    time_span_str = request.POST.get('time_span')
    time_str_list = time_span_str.split(',')
    time_start_str = time_str_list[0]
    time_end_str = time_str_list[1]

    whitelist = WhiteList.objects
    if name =='' or level =='' or phone_number =='' or time_start_str =='' or time_end_str =='':
        print('empty')
        result =False
        error_info = '所填项不能为空'
    else:
        print('sucsuc')
        time_start = datetime.datetime.strptime(time_start_str, '%H:%M:%S')
        time_end = datetime.datetime.strptime(time_end_str, '%H:%M:%S')
        whitelist.filter(phone_number=phone_number).update(name=name,level=level,phone_number=phone_number,time_start=time_start,time_end=time_end)


    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

#白名单
#删除
@api_view(['POST'])
def whitelist_delete(request):
    detail = {}
    error_info=''
    whitelist = WhiteList.objects
    phone_number = request.POST.get('phone_number')
    if(whitelist.filter(phone_number=phone_number).delete()):
        print("success")
        result = True
    else:
        print('delede failed')
        result = False
        error_info = '删除失败'

    return JsonResponse({'result':result,'detail':detail,'errorInfo':error_info})

# -*- coding: utf-8 -*-
# Create your views here.
import datetime
import json
import time

import cv2
from django.contrib import auth
from django.core import serializers
from django.http import StreamingHttpResponse, JsonResponse

from django.contrib.auth.models import User

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from monitor.motion_detect_MOG2 import Detector
from django.views.decorators.http import require_http_methods

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

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
    print("user",user)
    if user == None:
        result = False
        errorInfo = u'用户名或密码错误'
        return Response({"result": result, "detail": detail, "errorInfo": errorInfo})

    if user.is_superuser == False and is_superuser == '0':
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
    return Response({"result": result, "detail": {'token': token}, "errorInfo": errorInfo})

def gen(d):
    while True:
        for frame, _, _, _ in d.run():
            time.sleep(.1)
            cv2.imwrite('./1.jpg', frame)
            flag, buffer = cv2.imencode('.jpg', frame)
            if not flag:
                continue
            print('send video')
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')

@api_view(['GET'])
@permission_classes((AllowAny,))
def send_video(request):
    d = Detector(1)
    return StreamingHttpResponse(gen(d), content_type="multipart/x-mixed-replace; boundary=frame")

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_all_users(request):
    userList = User.objects.values("username", "email", "is_superuser", "last_login")
    print(userList)
    response_data = json.dumps(list(userList.values("username", "email", "is_superuser", "last_login")), cls=DateEncoder)
    print(response_data)
    return JsonResponse(json.loads(response_data),safe=False)

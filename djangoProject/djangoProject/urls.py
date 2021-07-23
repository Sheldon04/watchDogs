"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from djangoProject import view, settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/video', view.send_video), #视频监控地址
    path('api/user/login', view.login), #登陆
    path('api/admin/getall', view.get_all_users), #获取所有用户信息
    path('api/admin/uploadface', view.upload_face), #上传人脸照片
    path('api/user/attacklistuser/all', view.get_specific_records), #所有入侵记录
    path('api/user/attacklistuser', view.get_specific_records) #指定时间入侵记录
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

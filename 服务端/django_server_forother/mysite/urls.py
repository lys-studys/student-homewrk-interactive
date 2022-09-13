"""mysite URL Configuration

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
#from django.conf.urls import url 
#from tutorials import views 
 
#urlpatterns = [ 
#    url(r'^api/tutorials$', views.tutorial_list),
#    url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
#    url(r'^api/tutorials/published$', views.tutorial_list_published)
#]


from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="接口文档平台",
        default_version="v1",
        decription="文档描述",
        terms_of_service="",
        contact=openapi.Contact(email="mhhcode@mhhcode.com"),
        license=openapi.License(name="BSD LICENSE")
        ),
    public=True,
)

#from rest_framework import routers  # 路由配置模块
#from API import views   # 视图模块
# 导入辅助函数get_schema_view
#from rest_framework.schemas import get_schema_view
# 导入两个类
#from rest_framework_swagger.renderers import SwaggerUIRenderer,OpenAPIRenderer

#router = routers.DefaultRouter()    # 创建路由对象
#router.register(r'users',views.UserViewSet) # 调用register方法，配置Users的路由
#router.register(r'groups',views.GroupViewSet)   # 配置Groups路由配置模块

#schema_view = get_schema_view(title='API',renderer_classes=[SwaggerUIRenderer,OpenAPIRenderer])


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('admin/', admin.site.urls),
    url(r'^', include('tutorials.urls')),
    url(r'^docs/',include_docs_urls(title="My API Title")),   # 配置docs的url路径
    path("swagger", schema_view.with_ui("swagger",cache_timeout=0), name="schema-swagger"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema_redoc"),

#    path('docs/',schema_view,name='docs'),   # 配置docs的url路径
    
]

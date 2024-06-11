
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from newapp import views

router = routers.DefaultRouter()
router.register(r'news', views.NewsViewset, basename='news')
router.register(r'articles', views.ArticlesViewset, basename='articles')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger-ui/', TemplateView.as_view(
       template_name='swagger-ui.html',
       extra_context={'schema_url':'openapi-schema'}
   ), name='swagger-ui'),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include('newapp.urls')),
    path("accounts/", include("allauth.urls")),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include(('newapp.urls'))),
    path('api/', include(router.urls)),
    # path('api-own/', include('api.urls')),
]

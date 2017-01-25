from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/',                             admin.site.urls                    ),
    url(r'^auth/',                              include('django.contrib.auth.urls')),
    url(r'^auth/register/',                     views.register, name='register'    ),
    url(r'^(?P<exercise_id>[0-9]+)/$',          views.detail, name='detail'        ),
    url(r'^(?P<exercise_id>[0-9]+)/sessions/$', views.sessions, name='sessions'    ),
    url(r'^$',                                  views.index, name='index'          ),
]

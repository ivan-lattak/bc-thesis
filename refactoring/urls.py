from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^admin/',                                                         admin.site.urls                            ),
    url(r'^auth/',                                                          include('django.contrib.auth.urls')        ),
    url(r'^auth/register/',                                                 views.register, name='register'            ),
    url(r'^auth/logged_out/',                                               views.logged_out, name='logged_out'        ),
    url(r'^(?P<exercise_id>[0-9]+)/$',                                      views.detail, name='detail'                ),
    url(r'^(?P<exercise_id>[0-9]+)/sessions/$',                             views.sessions, name='sessions'            ),
    url(r'^(?P<exercise_id>[0-9]+)/solutions/$',                            views.solutions, name='solutions'          ),
    url(r'^(?P<exercise_id>[0-9]+)/src_diff/$',                             views.src_diff, name='src_diff'            ),
    url(r'^(?P<exercise_id>[0-9]+)/test_diff/$',                            views.test_diff, name='test_diff'          ),
    url(r'^(?P<exercise_id>[0-9]+)/new_session/$',                          views.new_session, name='new_session'      ),
    url(r'^(?P<exercise_id>[0-9]+)/delete_session/(?P<session_id>[0-9]+)$', views.delete_session, name='delete_session'),
    url(r'^$',                                                              views.index, name='index'                  ),
]

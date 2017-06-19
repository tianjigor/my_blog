# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from firstapp.views import index, detail, detail_comment, index_login, index_register, detail_vote, archives, category, tag
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout

from DjangoUeditor import urls as DjangoUeditor_urls

app_name = 'firstapp'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^detail/(?P<page_num>\d+)$', detail, name="detail"),
    url(r'^comment/(?P<page_num>\d+)$', detail_comment, name="detail_comment"),
    url(r'^$', index, name="index"),
    url(r'^index/(?P<cate>[A-Za-z]+)$', index, name="index"),
    url(r'^login/$', index_login, name="login_regsiter"),
    url(r'^register/$', index_register, name="index_register"),
    url(r'^logout/$', logout, {'next_page': '/register'}, name="logout"),  #{'next_page':跳转页} loout参数
    url(r'^detail/vote/(?P<page_num>\d+)$', detail_vote, name="vote"),
    url(r'^ueditor/', include('DjangoUeditor.urls' )),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', category, name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', tag, name='tag'),
    url(r'^base/$', index, name="index"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

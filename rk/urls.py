## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^result/$', views.result),
    url(r'^success/$', views.success),
    url(r'^cancel/$', views.cancel),
]

## encoding: utf-8
##
## Max E. Kuznecov <mek@mek.uz.ua>
## muzmates.com 2013
##

from django.conf.urls import patterns, include, url

urlpatterns = patterns('rk.views',
    url(r'^init/$', 'init'),
    url(r'^result/$', 'result'),
    url(r'^success/$', 'success'),
    url(r'^fail/$', 'fail'),
)

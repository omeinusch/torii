from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'content.views.homepage', name='homepage'),
                       url(r'^news$', 'content.views.news', name='news'),
                       url(r'^news/(?P<news_slug>.+)$', 'content.views.news_detail', name='news-detail'),
                       url(r'^releases$', 'content.views.releases', name='releases'),
                       url(r'^releases/(?P<milestone_title>[\w\d\.]+)$', 'content.views.releases_detail', name='releases-detail'),
                       url(r'^downloads$', 'content.views.downloads', name='downloads'),
                       url(r'^support$', 'content.views.support', name='support'),

                       url(r'^admin/', include(admin.site.urls)),
)

"""project_nicework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from nicework import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.user_login, name='login'),
    # url(r'^register/', views.register, name='register'),
    # url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^base/', views.base, name='base'),
    url(r'^index/', views.index, name='index'),
    url(r'^$', views.welcome, name='welcome'),
    url(r'^contact/', views.contact, name='contact'),
    # url(r'^student/',
    #     views.student_index, name='student_index'),
    # url(r'^staff/',
    #     views.staff_index, name='staff_index'),
    # url(r'^mentor/',
    #     views.mentor_index, name='mentor_index'),
    url(r'^add_journal/$', views.add_journal, name='add_journal'),
    url(r'^edit_profile/$', views.edit_profile, name='edit_profile'),
    url(r'^add_activity/$', views.add_activity, name='add_activity'),
    url(r'^journal/(?P<journal_id>[\d\-]+)/add_entry/$',
        views.add_entry, name='add_entry'),
    # url(r'^entry/(?P<entry_id>[\d\-]+)/add_comment/$',
    #     views.add_comment, name='add_comment'),
    url(r'^delete_activity/(?P<activity_id>[\d\-]+)/$',
        views.delete_activity, name='delete_activity'),
    url(r'^delete_journal/(?P<journal_id>[\d\-]+)/$',
        views.delete_journal, name='delete_journal'),
    url(r'^view_classmates/$',
        views.view_classmates, name='view_classmates'),
    # url(r'^show_journal/(?P<activity_id>[\d\-]+)/$',
    #     views.show_journal, name='show_journal'),
    url(r'^show_entry/(?P<entry_id>[\d\-]+)/$',
        views.show_entry, name='show_entry'),
    url(r'^show_activity/(?P<activity_id>[\d\-]+)/$',
        views.show_activity, name='show_activity'),
    url(r'^edit_entry/(?P<entry_id>[\d\-]+)/$',
        views.edit_entry, name='edit_entry'),
    url(r'^evaluate_entry/(?P<entry_id>[\d\-]+)/$',
        views.evaluate_entry, name='evaluate_entry'),
    url(r'^pass_entry/(?P<entry_id>[\d\-]+)/$',
        views.pass_entry, name='pass_entry'),
    url(r'^fail_entry/(?P<entry_id>[\d\-]+)/$',
        views.fail_entry, name='fail_entry'),
    url(r'^like/(?P<entry_id>[\d\-]+)/$',
        views.like, name='like'),
    url(r'^edit_profile/$',
        views.edit_profile, name='edit_profile'),
    url(r'^view/$',
        views.view, name='view'),
    url(r'^view_classmates/$',
        views.view_classmates, name='view_classmates'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
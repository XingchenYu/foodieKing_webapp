"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth import views as auth_views

import foodie.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', foodie.views.home, name='home'),
    url(r'^mainpage$', foodie.views.main, name='main'),
    url(r'^register$', foodie.views.register, name='register'),
    url(r'^logout', auth_views.logout_then_login, name='logout'),
    url(r'^photo(?P<profile_id>[0-9]+)/$', foodie.views.photo, name='photo'),
    url(r'^edit/', foodie.views.main, name='edit'),
    url(r'^mealeventbox/(?P<eventid>[0-9]+)$', foodie.views.eventInfo, name='mealeventbox'),
    url(r'^addactivity$', foodie.views.addactivity, name='addactivity'),
    url(r'^get_allbubbles$', foodie.views.get_allbubbles, name='getallbubbles'),
    url(r'^restaurant/(?P<res_id>[0-9]+)$', foodie.views.restaurant, name='restaurant'),
    url(r'^joingroup$', foodie.views.join_group, name='joingroup'),
    url(r'^quitgroup$', foodie.views.quit_group, name='quitgroup'),
    url(r'^getdishphoto/(?P<name>.*)', foodie.views.getdishphoto, name='getdishphoto'),

    url(r'^post-new', foodie.views.post, name='post-new'),
    url(r'^get-posts/', foodie.views.get_posts, name='get-posts'),
    url(r'^get-changes/(?P<time>.+)$', foodie.views.get_changes),
    url(r'^get-changes/', foodie.views.get_changes),
    url(r'^create_restaurant$', foodie.views.create_restaurant, name='create_restaurant'),

    url(r'^order$', foodie.views.order, name='order'),
    url(r'^joinmealevent$', foodie.views.joinmealevent, name="joinevent"),
    url(r'^quitmealevent$', foodie.views.quitmealevent, name="quitmealevent"),
    url(r'^manage$', foodie.views.manage, name='manage'),
    url(r'^confirm/(?P<name>[0-9A-Za-z_\-]+)\\(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', foodie.views.confirm,
        name='confirm'),
    url(r'^forgetpassword/', foodie.views.forgetpassword, name='forgetpassword'),
    url(r'^reset/(?P<name>[0-9A-Za-z_\-]+)\\(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', foodie.views.reset,
        name='reset'),
    url(r'^comment/(?P<blog_id>\d+)$', foodie.views.comment),
    url(r'^get_comment_photo(?P<profile_id>[0-9]+)/$', foodie.views.get_comment_photo, name='get_comment_photo'),
    url(r'^get_group_buy_allbubbles$', foodie.views.get_group_buy_allbubbles, name='get_group_buy_allbubbles'),

    url(r'^getallitems$', foodie.views.getallitems, name='getallitems'),
    url(r'^getportrait/(?P<name>.*)', foodie.views.getportrait, name='getportrait'),
    url(r'^adddish$', foodie.views.adddish, name="adddish"),
    url(r'^deletedish', foodie.views.deletedish, name="deletedish"),

    url(r'^groupbuyinfo/(?P<eventid>[0-9]+)$', foodie.views.groupbuyinfo, name="groupbuyinfo"),
    url(r'^joingroupbuy$', foodie.views.joingroupbuy, name="joingroupbuy"),
    url(r'^quitgroupbuy$', foodie.views.quitgroupbuy, name="quitgroupbuy"),

    url(r'^get_all_groupbuy_items$', foodie.views.get_all_groupbuy_items, name="get_all_groupbuy_items"),
    url(r'^changepassword/', foodie.views.changepassword, name='changepassword'),
    url(r'^edit_res/(?P<res_id>[0-9]+)$', foodie.views.edit_res, name="edit_res"),
    url(r'^getprofile$', foodie.views.getprofile, name='getprofile'),

    url(r'^delete_groupbuy$', foodie.views.delete_groupbuy, name="delete_groupbuy"),
    url(r'^finishorder$', foodie.views.finishorder, name="finishorder"),

]

from __future__ import unicode_literals
from django.db.models import Max
from django.utils.html import escape
from django.db import models
from django.contrib.auth.models import User
from choices import *
import datetime


class Myuser(models.Model):
    user = models.OneToOneField(User, related_name="MAIN", on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    fav_foods = models.CharField(max_length=100, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    photo = models.ImageField(upload_to="user-images", null=True, blank=True)

    def __unicode__(self):
        return self.user.username


class Restaurant(models.Model):
    TYPE_CHOICES = (
        (1, 'Chinese'), (2, 'American'), (3, 'Japanese'), (4, 'Mexican'), (5, 'European'), (6, 'Indian'), (7, 'Other'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    res_name = models.CharField(max_length=50)  # reataurant name
    location = models.CharField(max_length=200, blank=True, null=True)  # the location of it
    coordinate_x = models.FloatField()  # longitude of it
    coordinate_y = models.FloatField()  # latitude of it
    build_time = models.DateTimeField(auto_now=True)  # date of building
    scale = models.IntegerField()  # The number of the restaurant can accommodate
    type_res = models.IntegerField(choices=TYPE_CHOICES, default=1, blank=True, null=True)  # the type of the reataurant
    popularity = models.IntegerField(blank=True, null=True)  # The number of the costumers have been to
    big_table = models.IntegerField()
    mid_table = models.IntegerField()
    small_table = models.IntegerField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    home_page = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return self.res_name


class MealEvent(models.Model):
    event_name = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)  # the restaurant they will go
    coordinate_x = models.FloatField()  # longitude of launching
    coordinate_y = models.FloatField()  # latitude of launching
    originator = models.ForeignKey(User, related_name="START",
                                   on_delete=models.CASCADE)  # the user who organize the event
    time_eating = models.DateTimeField('time eat', null=True)  # time of eating
    time_launch = models.DateTimeField('time launch', auto_now=True)  # time of launching the event
    members = models.ManyToManyField(User, related_name="mealevent",
                                     related_query_name="mealevent")  # menbers join in this event
    description = models.CharField(max_length=500, null=True)
    numbers = models.IntegerField(null=True)  # the max number of member

    def __unicode__(self):
        return self.restaurant.res_name + " " + self.event_name + " " + self.originator.username


class GroupBuy(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True)  # the restaurant
    # coordinate_x = models.IntegerField() #longitude of restaurant
    # coordinate_y = models.IntegerField() #latitude of restaurant
    time_start = models.DateTimeField()  # time of starting
    time_end = models.DateTimeField()  # time of ending
    time_launch = models.DateTimeField(blank=True)  # time of launching
    members = models.ManyToManyField(User, related_name="groupbuy", related_query_name="groupbuy",
                                     blank=True)  # menbers join in this activity
    description = models.CharField(max_length=500)
    backimg = models.ImageField(upload_to="event-images", blank=True)

    def __unicode__(self):
        return self.name


class Timetable(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)  # the restaurant
    week_start = models.TimeField()
    week_end = models.TimeField()
    sat_start = models.TimeField()
    sat_end = models.TimeField()
    sun_start = models.TimeField()
    sun_end = models.TimeField()

    def __unicode__(self):
        return self.restaurant.res_name


class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=30)
    price = models.FloatField()
    photo = models.ImageField(upload_to="dish-images")
    dish_type = models.CharField(max_length=30)  # the type of the dish
    pungency = models.IntegerField()  # the pungency degree of this dish
    source = models.CharField(max_length=300)  # ingredients of this dish
    is_spe = models.BooleanField(default=False)

    def __unicode__(self):
        return self.dish_name + " " + self.restaurant.res_name


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish)
    totalSum = models.FloatField()

    def __unicode__(self):
        r = ''
        for dish in self.dishes.all():
            r = r + dish.dish_name + " "
        return r


class Blog(models.Model):
    content = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_changed = models.DateTimeField(auto_now=True)
    like_number = models.IntegerField(default=0)
    dislike_number = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="comment-photo", blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.content

    @staticmethod
    def get_changes(res_name, time="1970-01-01T00:00+00:00"):
        return Blog.objects.filter(restaurant=res_name).filter(last_changed__gt=time).distinct()

    @property
    def html(self):
        result = """<br><br><br>
                    <div class='box box-widget'>
                        <div>
                            <div class='box-header with-border'>
                            <div class='user-block'>
                                <img class='round-border' src='/photo%s' alt='%s %s'>
                                <span class='username_ '>
                                    <a> %s </a>
                                </span>
                                <span class='description'> %s </span>
                            </div>
                        </div>
                        <p class='post_content_blog'>%s</p>
                        <img class='img-responsive show-in-modal' src='/get_comment_photo%s' alt='Photo'>
                        <button id='comment-toggle%s' class='btn btn-default move_comment_up'>Show comments</button>
                   </div>""" % (
        escape(self.user.id), escape(self.user.first_name), escape(self.user.last_name), escape(self.user.username),
        escape(self.pub_date.strftime('%b. %d, %Y %X')), escape(self.content), escape(self.id), escape(self.id))
        result += """<div hidden id='comment-area'>
                            <div class='form-group comment-btn'>
                                    <div class='col-sm-8'>
                                        <input id='commentField_%d' class='moveright-comment form-control' placeholder='Input comment...' type='text'>
                                    </div>
                                    <div class='col-sm-2'>
                                        <button id='commentbtn' btn-id=%d class='btn btn-primary'>Comment</button>
                                    </div>
                                </div>
                                <ol id='comment_list_%d'></ol>
                            </div>
                        </div>""" % (self.id, self.id, self.id)

        return result

    @staticmethod
    def get_max_time():
        return Blog.objects.all().aggregate(Max('last_changed'))['last_changed__max'] or "1970-01-01T00:00+00:00"


class Comment(models.Model):
    text = models.CharField(max_length=420)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    com_user = models.ForeignKey(User)
    com_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text + " " + self.blog.content

    @property
    def html(self):
        return """<br><br><br>
                <div>
                    <div class=''>
                        <div class=''>
                            <img  class='movetop_comment float-left round-border' src='/photo%s' alt='%s %s' height='50' width='50'/>
                            <a class=''>%s</a>
                            <span class='description'> %s </span>
                        </div>
                    <div class=''>
                        <p>%s</p>
                    </div>
                    <div class='content-time2 float-right movetop-text3 comment-time'>
                    </div>
                </div>""" % (
        escape(self.com_user.id), escape(self.com_user.first_name), escape(self.com_user.last_name),
        escape(self.com_user.username), escape(self.com_time.strftime('%m/%d/%y %H:%M:%S')), escape(self.text))
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from models import *
import json
from forms import *
import datetime
from django.utils import timezone
from mimetypes import guess_type
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core import serializers


@transaction.atomic
def home(request):
    if request.user.username:
        return redirect(reverse('main'))
    context = {}
    if request.method == 'GET':
        context['form_log'] = signForm()
        return render(request, "foodieking/home.html", context)

    form_log = signForm(request.POST)
    context['form_log'] = form_log

    if not form_log.is_valid():
        return render(request, 'foodieking/home.html', context)

    username = form_log.cleaned_data['username']
    password = form_log.cleaned_data['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        context['user'] = user
        login(request, user)
        return redirect(reverse('main'))
    else:
        return render(request, "foodieking/home.html", context)


@transaction.atomic
def register(request):
    context = {}
    if request.method == 'GET':
        context['form_reg'] = registerForm()
        return render(request, "foodieking/register.html", context)
    form_reg = registerForm(request.POST)
    context['form_reg'] = form_reg

    if not form_reg.is_valid():
        return render(request, 'foodieking/register.html', context)

    new_user = User.objects.create_user(username=form_reg.cleaned_data['username'],
                                        first_name=form_reg.cleaned_data['first_name'],
                                        last_name=form_reg.cleaned_data['last_name'],
                                        email=form_reg.cleaned_data['email'],
                                        password=form_reg.cleaned_data['password'],
                                        is_active=False)
    new_user.save()
    new_myuser = Myuser.objects.create(user=new_user)
    new_myuser.save()

    token = default_token_generator.make_token(new_user)
    email_body = """
        Welcome to FoodieKing. Please click the link below to verify your email address and complete the registration of your account:

        http://%s%s
        """ % (request.get_host(), reverse('confirm', args=(new_user.username, token)))
    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="web9382@gmail.com", recipient_list=[new_user.email])

    context['email'] = form_reg.cleaned_data['email']
    return render(request, 'foodieking/confirm.html', context)



@transaction.atomic
def confirm(request, name, token):
    user = get_object_or_404(User, username=name)
    if (default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse('main'))
    else:
        return redirect(reverse('register'))


@login_required
@transaction.atomic
def main(request):
    context = {}
    cur_user = request.user
    restaurants = Restaurant.objects.all().order_by('res_name')
    context['cur_user'] = cur_user
    context['restaurants'] = restaurants
    context['addEventForm'] = mealeventForm()
    cur_myuser = Myuser.objects.get(user=cur_user)
    context['cur_myuser'] = cur_myuser
    missions = MealEvent.objects.filter(members=cur_user) | MealEvent.objects.filter(originator=cur_user)
    context['missions'] = missions
    if request.method == 'GET':
        form_ed = editForm(instance=cur_user)
        form_my = editOtherForm(instance=cur_myuser)
        context['form_ed'] = form_ed
        context['form_my'] = form_my
        return render(request, "foodieking/main_page.html", context)
    form_ed = editForm(request.POST, instance=cur_user)
    form_my = editOtherForm(request.POST, request.FILES, instance=cur_myuser)
    if not form_ed.is_valid():
        context['form_ed'] = form_ed
        context['form_my'] = form_my
        return render(request, 'foodieking/main_page.html', context)
    if not form_my.is_valid():
        context['form_ed'] = form_ed
        context['form_my'] = form_my
        return render(request, 'foodieking/main_page.html', context)

    form_ed.save()
    form_my.save()
    return redirect(reverse('main'))


@login_required
@transaction.atomic
def photo(request, profile_id):
    user = User.objects.get(id=profile_id)
    my_user = get_object_or_404(Myuser, user=user)
    if not my_user.photo:
        raise Http404
    content_type = guess_type(my_user.photo.name)
    return HttpResponse(my_user.photo, content_type=content_type)


@login_required
@transaction.atomic
def eventInfo(request, eventid):
    cur_event = MealEvent.objects.get(id=eventid)
    print cur_event
    context = {}
    cur_user = request.user
    context["event_name"] = cur_event.event_name
    context["restaurant_name"] = cur_event.restaurant.res_name
    context["originator"] = cur_event.originator.username
    context["restaurant_id"] = cur_event.restaurant.id
    context["description"] = cur_event.description
    context["number"]=cur_event.numbers
    context["time"]=cur_event.time_eating
    # print context

    if ((cur_user == cur_event.originator) or (cur_user in cur_event.members.all())):
        context['joined'] = True
    else:
        context['joined'] = False

    return render(request, "json/eventInfo.json", context, content_type="application/json")


@login_required
@transaction.atomic
def groupbuyinfo(request, eventid):
    cur_groupbuy = GroupBuy.objects.get(id=eventid)
    # print cur_event
    context = {}
    context["name"] = cur_groupbuy.name
    context["resName"] = cur_groupbuy.restaurant.res_name
    context["res_id"] = cur_groupbuy.restaurant.id
    context["start"] = cur_groupbuy.time_start
    context["end"] = cur_groupbuy.time_end
    context["description"] = cur_groupbuy.description
    # print context
    cur_user = request.user

    if (cur_user in cur_groupbuy.members.all()):
        context['joined'] = True
    else:
        context['joined'] = False

    return render(request, "json/groupbuyinfo.json", context, content_type="application/json")


@login_required
@transaction.atomic
def getallitems(request):
    curTime = datetime.datetime.now()
    cur_user = User.objects.get(username=request.GET['username'])
    missions = MealEvent.objects.filter(members=cur_user).filter(time_eating__gt=curTime) | MealEvent.objects.filter(originator=cur_user).filter(time_eating__gt=curTime)
    list = ""
    for onemission in missions:
        list = list + ' ' + str(onemission.id)
    context = {'items': missions, 'list': list}
    return render(request, 'json/items.json', context, content_type='application/json')


@login_required
@transaction.atomic
def get_all_groupbuy_items(request):
    curTime = datetime.datetime.now()
    cur_user = User.objects.get(username=request.GET['username'])
    groupbuys = GroupBuy.objects.filter(members=cur_user).filter(time_end__gt=curTime)
    context = {'items': groupbuys}
    return render(request, 'json/groupbuyitems.json', context, content_type='application/json')


@login_required
@transaction.atomic
def getportrait(request, name):
    user = Myuser.objects.get(user__username=name)
    if not user.photo:
        raise Http404
    pictype = guess_type(user.photo.name)
    return HttpResponse(user.photo, content_type=pictype)


@login_required
@transaction.atomic
def get_allbubbles(request):
    curTime = datetime.datetime.now()
    bubbles = MealEvent.objects.filter(time_eating__gt=curTime)
    context = {"bubbles": bubbles}
    return render(request, 'json/bubbles.json', context, content_type='application/json')


#  On mainpage
@login_required
@transaction.atomic
def joingroupbuy(request):
    eventid = request.POST['eventid']
    mygroupbuy = GroupBuy.objects.get(id=eventid)
    user = request.user
    mygroupbuy.members.add(user)
    mygroupbuy.save()
    user.groupbuy.add(mygroupbuy)
    user.save()
    return HttpResponse("")


@login_required
@transaction.atomic
def quitgroupbuy(request):
    eventid = request.POST['eventid']
    mygroupbuy = GroupBuy.objects.get(id=eventid)
    user = request.user
    mygroupbuy.members.remove(user)
    mygroupbuy.save()
    user.groupbuy.remove(mygroupbuy)
    user.save()
    return HttpResponse("")

@transaction.atomic
@login_required
def addactivity(request):
    mealeventform = mealeventForm(request.POST)
    context={}
    if(mealeventform.is_valid()):
        # resid = int(mealeventform.cleaned_data['restaurant_name'])
        # resName = dict(mealeventform.fields['restaurant_name'].choices)[resid]
        res = Restaurant.objects.get(res_name=mealeventform.cleaned_data['restaurant_name'])
        event_name = mealeventform.cleaned_data['event_name']
        number = mealeventform.cleaned_data['numbers']
        description = mealeventform.cleaned_data['description']
        time = mealeventform.cleaned_data['time_eating']
        user = request.user
        if not res:
            raise Http404

        lat=request.POST['lat']
        lng=request.POST['lng']
        new_event = MealEvent(event_name = event_name, restaurant=res, numbers=number,
                              description=description, time_eating=time,
                              coordinate_x=lat, coordinate_y=lng,originator=user)
        new_event.save()
        eventid = new_event.id
        context["eventid"]=eventid
        context['errors']=""
        return render(request, 'json/activity.json', context, content_type='application/json')

    errors = json.dumps(mealeventform.errors)
    print errors
    context['errors']=errors
    return render(request,'json/errors.json',context, content_type="application/json")

@transaction.atomic
@login_required
def restaurant(request, res_id):
    context = {}
    user = request.user
    cur_myuser = Myuser.objects.get(user=user)
    restaurant = get_object_or_404(Restaurant, id=res_id)
    restaurants = Restaurant.objects.all().order_by('res_name')
    groups = GroupBuy.objects.filter(restaurant=restaurant)
    dishes = Dish.objects.filter(restaurant=restaurant)
    specialdishes = Dish.objects.filter(restaurant=restaurant, is_spe=True)
    mealevents = MealEvent.objects.filter(restaurant=restaurant)
    context['postform'] = postForm()
    # if restaurant.timetable_set is not None:
    timetable = get_object_or_404(Timetable, restaurant=restaurant)
    context['timetable'] = timetable
    context['groups'] = groups
    context['cur_myuser'] = cur_myuser
    context['specialdishes'] = specialdishes
    context['dishes'] = dishes
    context['mealevents'] = mealevents
    context['restaurant'] = restaurant
    context['restaurants'] = restaurants
    return render(request, "foodieking/restaurant_page_user.html", context)


@transaction.atomic
@login_required
def join_group(request):
    cur_user = request.user
    group_id = request.POST['id']
    print ('middle111')
    group = GroupBuy.objects.get(id=group_id)
    group.members.add(cur_user)
    group.save()
    return HttpResponse("")


@transaction.atomic
@login_required
def quit_group(request):
    cur_user = request.user
    group_id = request.POST['id']
    group = GroupBuy.objects.get(id=group_id)
    group.members.remove(cur_user)
    group.save()
    return HttpResponse("")


@login_required
@transaction.atomic
def getdishphoto(request, name):
    dish = Dish.objects.get(dish_name=name)
    if not dish.photo:
        raise Http404
    pictype = guess_type(dish.photo.name)
    return HttpResponse(dish.photo, content_type=pictype)


@login_required
@transaction.atomic
def get_changes(request, time="1970-01-01T00:00+00:00"):
    restaurant_name = request.GET['res_name']
    res = Restaurant.objects.get(res_name=restaurant_name)
    max_time = Blog.get_max_time()
    blogs = Blog.get_changes(res, time)
    context = {"max_time": max_time, "blogs": blogs}
    return render(request, 'json/blogs.json', context, content_type='application/json')


@login_required
@transaction.atomic
def get_posts(request):
    max_time = Blog.get_max_time()
    print max_time
    print "1"
    restaurant_name = request.GET['res_name']
    print "123"
    print "res_name:" + restaurant_name
    res = Restaurant.objects.get(res_name=restaurant_name)

    blogs = Blog.objects.filter(restaurant=res).order_by('-pub_date')
    # blogs = Blog.objects.order_by('-pub_date')
    context = {"max_time": max_time, "blogs": blogs}
    print "get_posts done"
    return render(request, 'json/blogs.json', context, content_type='application/json')


@login_required
@transaction.atomic
def post(request):
    restaurant_name = request.POST['resName']
    res = Restaurant.objects.get(res_name=restaurant_name)
    user = User.objects.get(username=request.POST['user'])
    postform = postForm(request.POST, request.FILES)
    if postform.is_valid():
        new_post = Blog(content=postform.cleaned_data['blog'], photo=postform.cleaned_data['photo'],
                        restaurant=res, user=user)
        print "valid"
        new_post.save()
        time = new_post.pub_date.strftime('%b. %d, %Y %X')
        context = {"id": new_post.id, "time": time, "userid": user.id}
        return render(request, 'json/postid.json', context, content_type='application/json')
    print "unvalid"
    return HttpResponse("")


@login_required
@transaction.atomic
def create_restaurant(request):
    context = {}
    cur_user = request.user
    restaurants = Restaurant.objects.all().order_by('res_name')
    context['cur_user'] = cur_user
    context['restaurants'] = restaurants
    cur_myuser = Myuser.objects.get(user=cur_user)
    context['cur_myuser'] = cur_myuser
    if request.method == "GET":
        context['form'] = restaurantForm()
        context['form2'] = timetableForm()
        return render(request, 'foodieking/create_restaurant.html', context)
    user = request.user
    form = restaurantForm(request.POST)
    form2 = timetableForm(request.POST)
    context['form'] = form
    context['form2'] = form2
    if not form.is_valid():
        return render(request, 'foodieking/create_restaurant.html', context)
    if not form2.is_valid():
        return render(request, 'foodieking/create_restaurant.html', context)
    new_res = Restaurant(user=user, res_name=form.cleaned_data['res_name'], location=form.cleaned_data['location'],
                         coordinate_x=form.cleaned_data['coordinate_x'], coordinate_y=form.cleaned_data['coordinate_y'],
                         scale=form.cleaned_data['scale'], type_res=form.cleaned_data['type_res'],
                         big_table=form.cleaned_data['big_table'],
                         mid_table=form.cleaned_data['mid_table'], small_table=form.cleaned_data['small_table'],
                         phone=form.cleaned_data['phone'], email=form.cleaned_data['email'],
                         home_page=form.cleaned_data['home_page'],
                         description=form.cleaned_data['description'])
    new_res.save()
    new_time = Timetable(restaurant=new_res, week_start=form2.cleaned_data['week_start'],
                         week_end=form2.cleaned_data['week_end'],
                         sat_start=form2.cleaned_data['sat_start'], sat_end=form2.cleaned_data['sat_end'],
                         sun_start=form2.cleaned_data['sun_start'], sun_end=form2.cleaned_data['sun_end'])
    new_time.save()
    return redirect(reverse('manage'))

    #  On restaurant page: modal1, online order


@login_required
@transaction.atomic
def order(request):
    res = Restaurant.objects.get(res_name=request.POST['res_name'])
    order = Order.objects.create(restaurant=res, user=request.user)
    for dish in request.POST.getlist('dishes[]'):
        dishobject = Dish.objects.get(id=dish)
        order.dishes.add(dishobject)
    order.save()
    return HttpResponse("")


#  On mainpage
@login_required
@transaction.atomic
def joinmealevent(request):
    eventid = request.POST['eventid']
    myevent = MealEvent.objects.get(id=eventid)
    user = request.user
    myevent.members.add(user)
    myevent.save()
    user.mealevent.add(myevent)
    user.save()
    return HttpResponse("")


@login_required
@transaction.atomic
def quitmealevent(request):
    eventid = request.POST['eventid']
    myevent = MealEvent.objects.get(id=eventid)
    user = request.user
    if (myevent.originator != user):
        myevent.members.remove(user)
        myevent.save()
        user.mealevent.remove(myevent)
        user.save()
    else:
        myevent.delete()
    return HttpResponse("")


@login_required
@transaction.atomic
def manage(request):
    user = request.user
    restaurant = get_object_or_404(Restaurant, user=user)
    context = {}
    restaurants = Restaurant.objects.all().order_by('res_name')
    timetable = get_object_or_404(Timetable, restaurant=restaurant)
    groups = GroupBuy.objects.filter(restaurant=restaurant)
    dishes = Dish.objects.filter(restaurant=restaurant)
    mealevents = MealEvent.objects.filter(restaurant=restaurant)
    orders = Order.objects.filter(restaurant=restaurant)
    context['user'] = user
    context['restaurants'] = restaurants
    context['restaurant'] = restaurant
    context['timetable'] = timetable
    context['groups'] = groups
    context['dishes'] = dishes
    context['mealevents'] = mealevents
    context['form_groupbuy'] = GroupbuyForm()
    context['dishform'] = dishForm()
    context['orders'] = orders
    if request.method == "GET":
        return render(request, "foodieking/restaurant_manage.html", context)
    form = GroupbuyForm(request.POST)
    context['form_groupbuy'] = form
    if not form.is_valid():
        return render(request, 'foodieking/restaurant_manage.html', context)
    obj = GroupBuy(name=form.cleaned_data['name'], restaurant=restaurant, description=form.cleaned_data['description'],
                   time_start=form.cleaned_data['time_start'],
                   time_end=form.cleaned_data['time_end'], time_launch=datetime.datetime.now())
    obj.save()
    return redirect(reverse("manage"))


@login_required
@transaction.atomic
def adddish(request):
    dishform = dishForm(request.POST,request.FILES)
    print "dishform"
    print dishform
    restaurant = Restaurant.objects.get(res_name=request.POST['resName'])
    if dishform.is_valid():
        is_spe = dishform.cleaned_data['is_spe']
        if(is_spe == '1'):
            spe = True
        else:
            spe = False
        dish = Dish.objects.create(dish_name=dishform.cleaned_data['dish_name'],price=dishform.cleaned_data['price'],source=dishform.cleaned_data['source'],photo=dishform.cleaned_data['photo'],dish_type=dishform.cleaned_data['dish_type'],pungency=dishform.cleaned_data['pungency'],restaurant=restaurant,is_spe=spe)
        dish.save()
        context={"id":dish.id,"errors":""}
        return render(request,"json/dishid.json",context,content_type='application/json')
    errors = json.dumps(dishform.errors)
    context={"errors":errors}
    return render(request,'json/errors.json',context, content_type="application/json")



@login_required
@transaction.atomic
def deletedish(request):
    try:
        dish = Dish.objects.get(id=request.POST['id'])
        dish.delete()
        return HttpResponse("")
    except:
        return HttpResponse("")


@transaction.atomic
def forgetpassword(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ForgetPasswordForm()
        return render(request, 'foodieking/forgetpassword.html', context)
    form = ForgetPasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'foodieking/forgetpassword.html', context)
    cu_user = User.objects.get(username=form.cleaned_data['username'])
    token = default_token_generator.make_token(cu_user)
    email_body = """
        Please click the link below to reset your email:

        http://%s%s
        """ % (request.get_host(), reverse('reset', args=(cu_user.username, token)))
    send_mail(subject="Reset your password of FoodieKing",
              message=email_body,
              from_email="web9382@gmail.com",
              recipient_list=[cu_user.email])

    context['email'] = cu_user.email
    message = []
    message.append('Please check your email to reset your password!')
    context['message'] = message
    return render(request, 'foodieking/forgetpassword.html', context)


@transaction.atomic
def reset(request, name, token):
    user = get_object_or_404(User, username=name)
    if (default_token_generator.check_token(user, token)):
        if request.method == 'GET':
            form = ResetPasswordForm()
            context = {'name': name, 'form': form, 'token': token}
            return render(request, 'foodieking/reset.html', context)
        else:
            form = ResetPasswordForm(request.POST)
            context = {'name': name, 'form': form, 'token': token}
            if form.is_valid():
                newpassword = form.cleaned_data['newpassword1']
                user.set_password(newpassword)
                user.save()
                login(request, user)
                return redirect(reverse('main'))
            else:
                return render(request, 'foodieking/reset.html', context)
    else:
        return redirect(reverse('forgetpassword'))


# On restaurant page: modal1, online order
@login_required
@transaction.atomic
def order(request):
    res = Restaurant.objects.get(res_name=request.POST['res_name'])
    order = Order.objects.create(restaurant=res, user=request.user, totalSum=request.POST['totalSum'])
    for dish in request.POST.getlist('dishes[]'):
        dishobject = Dish.objects.get(id=dish)
        order.dishes.add(dishobject)
    order.save()
    return HttpResponse("")


@login_required
@transaction.atomic
def comment(request, blog_id):
    print blog_id
    if not 'comment' in request.POST or not request.POST['comment']:
        print blog_id
        raise Http404
    else:
        blog = Blog.objects.get(id=blog_id)
        print blog.content
        new_comment = Comment(text=request.POST['comment'], blog=blog, com_user=request.user)
        new_comment.save()
        print new_comment.text
        comments = Comment.objects.all()
        blog = Blog.objects.get(id=blog_id)
        context = {'blog': blog, 'comments': comments}
        return render(request, 'json/comments.json', context, content_type='application/json')


@login_required
@transaction.atomic
def get_comment_photo(request, profile_id):
    blog = get_object_or_404(Blog, id=profile_id)
    if not blog.photo:
        raise Http404
    content_type = guess_type(blog.photo.name)
    return HttpResponse(blog.photo, content_type=content_type)


@login_required
@transaction.atomic
def get_group_buy_allbubbles(request):
    groupbuy_bubbles = GroupBuy.objects.all()
    context = {"groupbuy_bubbles": groupbuy_bubbles}
    return render(request, 'json/groupbuy_bubbles.json', context, content_type='application/json')


@login_required
@transaction.atomic
def changepassword(request):
    my_user = Myuser.objects.get(user=request.user)
    if request.method == 'GET':
        form = ChangePasswordForm()
        return render(request, 'foodieking/change_password.html', {'form': form, 'my_user': my_user})
    else:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = form.cleaned_data['oldpassword']
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = form.cleaned_data['newpassword1']
                user.set_password(newpassword)
                user.save()
                login(request, user)
                return redirect(reverse('main'))
            else:
                return render(request, 'foodieking/change_password.html',
                              {'form': form, 'my_user': my_user, 'oldpassword_is_wrong': True})
        else:
            return render(request, 'foodieking/change_password.html', {'form': form, 'my_user': my_user})


@login_required
@transaction.atomic
def edit_res(request, res_id):
    context = {}
    restaurant = get_object_or_404(Restaurant, id=res_id)
    timetable = get_object_or_404(Timetable, restaurant=restaurant)
    context['timetable'] = timetable
    context['restaurant'] = restaurant
    if request.method == "GET":
        context['form'] = editrestaurantForm(instance=restaurant)
        context['form2'] = timetableForm(instance=timetable)
        return render(request, 'foodieking/edit_restaurant.html', context)
    form_res = editrestaurantForm(request.POST, instance=restaurant)
    form_res2 = timetableForm(request.POST, instance=timetable)
    context['form'] = form_res
    context['form2'] = form_res2
    if not form_res.is_valid():
        return render(request, 'foodieking/edit_restaurant.html', context)
    if not form_res2.is_valid():
        return render(request, 'foodieking/edit_restaurant.html', context)
    form_res.save()
    form_res2.save()
    return redirect(reverse('manage'))


@login_required
@transaction.atomic
def getprofile(request):
    context = {}
    check_user = get_object_or_404(User, username=request.POST['name'])
    check_myuser = get_object_or_404(Myuser, user=check_user)

    context['check_user'] = check_user
    context['check_myuser'] = check_myuser

    if check_myuser.photo:
        context['hasphoto'] = "True"
    else:
        context['hasphoto'] = "False"
    return render(request, 'json/profile.json', context, content_type='application/json')


@login_required
@transaction.atomic
def delete_groupbuy(request):
    try:
        groupbuy = GroupBuy.objects.get(id=request.POST['id'])
        groupbuy.delete()
        return HttpResponse("")
    except:
        return HttpResponse("")

@login_required
@transaction.atomic
def finishorder(request):
    try:
        order = Order.objects.get(id=request.POST['id'])
        order.delete()
        return HttpResponse("")
    except:
        return HttpResponse("")
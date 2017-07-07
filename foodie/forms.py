from django import forms
from choices import *
from django.contrib.auth.models import User
from models import *


class signForm(forms.Form):
    username = forms.CharField(max_length=30, label='Username:',
                               widget=forms.TextInput(attrs={'placeholder': "Input Username...",
                                                             'class': 'form-control input-username',
                                                             'name': 'username'}))
    password = forms.CharField(max_length=50, label='Password:',
                               widget=forms.PasswordInput(attrs={'placeholder': "Input password...",
                                                                 'class': 'form-control input-username',
                                                                 'name': 'password'}))

    def clean(self):
        cleaned_data = super(signForm, self).clean()
        return cleaned_data


class registerForm(forms.ModelForm):
    cpassword = forms.CharField(max_length=50, label="Confirm password:",
                                widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password...",
                                                                  'class': 'form-control input-username'}))
    email = forms.EmailField(label="Email:",
                             widget=forms.TextInput(attrs={'placeholder': "Input Email...",
                                                           'class': 'form-control input-username'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Input Username...",
                                               'class': 'form-control input-username'}),
            'first_name': forms.TextInput(attrs={'placeholder': "Input First name...",
                                                 'class': 'form-control input-username'}),
            'last_name': forms.TextInput(attrs={'placeholder': "Input Last name...",
                                                'class': 'form-control input-username'}),
            'password': forms.PasswordInput(attrs={'placeholder': "Input Password...",
                                                   'class': 'form-control input-username'})
        }

    def clean(self):
        cleaned_data = super(registerForm, self).clean()

        password = cleaned_data.get('password')
        cpassword = cleaned_data.get('cpassword')
        if password and cpassword and password != cpassword:
            raise forms.ValidationError("Password did not match!")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username


class editForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': "Input First name...",
                                                 'class': 'form-control input-firstname'}),
            'last_name': forms.TextInput(attrs={'placeholder': "Input Last name...",
                                                'class': 'form-control input-lastname'}),
            'email': forms.TextInput(attrs={'placeholder': "Input Email...",
                                            'class': 'form-control input-pro'}),
        }

    def clean(self):
        cleaned_data = super(editForm, self).clean()
        return cleaned_data


class editOtherForm(forms.ModelForm):
    class Meta:
        model = Myuser
        fields = ['age', 'fav_foods', 'photo', 'gender']
        widgets = {
            'age': forms.TextInput(attrs={'placeholder': "Input age...",
                                          'class': 'form-control input-pro'}),
            'fav_foods': forms.Textarea(attrs={'placeholder': "Input bio...",
                                               'class': 'form-control input-pro'}),
            'photo': forms.FileInput(attrs={'class': 'form-control input-pro'}),
            'gender': forms.Select(choices=GENDER_CHOICES, attrs={'class': 'input-gen'})
        }

    def clean(self):
        cleaned_data = super(editOtherForm, self).clean()
        return cleaned_data


class mealeventInfoForm(forms.Form):
    event_name = forms.CharField(max_length=50)
    restaurant_name = forms.CharField(max_length=50)
    originator = forms.CharField(max_length=50)


class mealeventForm(forms.Form):
    event_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'id': "addactivity_event_name", 'placeholder': 'Event Name'}))
    restaurant_name = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'id': "addactivity_restaurant_name", 'placeholder': 'Restaurant Name'}))
    time_eating = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'],
                                      widget=forms.DateTimeInput(attrs={'class': "datepicker",'placeholder': "Input start time",
                                                                        'id': 'addactivity_time'}))  # time of eating

    description = forms.CharField(max_length=500, widget=forms.TextInput(
        attrs={'id': "addactivity_description", 'placeholder': 'Describe about your event'}))
    numbers = forms.IntegerField(widget=forms.NumberInput(
        attrs={'id': "addactivity_number", 'placeholder': 'Number'}))  # the max number of member

    def clean_restaurant_name(self):
        restaurant_name = self.cleaned_data.get('restaurant_name')
        if (len(Restaurant.objects.filter(res_name=restaurant_name)) == 0):
            raise forms.ValidationError("Restaurant does not exist.")
        return restaurant_name

    def clean_number(self):
        number = self.cleaned_data.get('number')
        if (number <= 0):
            raise forms.ValidationError("Number of people should be larger than 0.")
        return number


class postForm(forms.Form):
    blog = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'id': 'blogContent','class':'form-control','rows':4}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'blogPhoto'}))


class restaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['res_name', 'location', 'coordinate_x', 'coordinate_y', 'scale', 'type_res', 'big_table', 'mid_table',
                  'small_table', 'phone', 'email', 'home_page', 'description']
        widgets = {
            'res_name': forms.TextInput(
                attrs={'placeholder': "Input restaurant name...", 'class': 'form-control input-username',
                       'id': 'resName'}),
            'location': forms.TextInput(
                attrs={'placeholder': "Input location...", 'class': 'form-control input-username',
                       'id': 'resLocation'}),
            'coordinate_x': forms.TextInput(
                attrs={'placeholder': "Choose location on the map...", 'class': 'form-control input-username',
                       'id': 'resCoordX'}),
            'coordinate_y': forms.TextInput(
                attrs={'placeholder': "Choose location on the map...", 'class': 'form-control input-username',
                       'id': 'resCoordY'}),
            'scale': forms.TextInput(
                attrs={'placeholder': "Input the seating capacity...", 'class': 'form-control input-username',
                       'id': 'resScale'}),
            'type_res': forms.Select(attrs={'class': 'form-control input-username', 'id': 'resType'}),
            'big_table': forms.TextInput(
                attrs={'placeholder': "Input number of big table...", 'class': 'form-control input-username',
                       'id': 'resBigTable'}),
            'mid_table': forms.TextInput(
                attrs={'placeholder': "Input number of medium table...", 'class': 'form-control input-username',
                       'id': 'resMediumTable'}),
            'small_table': forms.TextInput(
                attrs={'placeholder': "Input number of small table...", 'class': 'form-control input-username',
                       'id': 'resSmallTable'}),
            'phone': forms.TextInput(
                attrs={'placeholder': "Input phone number...", 'class': 'form-control input-username',
                       'id': 'resPhone'}),
            'email': forms.TextInput(
                attrs={'placeholder': "Input email...", 'class': 'form-control input-username', 'id': 'resEmail'}),
            'home_page': forms.TextInput(
                attrs={'placeholder': "Input home page...", 'class': 'form-control input-username',
                       'id': 'resHomepage'}),
            'description': forms.Textarea(
                attrs={'placeholder': "Input description...", 'class': 'form-control input-username',
                       'id': 'resDescription'}),
        }

    def clean(self):
        cleaned_data = super(restaurantForm, self).clean()
        return cleaned_data

    def clean_res_name(self):
        res_name = self.cleaned_data.get('res_name')
        if Restaurant.objects.filter(res_name__exact=res_name):
            raise forms.ValidationError("Restaurant name is already taken.")
        return res_name


class timetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['week_start', 'week_end', 'sat_start', 'sat_end', 'sun_start', 'sun_end']
        widgets = {
            'week_start': forms.TimeInput(
                attrs={'placeholder': "Open time of weekdays(hh:mm:ss)", 'class': 'form-control input-username'}),
            'week_end': forms.TimeInput(
                attrs={'placeholder': "Close time of weekdays(hh:mm:ss)", 'class': 'form-control input-username'}),
            'sat_start': forms.TimeInput(
                attrs={'placeholder': "Open time of Saturday(hh:mm:ss)", 'class': 'form-control input-username'}),
            'sat_end': forms.TimeInput(
                attrs={'placeholder': "Close time of Saturday(hh:mm:ss)", 'class': 'form-control input-username'}),
            'sun_start': forms.TimeInput(
                attrs={'placeholder': "Open time of Sunday(hh:mm:ss)", 'class': 'form-control input-username'}),
            'sun_end': forms.TimeInput(
                attrs={'placeholder': "Close time of Sunday(hh:mm:ss)", 'class': 'form-control input-username'}),
        }

    def clean(self):
        cleaned_data = super(timetableForm, self).clean()
        return cleaned_data


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="Username",
        error_messages={'required': 'Please input your username!'},
        widget=forms.TextInput(attrs={'placeholder': "Input username...",
                                      'class': 'form-control input-username'}))

    def clean(self):
        cleaned_data = super(ForgetPasswordForm, self).clean()
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is not existed.")

        return username


class ResetPasswordForm(forms.Form):
    newpassword1 = forms.CharField(
        required=True,
        label="New password",
        error_messages={'required': 'Please input new password!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Input new password...",
                                          'class': 'form-control input-username'}))

    newpassword2 = forms.CharField(
        required=True,
        label="Confirm password",
        error_messages={'required': 'Please input new password again!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Confirm new password...",
                                          'class': 'form-control input-username'}))

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("You should complete every textarea!")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError("New passwords do not match!")
        else:
            cleaned_data = super(ResetPasswordForm, self).clean()
        return cleaned_data


class dishForm(forms.ModelForm):
    choices=[(1,'Special Dish'),(2,'Regular Dish')]
    is_spe = forms.ChoiceField(widget=forms.Select(attrs={'id':'dishIsSpec','class':'form-control'}), choices=choices)
    class Meta:
        model = Dish
        fields = ['dish_name', 'price',  'source', 'dish_type', 'pungency','photo']
        widgets = {
            'dish_name': forms.TextInput(attrs={'placeholder': "Dish name",'class':'form-control','id':'dishName'}),
            'price': forms.TextInput(attrs={'placeholder': "Dish price",'class': 'form-control','id':'dishPrice'}),
            'photo': forms.FileInput(attrs={'class': 'form-control','id':'dishPhoto'}),
            'source': forms.TextInput(attrs={'placeholder': "Ingredients",'class': 'form-control','id':'dishSource'}),
            'dish_type': forms.TextInput(attrs={'placeholder': "Dish type",'class': 'form-control','id':'dishType'}),
            'pungency': forms.NumberInput(attrs={'placeholder': "Pungency level",'class': 'form-control','id':'dishPungency'}),
        }

    def clean(self):
        cleaned_data = super(dishForm, self).clean()
        return cleaned_data

class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label="Old password",
        error_messages={'required': 'Please input old password!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Input old password...",
                                          'class': 'form-control input-username'}))

    newpassword1 = forms.CharField(
        required=True,
        label="New password",
        error_messages={'required': 'Please input new password!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Input new password...",
                                          'class': 'form-control input-username'}))

    newpassword2 = forms.CharField(
        required=True,
        label="Confirm password",
        error_messages={'required': 'Please input new password again!'},
        widget=forms.PasswordInput(attrs={'placeholder': "Confirm new password...",
                                          'class': 'form-control input-username'}))

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("You should complete every textarea!")
        elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
            raise forms.ValidationError("New passwords do not match!")
        else:
            cleaned_data = super(ChangePasswordForm, self).clean()
        return cleaned_data


class editrestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['res_name', 'location', 'coordinate_x', 'coordinate_y', 'scale', 'type_res', 'big_table', 'mid_table',
                  'small_table', 'phone', 'email', 'home_page', 'description']
        widgets = {
            'res_name': forms.TextInput(
                attrs={'placeholder': "Input restaurant name...", 'class': 'form-control input-username',
                       'id': 'resName'}),
            'location': forms.TextInput(
                attrs={'placeholder': "Input location...", 'class': 'form-control input-username',
                       'id': 'resLocation'}),
            'coordinate_x': forms.TextInput(
                attrs={'placeholder': "Choose location on the map...", 'class': 'form-control input-username',
                       'id': 'resCoordX'}),
            'coordinate_y': forms.TextInput(
                attrs={'placeholder': "Choose location on the map...", 'class': 'form-control input-username',
                       'id': 'resCoordY'}),
            'scale': forms.TextInput(
                attrs={'placeholder': "Input the seating capacity...", 'class': 'form-control input-username',
                       'id': 'resScale'}),
            'type_res': forms.Select(attrs={'class': 'form-control input-username', 'id': 'resType'}),
            'big_table': forms.TextInput(
                attrs={'placeholder': "Input number of big table...", 'class': 'form-control input-username',
                       'id': 'resBigTable'}),
            'mid_table': forms.TextInput(
                attrs={'placeholder': "Input number of medium table...", 'class': 'form-control input-username',
                       'id': 'resMediumTable'}),
            'small_table': forms.TextInput(
                attrs={'placeholder': "Input number of small table...", 'class': 'form-control input-username',
                       'id': 'resSmallTable'}),
            'phone': forms.TextInput(
                attrs={'placeholder': "Input phone number...", 'class': 'form-control input-username',
                       'id': 'resPhone'}),
            'email': forms.TextInput(
                attrs={'placeholder': "Input email...", 'class': 'form-control input-username', 'id': 'resEmail'}),
            'home_page': forms.TextInput(
                attrs={'placeholder': "Input home page...", 'class': 'form-control input-username',
                       'id': 'resHomepage'}),
            'description': forms.Textarea(
                attrs={'placeholder': "Input description...", 'class': 'form-control input-username',
                       'id': 'resDescription'}),
        }

    def clean(self):
        cleaned_data = super(editrestaurantForm, self).clean()
        return cleaned_data



class GroupbuyForm(forms.ModelForm):
    class Meta:
        model = GroupBuy
        fields = ['name', 'restaurant', 'description', 'time_start', 'time_end', 'time_launch']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Input group_buy name", 'class': 'form-control input-username'}),
            'restaurant': forms.TextInput(attrs={'placeholder': "Input restaurant name", 'class': 'form-control input-username'}),
            'description': forms.TextInput(attrs={'placeholder': "Input description", 'class': 'form-control input-username'}),
            'time_start': forms.DateTimeInput(attrs={'placeholder': "Input Start Time,   the Format shoule be like '2016-12-05 9:00'", 'class': 'form-control input-username'}),
            'time_end': forms.DateTimeInput(attrs={'placeholder': "Input  End  Time,   the Format shoule be like '2016-12-05 9:00'", 'class': 'form-control input-username'}),
            'time_launch': forms.DateTimeInput(attrs={'placeholder': "Input Time_Launch,   the Format shoule be like '2016-12-05 9:00'", 'class': 'form-control input-username'})
        }

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError("You should complete every textarea!")
        cleaned_data = super(GroupbuyForm, self).clean()
        return cleaned_data



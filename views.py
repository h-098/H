from django.shortcuts import render,redirect
from reservationApp.models import Category, Bus, Schedule
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from reservationApp.forms import UserRegistration, UpdateProfile, UpdatePasswords, SaveCategory, SaveLocation, SaveBus, SaveSchedule, SaveBooking, PayBooked
from reservationApp.models import Booking, Category, Location, Bus, Schedule
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import json

context = {
    'page_title' : 'File Management System',
}
#login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')


#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

# @login_required
def home(request):
    context['page_title'] = 'Home'
    context['buses'] = Bus.objects.count()
    context['categories'] = Category.objects.count()
    context['upcoming_trip'] = Schedule.objects.filter(status= 1, schedule__gt = datetime.today()).count()
    return render(request, 'home.html',context)

def registerUser(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home-page')
    context['page_title'] = "Register User"
    if request.method == 'POST':
        data = request.POST
        form = UserRegistration(data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username= username, password = pwd)
            login(request, loginUser)
            return redirect('home-page')
        else:
            context['reg_form'] = form

    return render(request,'register.html',context)

@login_required
def update_profile(request):
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id = request.user.id)
    if not request.method == 'POST':
        form = UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile")
        else:
            context['form'] = form
            
    return render(request, 'manage_profile.html',context)


@login_required
def update_password(request):
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = UpdatePasswords(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile")
        else:
            context['form'] = form
    else:
        form = UpdatePasswords(request.POST)
        context['form'] = form
    return render(request,'update_password.html',context)


@login_required
def profile(request):
    context['page_title'] = 'Profile'
    return render(request, 'profile.html',context)


# Category
@login_required
def category_mgt(request):
    context['page_title'] = "Bus Categories"
    categories = Category.objects.all()
    context['categories'] = categories

    return render(request, 'category_mgt.html', context)

@login_required
def save_category(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            category = Category.objects.get(pk=request.POST['id'])
        else:
            category = None
        if category is None:
            form = SaveCategory(request.POST)
        else:
            form = SaveCategory(request.POST, instance= category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@login_required
def manage_category(request, pk=None):
    context['page_title'] = "Manage Category"
    if not pk is None:
        category = Category.objects.get(id = pk)
        context['category'] = category
    else:
        context['category'] = {}

    return render(request, 'manage_category.html', context)

@login_required
def delete_category(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            category = Category.objects.get(id = request.POST['id'])
            category.delete()
            messages.success(request, 'Category has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'Category has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Category has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Location
@login_required
def location_mgt(request):
    context['page_title'] = "Locations"
    locations = Location.objects.all()
    context['locations'] = locations

    return render(request, 'location_mgt.html', context)

@login_required
def save_location(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            location = Location.objects.get(pk=request.POST['id'])
        else:
            location = None
        if location is None:
            form = SaveLocation(request.POST)
        else:
            form = SaveLocation(request.POST, instance= location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@login_required
def manage_location(request, pk=None):
    context['page_title'] = "Manage Location"
    if not pk is None:
        location = Location.objects.get(id = pk)
        context['location'] = location
    else:
        context['location'] = {}

    return render(request, 'manage_location.html', context)

@login_required
def delete_location(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            location = Location.objects.get(id = request.POST['id'])
            location.delete()
            messages.success(request, 'Location has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'location has failed to delete'
            print(err)

    else:
        resp['msg'] = 'location has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Create your views here.
'''
# myapp/views.py
from django.shortcuts import render

def home(request):
    context['page_title'] = 'Home'
    context['buses'] = Bus.objects.count()
    context['categories'] = Category.objects.count()
    context['upcoming_trip'] = Schedule.objects.filter(status= 1, schedule__gt = datetime.today()).count()
    return render(request, 'home.html',context)
'''
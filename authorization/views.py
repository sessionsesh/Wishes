from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .forms import UserLoginForm
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from desires.models import *
from friends.models import *
from django.db.models import Q


def home_view(request):
	return render(request, "home.html")


def register_view(request):
	if request.user.is_authenticated:
		return redirect('/desires')

	args = {}
	if request.method == 'GET':
		reg_form = UserRegisterForm()
		args['reg_form'] = reg_form
	if request.method == 'POST':
		reg_form = UserRegisterForm(data=request.POST)
		print(reg_form)
		args = {'reg_form': reg_form}
		if reg_form.is_valid():
			new_user = User.objects.create_user(**reg_form.cleaned_data)
			return redirect('/login')
	return render(request, 'register.html', args)


def login_view(request):
	if request.user.is_authenticated:
		return redirect('/desires')
	args = {}
	if request.method == 'GET':
		log_form = UserLoginForm()
		args['log_form'] = log_form
	if request.method == 'POST':
		log_form = UserLoginForm(data=request.POST)
		args['log_form'] = log_form
		if log_form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/desires')
	return render(request, 'login.html', args)


@login_required
def logout_view(request):
	logout(request)
	return redirect('/login')


@login_required
def user_profile_view(request):
	'''
	Show user profile
	'''
	if request.method == 'GET':
		user = request.user
		desires_list = Desire.objects.filter(user=user)
		args = {'user': user,
                    'desires_list': desires_list,
                    'user_profile': True,
                    'friends_count': Relationship.objects.filter(Q(user1=user) | Q(user2=user)).count(),
                    'desires_count': Desire.objects.filter(user=user).count()}
		return render(request, "profile.html", args)


@login_required
def profile_view(request, ID):
	'''
	Show another person profile
	'''
	if request.method == 'GET':
		user = User.objects.get(pk=ID)
		friends_check = Relationship.objects.filter(
			Q(user1=request.user, user2=user) | Q(user1=user, user2=request.user)).exists()
		desires_list = Desire.objects.filter(user=user)
		args = {'user': user,
                    'desires_list': desires_list,
                    'user_profile': False,
                    'friends_check': friends_check,
                    'friends_count': Relationship.objects.filter(Q(user1=user) | Q(user2=user)).count(),
                    'desires_count': Desire.objects.filter(user=user).count()}
		return render(request, "profile.html", args)

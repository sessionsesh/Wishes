from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .forms import UserLoginForm
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_view(request):
	if request.user.is_authenticated:
		return redirect('/users')

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
		return redirect('/users')

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
				return redirect('/users')
	return render(request, 'login.html', args)

@login_required
def logout_view(request):
	logout(request)
	return redirect('/login')

@login_required
def users_view(request):
	users = User.objects.all()
	args = {'users': users,
			'user': request.user.username}
	return render(request, "users.html", args)

from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.Form):
	email = forms.EmailField()
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())

	def clean(self):
		super(UserRegisterForm, self).clean()
		# Check username busyness
		if User.objects.filter(username=self.cleaned_data['username']).exists():
			raise forms.ValidationError("This username is already taken")

		# Check email busyness
		if User.objects.filter(email=self.cleaned_data['email']).exists():
			raise forms.ValidationError("This email is already taken")

		# Check password matching
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password and confirm_password and password != confirm_password:
			raise forms.ValidationError('Passwords doesn\'t match')

		# Delete confirm password from form just not to override save() method
		del self.cleaned_data['confirm_password']

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	
	def clean(self):
		super(UserLoginForm, self).clean()
		if not User.objects.filter(username=self.cleaned_data['username']).exists():
			raise forms.ValidationError("Wrong username")
		

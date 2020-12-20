from django import forms

class DesireForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField(required=False)
	# url = forms.URLField(required=False)
	image_url = forms.URLField(required=False)
	label = forms.CharField(required=False)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import (Desire, Label)
from .forms import *
from django.http.response import HttpResponse


@login_required
def desires_view(request):
    if request.method == 'GET':
        user = request.user
        desires_list = Desire.objects.filter(user=user)
        print(desires_list)
        form = DesireForm()
        args = {'desires_list': desires_list,
                'form': form}
        return render(request, 'desires.html', args)



@login_required
def desire_add(request):
    if request.method == 'POST':
        form = DesireForm(data=request.POST)
        if form.is_valid():
            desire = Desire()
            desire.user = request.user
            desire.name = form.data.get('name')
            if len(form.data.get('description')) > 0:
                desire.description = form.data.get('description')
            desire.image_url = form.data.get('image_url')
            label = Label.objects.create(name=form.data.get('label'))
            desire.label = label
            desire.save()
        args = {'form': form}
        return redirect('/desires')
    else:
        # To avoid add by url
        return redirect('/desires')


@login_required
def desire_delete(request, ID):
    if request.method == 'GET':
        desire = Desire.objects.get(pk=ID)
        if desire.user == request.user:
            desire.delete()
            return redirect('/desires')
        else:
            return HttpResponse("You don't have permission to do this")
    else:
        # To avoid delete by url
        return redirect('/desires')

@login_required
def desire_edit(request, ID):
    if request.method == 'POST':
        form = DesireForm(data=request.POST)
        if form.is_valid():
            desire = Desire.objects.get(pk=ID)
            desire.name = form.data.get('name')
            if form.data.get('description') != '':
                desire.description = form.data.get('description')
            desire.image_url = form.data.get('image_url')
            label = Label.objects.create(name=form.data.get('label'))
            desire.label = label
            desire.save()
        args = {'form': form}
        return redirect('/desires')
    else:
        # To avoid add by url
        return redirect('/desires')
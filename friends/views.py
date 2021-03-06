from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
from django.http.response import HttpResponse


@login_required
def friends_view(request):
    user = request.user
    if request.method == 'GET':
        relationships = Relationship.objects.filter(
            Q(user1=user.id) | Q(user2=user.id))

        # Fill friends list
        friends_list = []
        friend_requests_list = []
        for each in relationships:
            # If GET request user in one field, then add to friends_list user from another field
            if each.user1 == user:
                friends_list.append(each.user2)
            if each.user2 == user:
                # If GET request user is receiver of friend request
                # and he accept request, then add user1 to friends list
                if each.accept2 == True:
                    friends_list.append(each.user1)

                # If GET request user is receiver of friend request
                # and he doesnt accept request, then add user1 to friend requests list
                if each.accept2 == False:
                    friend_requests_list.append(each.user1)

        args = {'friends': friends_list,
                'friend_requests': friend_requests_list}
        return render(request, "friends.html", args)


@login_required
def explore_view(request):
    if request.method == 'GET':
        return render(request, 'explore.html')


"""
TODO:
PROBABLY
From this line will be defined functions needs for js
"""


@login_required
def send_friend_request(request, ID):
    '''Send friend request to user by ID'''
    request_sender = request.user
    if request.method == 'GET':
        # Check that sender send friend request to himself
        if request_sender.id != ID:
            # Check that user with ID exists
            try:
                # Check that user already have some(accepted or not) relationshipwith user where user.id == ID
                rs = Relationship.objects.filter(
                    user2=request_sender, user1=ID)
                if rs.exists():
                    rs = rs.first()
                    if rs.accept2 == True:
                        return render(request, "message.html", {'message':'Вы уже дружите с этим пользователем'})
                    else:
                        return render(request, "message.html", {'message':'Этот пользователь уже отправил вам заявку. Посмотрите во вкладке "Друзья" '})
                else:
                    # Check that sender already send friend request to user with ID
                    if not Relationship.objects.filter(user1=request_sender.id, user2=ID).exists():
                        request_receiver = User.objects.get(pk=ID)
                        new_relationship = Relationship(
                            user1=request_sender, user2=request_receiver, accept1=True)
                        new_relationship.save()
                        return redirect('/friends')
                    else:
                        return render(request, "message.html", {'message':'Вы уже отправили заявку этому пользователю'})
            except User.DoesNotExist:
                return render(request, "message.html", {'message':'Пользователя с таким ID не существует'})
        else:
            return render(request, "message.html", {'message':'Вы не можете отправить заявку самому себе'})


@login_required
def accept_friend_request(request, ID):
    '''Accept friends request from user by ID'''
    user = request.user
    if request.method == 'GET':
        # Check that accepter accept request from himself
        if user.id != ID:
            # Check that friend request was sended
            try:
                relationship_to_accept = Relationship.objects.get(user1=ID)
                # Check that request already accepted
                if relationship_to_accept.accept2 == False:
                    relationship_to_accept.accept2 = True
                    relationship_to_accept.save()

                    return redirect('/friends')
                else:
                    return render(request, "message.html", {'message':'Вы уже друзья'})
            except Relationship.DoesNotExist:
                return render(request, "message.html", {'message':'Такой заявки не существует'})
        else:
            return render(request, "message.html", {'message':'Вы не можете принять заявку от самого себя'})


@login_required
def dissolve_relationship(request, ID):
    '''Dissolve realtionship with user with ID even if receiver user didn\'t accept friend request.
    Relationship dissovler can be user, who send friend request(user1) and also can be user, who receive friend request.
    '''
    dissolve_initiator = request.user
    if request.method == 'GET':
        try:
            # If GET request sender is user1 in the db table, then user2.id = ID,
            # else GET sender is user2 in the db table and user1.id = ID
            relationship_to_dissolve = \
                Relationship.objects.get((Q(user1=ID) | Q(user2=ID)) & (
                    Q(user1=dissolve_initiator) | Q(user2=dissolve_initiator)))
            relationship_to_dissolve.delete()
            return redirect('/friends')
        except Relationship.DoesNotExist:
            return render(request, "message.html", {'message':'Вы не дружите с этим пользователем'})


"""
From this line will be defined functions needs for ajax
"""


@login_required
def explore_users(request, regexp):
    if request.method == 'GET':
        regexp = r'' + regexp
        users_list = User.objects.filter(username__iregex=regexp).exclude(
            pk=request.user.id)  # excluding user, who makes request
        args = {'users': users_list}
        return render(request, 'users.html', args)


@login_required
def explore_users_empty(request):
    if request.method == 'GET':
        args = {'users': User.objects.all().exclude(pk=request.user.id)}
        return render(request, 'users.html', args)

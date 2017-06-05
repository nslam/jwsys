from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    if username is None:
        return HttpResponse('username cannot be none!')
    if password is None:
        return HttpResponse('Password cannot be none!')
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse('Password is not correct!')
    return HttpResponse('Login successed!')


@login_required
def setPassword(request):
    user = authenticate(username=request.user.username, password=request.POST['oldPassword'])
    if user is None:
        return HttpResponse('Password is wrong!')
    user.set_password(request.POST['newPassword'])
    return HttpResponse('Password changed!')



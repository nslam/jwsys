# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from basicInfo.models import *

# Create your models here.
class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    content = models.CharField(max_length=1000, default='')
    is_top = models.IntegerField(default=0)
    is_best = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    layer_number = models.IntegerField(default=0)
    files = models.FileField(upload_to='files/')

class Reply(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    replier = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.CharField(max_length=256, default='')
    time = models.DateTimeField(auto_now_add=True)

class Notice(models.Model):
    instructor = models.ForeignKey("basicInfo.Instructor", null=True, on_delete=models.SET_NULL)
    content = models.CharField(max_length=1000, default='')
    time = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE,related_name='senders')
    receiver = models.ForeignKey(User, on_delete= models.CASCADE,related_name='receivers')
    content = models.CharField(max_length=1000, default='')
    is_read = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return u'%s %s %s %d %s' % (
        self.sender.username, self.receiver.name, self.content, self.is_read, self.time.strftime("%Y-%m-%d"))
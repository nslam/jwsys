# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import Http404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from basicInfo.views import getType
from django.template import Template, Context
from django.template.loader import get_template
import math


# Create your views here.

@login_required
def manageNotice(request):
    user = request.user
    type = getType(user)
    Posts = []
    Notices = []
    if request.method == 'POST':
        id = request.POST['notice_id']
        notice = Notice.objects.get(id=id)
        notice.delete()
    # 显示界面
    if type == 'Student':
        status = 'Unable to operate on a notice!You are not an instructor!'
        is_teacher = 0
        is_manager = 0
        if type == 'Manager':
            typestr = 'manager'
            is_manager = 1
        elif type == 'Student':
            typestr = 'student'
        else:
            typestr = 'instructor'
            is_teacher = 1
        posts = Post.objects.all().order_by("-is_top", "-time")
        notices = Notice.objects.all().order_by("-time")[0:2]
        for var in posts:
            Posts.append({'id': var.id, 'poster': var.poster.username, 'time': var.time, 'title': var.title})
        for var in notices:
            Notices.append({'instructor': var.instructor.user.username, 'content': var.content})
        return render(request, 'bbs_homepage.html',
                      {'is_teacher': is_teacher, 'is_manager': is_manager, 'type': typestr, 'userid': user.id,
                       'username': user.username, 'post_list': Posts, 'notices': Notices, 'status': status})  # 主界面
    ret_notice = []
    if type == 'Instructor':
        inst_notice = Notice.objects.filter(instructor=user.instructor)
    else:
        inst_notice = Notice.objects.all()
    for n in inst_notice:
        ret_notice.append({'id': n.id, 'instructor': n.instructor.user.username, 'time': n.time, 'content': n.content})
    return render(request, 'manage_notice.html', {'notices': ret_notice, 'username': user.username, 'userid': user.id})


@login_required
def postNotice(request):
    user = request.user
    type = getType(user)
    usern = user.username
    Posts = []
    Notices = []
    if type != 'Instructor':
        # 主界面,小窗口：（不是教师，发公告失败）
        status = 'Unable to operate on a notice!You are not an instructor!'
        is_teacher = 0
        is_manager = 0
        if type == 'Manager':
            typestr = 'manager'
            is_manager = 1
        elif type == 'Student':
            typestr = 'student'
        else:
            typestr = 'instructor'
            is_teacher = 1
        posts = Post.objects.all().order_by("-is_top", "-time")
        notices = Notice.objects.all().order_by("-time")[0:2]
        for var in posts:
            Posts.append({'id': var.id, 'poster': var.poster.username, 'time': var.time, 'title': var.title})
        for var in notices:
            Notices.append({'instructor': var.instructor.user.username, 'content': var.content})
        return render(request, 'bbs_homepage.html',
                      {'is_teacher': is_teacher, 'is_manager': is_manager, 'type': typestr, 'userid': user.id,
                       'username': usern, 'post_list': Posts, 'notices': Notices, 'status': status})  # 主界面
    else:
        if request.method == 'GET':
            # 公告存入数据库
            errors = []
            text = request.GET['notice']
            # 检测是不是post
            # 如果提交了一个空的表单，就会返回相应的错误信息
            if text == '':
                errors.append('请输入发送的消息')
            # 如果不出错的话就将数据存到数据库
            if not errors:
                msg_text = request.POST.get('send_msg')  # 得到短消息的文本
                # 初始化一条消息的元组
                notice = Notice.objects.create(
                    instructor=user.instructor,
                    content=text
                )
                notice.save()
                return bbsMain(request)
            else:
                status = 'Noitce cannot be empty!'
                is_teacher = 0
                is_manager = 0
                if type == 'Manager':
                    typestr = 'manager'
                    is_manager = 1
                elif type == 'Student':
                    typestr = 'student'
                else:
                    typestr = 'instructor'
                    is_teacher = 1
                posts = Post.objects.all().order_by("-is_top", "-time")
                notices = Notice.objects.all().order_by("-time")[0:2]
                for var in posts:
                    Posts.append({'id': var.id, 'poster': var.poster.username, 'time': var.time, 'title': var.title})
                for var in notices:
                    Notices.append({'instructor': var.instructor.user.username, 'content': var.content})
                return render(request, 'bbs_homepage.html',
                              {'is_teacher': is_teacher, 'is_manager': is_manager, 'type': typestr, 'userid': user.id,
                               'username': usern, 'post_list': Posts, 'notices': Notices, 'status': status})  # 主界面


@login_required
def bbsMain(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    usern = user.username
    Posts = []
    Notices = []
    is_teacher = 0
    is_manager = 0
    if type == 'Manager':
        typestr = 'manager'
        is_manager = 1
    elif type == 'Student':
        typestr = 'student'
    else:
        typestr = 'instructor'
        is_teacher = 1
    posts = Post.objects.all().order_by("-is_top", "-time")
    notices = Notice.objects.all().order_by("-time")[0:2]
    for var in posts:
        if var.is_best == 0:
            title = var.title
        else:
            title = '[best]:' + var.title
        Posts.append({'id': var.id, 'poster': var.poster.username, 'time': var.time, 'title': title})
    for var in notices:
        Notices.append({'instructor': var.instructor.user.username, 'content': var.content})
    return render(request, 'bbs_homepage.html',
                  {'is_teacher': is_teacher, 'is_manager': is_manager, 'type': typestr, 'userid': user.id,
                   'username': usern, 'post_list': Posts, 'notices': Notices, 'status': 'true'})  # 主界面


@login_required
def releasePost(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    errors = []
    if request.method == 'POST':
        if request.POST['post_title'] == '':
            errors.append('请输入标题')
        elif request.POST['post_content'] == '':
            errors.append('请输入内容')
        if not errors:
            ptitle = request.POST['post_title']
            pcontent = request.POST['post_content']
            post = Post.objects.create(
                poster=user,
                title=ptitle,
                content=pcontent
            )
            post.save()
            return bbsMain(request)

    html = get_template('release_post.html').render({
        'errors': errors,
        'posterid': user.id
    })
    return HttpResponse(html)


@login_required
def lookAndReply(request):
    user = User.objects.get(id=request.user.id)
    errors = []
    if request.method == 'POST':
        post_id = request.POST['post_id']
        if request.POST['reply_content'] == '':
            errors.append('请输入内容')
        if not errors:
            rcontent = request.POST['reply_content']
            reply = Reply.objects.create(
                post=Post.objects.get(id=post_id),
                replier=user,
                content=rcontent,
            )
            reply.save()
            return get_post(request, post_id)
    html = get_template('release_reply.html').render({
        'errors': errors,
        'postid': request.GET['post_id']
    })
    return HttpResponse(html)


@login_required
def lookMessage(request):
    user = request.user
    type = getType(user)
    usern = user.username
    Messages = []
    message = Message.objects.filter(receiver=user)
    for m in message:
        Messages.append({'is_read': m.is_read, 'sender': m.sender.username, 'time': m.time, 'content': m.content})
    for item in message:
        item.is_read = 1
        item.save()
    return render(request, 'look_message.html', {'username': usern, 'message_list': Messages})  # 消息盒子界面


@login_required
def sendMessage(request):
    user = request.user
    errors = []
    # 检测是不是post
    if request.method == "POST":
        receivername = request.POST.get('receivername')
        sendername = request.POST.get('sendername')
        # 如果提交了一个空的表单，就会返回相应的错误信息
        if request.POST.get('send_msg', '') == '':
            errors.append('请输入发送的消息')
        # 如果不出错的话就将数据存到数据库
        if not errors:
            msg_text = request.POST.get('send_msg')  # 得到短消息的文本
            # 初始化一条消息的元组
            message = Message.objects.create(
                sender=User.objects.get(username=sendername),
                receiver=User.objects.get(username=receivername),
                is_read=0,
                content=msg_text
            )
            message.save()  # 存到数据库，相当于commit
            return bbsMain(request)
            # 提交空表单的错误和刷新会返回发消息的界面
    # return HttpResponse("hehe")
    receivername = request.GET['receivername']
    sendername = request.GET['sendername']
    html = get_template('send_message.html').render({
        'errors': errors,
        'receivername': receivername,
        'sendername': sendername,
    })
    return HttpResponse(html)


@login_required
def managePost(request):
    user = request.user
    type = getType(user)
    if type == 'Manager':
        if request.method == 'POST':
            if 'reply_id' in request.POST:
                rid = request.POST['reply_id']
                reply = Reply.objects.get(id=rid)
                reply.delete()
            if 'post_id' in request.POST:
                pid = request.POST['post_id']
                post = Post.objects.get(id=pid)
                post.delete()
        ret_post = []
        ret_reply = []
        posts = Post.objects.all()
        replies = Reply.objects.all()
        for p in posts:
            ret_post.append({'id': p.id, 'title': p.title, 'content': p.content, 'time': p.time})
        for r in replies:
            ret_reply.append({'id': r.id, 'time': r.time, 'post_title': r.post.title, 'content': r.content})
        return render(request, 'user_manage_post.html',
                      {'username': user.username, 'userid': user.id, 'posts': ret_post, 'replies': ret_reply})
    else:
        if request.method == 'POST':
            if 'reply_id' in request.POST:
                rid = request.POST['reply_id']
                reply = Reply.objects.get(id=rid)
                reply.delete()
            if 'post_id' in request.POST:
                pid = request.POST['post_id']
                post = Post.objects.get(id=pid)
                post.delete()
        ret_post = []
        ret_reply = []
        posts = Post.objects.filter(poster=user)
        replies = Reply.objects.filter(replier=user)
        for p in posts:
            ret_post.append({'id': p.id, 'title': p.title, 'content': p.content, 'time': p.time})
        for r in replies:
            ret_reply.append({'id': r.id, 'time': r.time, 'post_title': r.post.title, 'content': r.content})
        return render(request, 'user_manage_post.html',
                      {'username': user.username, 'userid': user.id, 'posts': ret_post, 'replies': ret_reply})


@login_required
def setTop(request):
    user = request.user
    type = getType(user)
    post = {}
    reply = []
    is_manager = 0
    if type == 'Manager':
        is_manager = 1
    if request.method == 'POST':
        if type != 'Manager':
            return HttpResponse('Fxxk!stop such actions!')
        ppost = Post.objects.get(id=request.POST['post_id'])
        if ppost.is_top == 0:
            ppost.is_top = 1
        else:
            ppost.is_top = 0
        ppost.save()
        post['id'] = ppost.id
        post['title'] = ppost.title
        post['content'] = ppost.content
        post['poster'] = ppost.poster.username
        post['time'] = ppost.time
        replies = Reply.objects.filter(post=ppost).order_by("time")
        for r in replies:
            reply.append({'id': r.id, 'replier': r.replier.username, 'replier_id': r.replier.id, 'content': r.content,
                          'time': r.time})
        return render(request, 'bbs_post.html',
                      {'is_manager': is_manager, 'post': post, 'replies': reply, 'status': 'Operation succeed!'})
    else:
        if 'post_id' not in request.GET:
            return HttpResponse('Fxxk!stop such actions!')
        ppost = Post.objects.get(id=request.GET['post_id'])
        post['id'] = ppost.id
        post['title'] = ppost.title
        post['content'] = ppost.content
        post['poster'] = ppost.poster.username
        post['time'] = ppost.time
        replies = Reply.objects.filter(post=ppost).order_by("time")
        for r in replies:
            reply.append({'id': r.id, 'replier': r.replier.username, 'replier_id': r.replier.id, 'content': r.content,
                          'time': r.time})
        return render(request, 'bbs_post.html',
                      {'is_manager': is_manager, 'post': post, 'replies': reply, 'status': 'true'})


@login_required
def setBest(request):
    user = request.user
    type = getType(user)
    post = {}
    reply = []
    is_manager = 0
    if type == 'Manager':
        is_manager = 1
    if request.method == 'POST':
        if type != 'Manager':
            return HttpResponse('Fxxk!stop such actions!')
        ppost = Post.objects.get(id=request.POST['post_id'])
        if ppost.is_best == 0:
            ppost.is_best = 1
        else:
            ppost.is_best = 0
        ppost.save()
        post['id'] = ppost.id
        post['title'] = ppost.title
        post['content'] = ppost.content
        post['poster'] = ppost.poster.username
        post['time'] = ppost.time
        replies = Reply.objects.filter(post=ppost).order_by("time")
        for r in replies:
            reply.append({'id': r.id, 'replier': r.replier.username, 'replier_id': r.replier.id, 'content': r.content,
                          'time': r.time})
        return render(request, 'bbs_post.html',
                      {'is_manager': is_manager, 'post': post, 'replies': reply, 'status': 'Operation succeed!'})
    else:
        if 'post_id' not in request.GET:
            return HttpResponse('Fxxk!stop such actions!')
        ppost = Post.objects.get(id=request.GET['post_id'])
        post['id'] = ppost.id
        post['title'] = ppost.title
        post['content'] = ppost.content
        post['poster'] = ppost.poster.username
        post['time'] = ppost.time
        replies = Reply.objects.filter(post=ppost).order_by("time")
        for r in replies:
            reply.append({'id': r.id, 'replier': r.replier.username, 'replier_id': r.replier.id, 'content': r.content,
                          'time': r.time})
        return render(request, 'bbs_post.html',
                      {'is_manager': is_manager, 'post': post, 'replies': reply, 'status': 'true'})


@login_required
def deletePostManager(request):
    user = request.user
    type = getType(user)
    if request.method == 'POST':
        if type != 'Manager':
            return HttpResponse('Fxxk!stop such actions!')
        ppost = Post.objects.get(id=request.POST['post_id'])
        ppost.delete()
        return bbsMain(request)
    else:
        return bbsMain(request)


@login_required
def sendMessageTo(request):
    user = request.user
    if 'receiver_id' not in request.GET:
        receivername = request.GET['receivername']
        sendername = request.GET['sendername']
        html = get_template('send_message.html').render({
            'errors': [],
            'receivername': receivername,
            'sendername': sendername,
        })
        return HttpResponse(html)
    receiver_id = request.GET['receiver_id']
    receiver = User.objects.get(id=receiver_id)
    receivername = receiver.username
    sendername = user.username
    html = get_template('send_message.html').render({
        'errors': [],
        'receivername': receivername,
        'sendername': sendername,
    })
    return HttpResponse(html)


@login_required
def deleteReply(request):
    user = request.user
    type = getType(user)
    post = {}
    reply = []
    is_manager = 0
    if type == 'Manager':
        is_manager = 1
    if request.method == 'POST':
        if type != 'Manager':
            return HttpResponse('Fxxk!stop such actions!')
        ppost = Post.objects.get(id=request.POST['post_id'])
        delreply = Reply.objects.get(id=request.POST['reply_id'])
        delreply.delete()
        ppost.save()
        post['id'] = ppost.id
        post['title'] = ppost.title
        post['content'] = ppost.content
        post['poster'] = ppost.poster.username
        post['time'] = ppost.time
        replies = Reply.objects.filter(post=ppost).order_by("time")
        for r in replies:
            reply.append({'id': r.id, 'replier': r.replier.username, 'replier_id': r.replier.id, 'content': r.content,
                          'time': r.time})
        return render(request, 'bbs_post.html',
                      {'is_manager': is_manager, 'post': post, 'replies': reply, 'status': 'true'})
    else:
        if 'post_id' not in request.GET:
            return HttpResponse('Fxxk!stop such actions!')
        ppost = Post.objects.get(id=request.GET['post_id'])
        ppost.save()
        post['id'] = ppost.id
        post['title'] = ppost.title
        post['content'] = ppost.content
        post['poster'] = ppost.poster.username
        post['time'] = ppost.time
        replies = Reply.objects.filter(post=ppost).order_by("time")
        for r in replies:
            reply.append({'id': r.id, 'replier': r.replier.username, 'replier_id': r.replier.id, 'content': r.content,
                          'time': r.time})
        return render(request, 'bbs_post.html',
                      {'is_manager': is_manager, 'post': post, 'replies': reply, 'status': 'true'})


def get_post(request, offset):
    user = request.user
    type = getType(user)
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    # 测试用的，添加了两个p和r数据
    # 主要逻辑，根据offset找出相应的post
    post = Post.objects.filter(id=offset)
    # 根据post找出相应的replies
    replies = Reply.objects.filter(post=post)
    # 渲染帖子页面
    if type != 'Manager':
        html = get_template('bbs_post.html').render({
            'post': post[0],
            'replies': replies,
            'is_manager': 0,
            'status': 'true',
        })
    else:
        html = get_template('bbs_post.html').render({
            'post': post[0],
            'replies': replies,
            'is_manager': 1,
            'status': 'true',
        })
    return HttpResponse(html)


@login_required
def manageUser(request):
    user = request.user
    type = getType(user)
    if type != 'Manager':
        return HttpResponse('Fxxk!stop such actions!')
    if request.method == 'POST':
        user_id = request.POST['user_id']
        if 'reply_id' in request.POST:
            rid = request.POST['reply_id']
            reply = Reply.objects.get(id=rid)
            reply.delete()
        if 'post_id' in request.POST:
            pid = request.POST['post_id']
            post = Post.objects.get(id=pid)
            post.delete()
    if 'user_id' in request.GET:
        user_id = request.GET['user_id']
    ret_post = []
    ret_reply = []
    posts = Post.objects.filter(poster=User.objects.get(id=user_id))
    replies = Reply.objects.filter(replier=User.objects.get(id=user_id))
    for p in posts:
        ret_post.append({'id': p.id, 'title': p.title, 'content': p.content, 'time': p.time})
    for r in replies:
        ret_reply.append({'id': r.id, 'time': r.time, 'post_title': r.post.title, 'content': r.content})
    return render(request, 'manage_user.html',
                  {'username': user.username, 'userid': user_id, 'posts': ret_post, 'replies': ret_reply})


@login_required
def search_post(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    usern = user.username
    notices = Notice.objects.all()[0:2]
    # 主逻辑部分
    # 过去搜索键值
    key = request.GET.get('search_key', '')
    # 得到当前在使用搜索的用户
    userid = request.GET.get('userid', 22389)
    # 得到题目包含关键字的帖子们
    posts = Post.objects.filter(title__contains=key).order_by("-is_top", "-time")
    # 渲染主界面，在搜索完后返回到这个界面
    Posts = []
    Notices = []
    is_teacher = 0
    is_manager = 0
    if type == 'Manager':
        typestr = 'manager'
        is_manager = 1
    elif type == 'Student':
        typestr = 'student'
    else:
        typestr = 'instructor'
        is_teacher = 1
    notices = Notice.objects.all().order_by("-time")[0:2]
    for var in posts:
        if var.is_best == 0:
            title = var.title
        else:
            title = '[best]:' + var.title
        Posts.append({'id': var.id, 'poster': var.poster.username, 'time': var.time, 'title': title})
    for var in notices:
        Notices.append({'instructor': var.instructor.user.username, 'content': var.content})
    return render(request, 'bbs_homepage.html',
                  {'is_teacher': is_teacher, 'is_manager': is_manager, 'type': typestr, 'userid': user.id,
                   'username': usern, 'post_list': Posts, 'notices': Notices, 'status': 'true'})  # 主界面

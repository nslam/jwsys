from django.shortcuts import render, redirect, reverse, render_to_response
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from basicInfo.models import Student, Instructor, Course, Takes
from courseArrange.models import Teaches, Section
from basicInfo.views import getType
import math
import operator
import random


@login_required
def dotest(request, paper_id):
	user=request.user
	stu=user.student #获取学生对象
	paper=Paper.objects.get(id = paper_id) #获取试卷对象
	p=paper
	question_list=paper.question_set.all()	#查询这个试卷的所有题目
	question_xz_list=[]
	question_pd_list=[]
	for ques in question_list:
		if ques.q_type == 'xz':
			question_xz_list.append(ques)
		else:
			question_pd_list.append(ques)

	
	if request.method == 'GET':
		return render(request, 'test.html', {'paper':paper,'question_pd_list':question_pd_list,'question_xz_list': question_xz_list})
	else :
		sheet = Sheet.objects.create(student_id=stu.id,paper_id=p.id) #建立答卷对象
		xz_score=0	#选择题总分
		pd_score=0	#判断题总分
		for pd in question_pd_list :
			q_id = ''
			q_id = str(pd.id)
			if q_id in request.POST:	#判断是否作答
				res = request.POST[q_id]
				if pd.answer == str(res):	#答案正确
					obj = {'question':pd,'sheet':sheet,'ans':res,'mark':1}
					pd_score=pd_score+1
				else :	#答案错误
					obj = {'question':pd,'sheet':sheet,'ans':res,'mark':0}
			else :	#没有作答
				obj = {'question':pd,'sheet':sheet,'ans':'N','mark':0}
			_obj = Reply.objects.create(**obj)	#建立回答对象

		for xz in question_xz_list :
			q_id = ''
			q_id = str(xz.id)
			if q_id in request.POST:
				res = request.POST[q_id]
				if xz.answer == str(res):
					obj = {'question':xz,'sheet':sheet,'ans':res,'mark':1}
					xz_score=xz_score+1
				else :
					obj = {'question':xz,'sheet':sheet,'ans':res,'mark':0}
			else :
				obj = {'question':xz,'sheet':sheet,'ans':'N','mark':0}	
			_obj = Reply.objects.create(**obj)

		sheet.tot_mark=xz_score+pd_score	#记录总分
		sheet.xz_mark=xz_score
		sheet.pd_makr=pd_score
		sheet.save()
			
		return HttpResponseRedirect('/onlinetest/student1/')

@login_required
def student1(request):
	user = request.user
	stu = user.student
	
	ta = Takes.objects.filter(student_id=stu.id)
	takes=[]
	for t in ta:
		takes.append(t.section.course)
	sPaper = Paper.objects.all()
	stuPaper = []
	for s in sPaper:
		if s.course in takes:
			stuPaper.append(s)
	myPaper = []
	for ss in stuPaper:
		if ss.status == 'o':
			myPaper.append(ss)
	pP = Sheet.objects.filter(student_id=stu.id)
	passedPaper = []
	for p in pP:
		passedPaper.append(p.paper)
	waitPaper = []
	for paper in myPaper:
		if paper not in passedPaper:
			waitPaper.append(paper)
	allpaper=[]
	for paper in stuPaper:
		if paper not in passedPaper:
			allpaper.append(paper)
	
	else:
		return render(request,'student1.html',{'user':user,'allpaper_list':allpaper,'mypaper_list':waitPaper})

@login_required
def student2(request):
	user = request.user
	stu = user.student
	
	ta = Takes.objects.filter(student_id=stu.id)
	takes=[]
	for t in ta:
		takes.append(t.section.course)
	allcourse_score_list = Sheet.objects.filter(student_id = stu.id)
	
	return render(request,'student2.html',{'user':user,'course_list':takes,'allcourse_score_list':allcourse_score_list})

@login_required
def teacher1(request):
	user = User.objects.get(id=request.user.id)
	ins = user.instructor
	
	tches = Teaches.objects.filter(instructor_id = ins.id)
	teaches = []
	for t in tches:
		teaches.append(t.section.course)
	iPaper = Paper.objects.all()
	instruPaper = []
	for p in iPaper:
		if p.course in teaches:
			instruPaper.append(p)
	myPaper = []
	myPaper = Paper.objects.filter(instructor_id = ins.id)
	
	return render(request,'teacher1.html',{'user':user,'allpaper_list':instruPaper,'mypaper_list':myPaper})

@login_required
def deletepaper(request,pid):
	user = request.user
	ins = user.instructor
	type = getType(user)
	if type != 'Instructor':
		return HttpResponse('You are not an instructor!')

	paper = Paper.objects.get(id=pid)
	paper.delete()

	tches = Teaches.objects.filter(instructor_id = ins.id)
	teaches = []
	for t in tches:
		teaches.append(t.section.course)
	
	iPaper = Paper.objects.all()
	instruPaper=[]
	for i in iPaper:
		if i.course in teaches:
			instruPaper.append(i)
	myPaper = Paper.objects.filter(instructor_id=ins.id)
	return render(request,'teacher1.html',{'user':user,'allpaper_list':instruPaper,'mypaper_list':myPaper})



@login_required
def teacher3(request):
	ques = Question.objects.all()
	tuser = request.user
	ins = tuser.instructor
	myques = Question.objects.filter(instructor_id = ins.id)
	return render(request,'teacher3.html',{'allquestion_list': ques,'user':tuser,'myquestion_list':myques})

@login_required	
def newpdquestion(request):
    '''点击 添加新试题，在小框框中输入后，点击 确认修改，会调用该函数'''
    	
    if 'course_name' not in request.POST:
    	error = '没有输入课程！'
    	return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
    else:
    	qcours = request.POST['course_name']
    	qcourse = Course.objects.get(title = qcours)
    	
    if 'question_title' not in request.POST:
    	error = '没有输入题目内容！'
    	return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
    else:
    	qtitle = request.POST['question_title']
    	
    if 'question_ans' not in request.POST:
    	error = '没有输入题目答案！'
    	return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
    else:
    	qans = request.POST['question_ans']	
    	
    tname = User.objects.get(id=request.user.id)
    			
    if 'test_point' not in request.POST:
    	error = '没有输入考点！'
    	return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
    else:
    	qtestpoi = request.POST['test_point']
    	
    if 'difficulty' not in request.POST:
    	error = '没有输入题目难度！'
    	return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
    else:
    	qdif = request.POST['difficulty']
    #~检验完毕
    
    new = Question()
    new.course = qcourse 
    new.instructor = tname.instructor
    new.title = qtitle 
    new.q_type = 'pd' 
    new.status = 'o' 
    new.test_point = qtestpoi 
    new.answer = qans 
    new.difficulty = qdif
    new.save()#插入数据库
    #insertSuccess = True
    ques = Question.objects.all()
    tuser = request.user
    ins = tuser.instructor
    myques = Question.objects.filter(instructor_id  = ins.id)
    return render(request,'teacher3.html',{'allquestion_list': ques,'user':tuser,'myquestion_list':myques })

@login_required
def newxzquestion(request):
	if 'course_name' not in request.POST:
		error = '没有输入课程！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		qcours = request.POST['course_name']
		qcourse = Course.objects.get(title = qcours)

	if 'question_title' not in request.POST:
		error = '没有输入题目内容！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		qtitle = request.POST['question_title']
		
	if 'question_ans' not in request.POST:
		error = '没有输入题目答案！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		qans = request.POST['question_ans']	
		
	if 'choice1' not in request.POST:
		error = '没有输入选项A！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		ca = request.POST['choice1']	
		
	if 'choice2' not in request.POST:
		error = '没有输入选项B！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		cb = request.POST['choice2']	
		
	if 'choice3' not in request.POST:
		error = '没有输入选项C！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		cc = request.POST['choice3']	
		
	if 'choice4' not in request.POST:
		error = '没有输入选项D！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		cd = request.POST['choice4']	
		
	tname = User.objects.get(id=request.user.id)
				
	if 'test_point' not in request.POST:
		error = '没有输入考点！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		qtestpoi = request.POST['test_point']
		
	if 'difficulty' not in request.POST:
		error = '没有输入题目难度！'
		return render(request,'teacher3.html',{'error':error})#返回本页面，附加错误信息	
	else:
		qdif = request.POST['difficulty']
	#~检验完毕

	new = Question()
	new.course = qcourse 
	new.instructor = tname.instructor 
	new.title = qtitle 
	new.q_type = 'xz' 
	new.status = 'o'
	new.choice1=ca 
	new.choice2=cb 
	new.choice3=cc 
	new.choice4=cd 
	new.test_point = qtestpoi
	new.answer = qans
	new.difficulty = qdif
	new.save()
	
	#newTable2 = 
	#newTable2.save()#插入数据库
	#insertSuccess = True
	ques = Question.objects.all()
	tuser = request.user
	ins = tuser.instructor
	myques = Question.objects.filter(instructor_id  = ins.id)
	return render(request,'teacher3.html',{'allquestion_list': ques,'user':tuser,'myquestion_list':myques })#,{'success':insertSuccess}

@login_required	
def deletequestion(request,did):
    
    if did:
        x=Question.objects.get(id= did)
        x.delete()
        ques = Question.objects.all()
        tuser = request.user
        ins = tuser.instructor
        myques = Question.objects.filter(instructor_id  = ins.id)
        return render(request,'teacher3.html',{'allquestion_list': ques,'user':tuser,'myquestion_list':myques })
    else:
    	return render(reuqest,'teahcer3.html',{'error':'未获得题目id'})#未得到题目信息

@login_required		
def changequestion(request,updID):
    if  updID:
        theQues = Question.objects.get(id=updID) 
        if theQues :
            pass
        else:
            error = '未获得题目id'
            return render(reuqest,'teacher3.html',{'error':error})#error
    if 'course_name' in request.POST:
    	qcours = request.POST['course_name']
    	qcourse = Course.objects.get(title = qcours)
    	theQues.course = qcourse		
    if 'question_title' in request.POST:
    	qtitle = request.POST['question_title']
    	theQues.title = qtitle
    if 'question_ans'in request.POST:	
        qans = request.POST['question_ans']
        theQues.answer = qans
    if 'test_point'in request.POST:
    	qtestpoi= request.POST['test_point']
    	theQues.test_point=qtestpoi 
    if 'teacher_name' in request.POST:
    	tnam = request.POST['teacher_name']
    	tname = User.objects.get(username=tnam)
    	theQues.instructor= tname.instructor
    if 'choice1' in request.POST:
    	ca = request.POST['choice1']	
    	theQues.choice1 = ca
    if 'choice2' in request.POST:
    	cb = request.POST['choice1']	
    	theQues.choice2 = cb
    if 'choice3' in request.POST:
    	cc = request.POST['choice1']	
    	theQues.choice3 = cc
    if 'choice4' in request.POST:
    	cd = request.POST['choice1']	
    	theQues.choice4 = cd
    if 'difficulty' in request.POST:
    	qdif = request.POST['difficulty']
    	theQues.difficulty =qdif
    theQues.save()

    ques = Question.objects.all()
    tuser = request.user
    ins = tuser.instructor
    myques = Question.objects.filter(instructor_id  = ins.id)
    return render(request,'teacher3.html',{'allquestion_list': ques,'user':tuser,'myquestion_list':myques })

@login_required	
def searchquestion(request):
    
    if 'question_title' not in request.POST :#attr等名字由网页页面决定
        error = '没有输入题目！'
        return render(reuqest,'teahcer3.html',{'error':error})#返回本页面，附加错误信息	
    else:
        tit = request.POST['question_title']
    ques = Question.objects.filter(title__contains = tit)#没有搜到的话为空

    tuser = request.user
    ins = tuser.instructor
    myques = Question.objects.filter(instructor_id  = ins.id)
    return render(request,'teacher3.html',{'user':tuser,'myquestion_list': myques,'allquestion_list':ques})

@login_required
def paper1(request):
	user = request.user
	type = getType(user)
	if type != 'Instructor':
		return HttpResponse('You are not an instructor!')
	else:
		return render(request,'paper1.html',{'user':user})

@login_required
def paper2(request,paperId):
	user = request.user
	ins=user.instructor
	paper = Paper.objects.get(id=paperId)
	#question = Question.objects.get(id=questionId)
	tches = Teaches.objects.filter(instructor_id=ins.id)
	teacher = []
	for t in tches:
		teacher.append(t.section.course)
	
	questions = Question.objects.filter(course_id = paper.course_id)
	paperques = paper.question_set.all()
	xz = []
	pd = []
	for q in paperques:
		if q.q_type == 'xz':
			xz.append(q)
		else:
			pd.append(q)
	for p in questions:
		if p in paperques:
			del(p)
	type = getType(user)
	if type != 'Instructor':
		return HttpResponse('You are not an instructor!')
	else:
		return render(request,'paper2.html',
			{'user':user,'paper':paper,'question_pd_list':pd,'question_xz_list':xz,'allquestion_list':questions})

def paperchinfo(request,paperId):
	user = request.user
	type = getType(user)
	if type != 'Instructor':
		return HttpResponse('You are not an instructor!')
	if request.method == 'POST':
		p=Paper.objects.get(id=paperId)
		p.name = request.POST['paper_name']
		cour_name = request.POST['course_name']
		p.course = Course.objects.get(title = cour_name)
		#ins_name = request.POST['teacher_name']
		#p.instructor = User.objects.get(username = ins_name).instructor
		p.difficulty = request.POST['difficulty']
		#p.choice_num = request.POST['choiceNum']
		#p.judge_num = request.POST['judgeNum']
		#p.status = request.POST['status']
		p.limit_time = request.POST['limit_time']
		p.save()

		ins=user.instructor
		paper = Paper.objects.get(id=paperId)
		#question = Question.objects.get(id=questionId)
		tches = Teaches.objects.filter(instructor_id=ins.id)
		teacher = []
		for t in tches:
			teacher.append(t.section_course)
		qtions = Question.objects.all()
		questions=[]
		for f in qtions:
			if f.course in teacher:
				questions.append(f)
		paperques = paper.question_set.all()
		xz = []
		pd = []
		for q in paperques:
			if q.q_type == 'xz':
				xz.append(q)
			else:
				pd.append(q)
		for p in questions:
			if p in paperques:
				del(p)
	
		return render(request,'paper2.html',
			{'user':user,'paper':paper,'question_pd_list':pd,'question_xz_list':xz,'allquestion_list':questions})

@login_required
def paperadd(request,paperId,questionId):
	ques = Question.objects.get(id = questionId)
	pap = Paper.objects.get(id = paperId)
	ques.paper.add(pap)
	user = request.user
	ins=user.instructor
	paper = Paper.objects.get(id=paperId)
	questions = Question.objects.filter(course_id = paper.course_id)
	paperques = paper.question_set.all()
	xz = []
	pd = []
	for q in paperques:
		if q.q_type == 'xz':
			xz.append(q)
		else:
			pd.append(q)
	for p in questions:
		if p in paperques:
			del(p)
	type = getType(user)
	if type != 'Instructor':
		return HttpResponse('You are not an instructor!')
	else:
		return render(request,'paper2.html',
			{'user':user,'paper':paper,'question_pd_list':pd,'question_xz_list':xz,'allquestion_list':questions})


@login_required
#delete questions from paper
def paperdelete(request,paperId,questionId):
	ques = Question.objects.get(id = questionId)
	pap = Paper.objects.get(id = paperId)
	ques.paper.remove(pap)
	user = request.user
	ins=user.instructor
	paper = Paper.objects.get(id=paperId)
	questions = Question.objects.filter(course_id = paper.course_id)
	paperques = paper.question_set.all()
	xz = []
	pd = []
	for q in paperques:
		if q.q_type == 'xz':
			xz.append(q)
		else:
			pd.append(q)
	for p in questions:
		if p in paperques:
			del(p)
	type = getType(user)
	if type != 'Instructor':
		return HttpResponse('You are not an instructor!')
	else:
		return render(request,'paper2.html',
			{'user':user,'paper':paper,'question_pd_list':pd,'question_xz_list':xz,'allquestion_list':questions})

@login_required
def newpaper(request):
	user = request.user
	ins = user.instructor
	p = Paper()
	p.instructor = ins
	p.name = request.POST['paper_name']
	cname = request.POST['course_name']
	cour = Course.objects.get(title = cname)
	p.course = cour
	p.difficulty = request.POST['difficulty']
	p.status = request.POST['status']
	p.limit_time = request.POST['limit_time']
	ifauto = request.POST['method']
	xznum = request.POST['xznum']
	pdnum = request.POST['pdnum']
	question_pd_list=[]
	question_xz_list=[]
	if ifauto == 'yes':
		pdqueslist = Question.objects.filter(course_id = p.course_id, difficulty = p.difficulty, q_type = 'pd')
		xzqueslist = Question.objects.filter(course_id = p.course_id, difficulty = p.difficulty, q_type = 'xz')
		if pdqueslist.count() < int(pdnum):
			pdqueslist = Question.objects.filter(course_id = p.course_id, q_type = 'pd')
			if pdqueslist.count() < int(pdnum):
				return HttpResponse('没有这么多判断题！')
		if xzqueslist.count() < int(xznum):
			xzqueslist = Question.objects.filter(course_id = p.course_id, q_type = 'xz')
			if xzqueslist.count() < int(xznum):
				return HttpResponse('没有这么多选择题！')
		question_xz_list = random.sample(list(xzqueslist),int(xznum))
		p.save()
		for qxz in question_xz_list:
			qxz.paper.add(p)
		question_pd_list = random.sample(list(pdqueslist),int(pdnum))
		for qpd in question_pd_list:
			qpd.paper.add(p)
	else :
		p.save()

	paper = Paper.objects.get(id=p.id)
	questions = Question.objects.filter(course_id = p.course)
	paperques = paper.question_set.all()
	for p in questions:
		if p in paperques:
			del(p)
	type = getType(user)
	if type != 'Instructor':
		return HttpResponse('You are not an instructor!')
	else:
		return render(request,'paper2.html',
			{'user':user,'paper':paper,'question_pd_list':question_pd_list,'question_xz_list':question_xz_list,'allquestion_list':questions})

def statistics(request):
    error = False
    if 'paper' in request.POST :#输入一级条件是试卷
        paper = request.POST['paper']	
        pap = paper.obejects.filter(name = paper).id #name 要看数据库
        if 'test_point'in request.GET:
        	
            questions = Question.objects.filter(paper=pap)
            sheets = Sheet.objects.filter(paper=pap)
            tps_tot = {}#题目的考点及对应总的题数的字典
            tps_get = {}#某场考试某考点对的题数
            for q in questions:#试题的所有考点们
                if t not in tps:#未重复的新的考点
                    tps_tot[t] = 0
                    tps_get[t] = 0
                else:#已经出现过的考点 
                    tps_tot[t]+=1
            for s in sheets:
                for q in questions:
                    mark = Reply.objects.filter(sheet = s).filter(question = q)
                    testp = q.test_point #这道题的考点
                    if mark >0 :
                        tps_get[testp] +=1
            tps_percentage = {}
            for t in tps_tot.keys():
                tps_percentage[t]=tps_get[t] / tps_tot[t]#计算每个考点的正确率
            heights = tps_percentage.values()
            N = heights.count()
            ind = np.arange(N)  # the x locations for the groups
            width = 0.2       # the width of the bars
            rects = plt.bar(ind, heights, width, color='r')
            plt.ylabel('Percentage')
            plt.title('Correctness by test points')
            xnames = tps_percentage.keys()#各个考点
            plt.xticks(ind,xnames)
            def autolabel(rects):
            	# attach some text labels
            	for rect in rects:
            		height = rect.get_height()
            		plt.text(rect.get_x()+rect.get_width()/2., height, '%d'%int(height),
            				ha='center', va='bottom')
            autolabel(rects)
            plot.savefig('statistics.png')
            return render(request,'teacher2.html',{'picture':'statistics.png','total_pd':"",'total_xz':"",'avgage':"",'smax':"",'smin':""})
    		
        elif 'type' in request.POST:#返回2种类型的总的分数
        	
            sheets = Sheet.objects.filter(paper=pap)
            pd_tot = 0
            xz_tot = 0
            for s in sheets:
                pd_tot += s.pd_mark
                xz_tot += s.xz_mark
            return render(request,'teacher2.html',{'picture':"",'total_pd':pd_tot,'total_xz':xz_tot,'avgage':"",'smax':"",'smin':""})
        	
        else :
        	
            sheets = Sheet.objects.filter(paper=pap)
            ssum = 0
            avg = 0
            smin = 0
            smax = 0
            num = sheets.count()#总数
            belowSix = 0
            six2sev = 0
            sev2eig = 0
            eig2nin = 0
            aboveNin = 0
            for s in sheets:
                mark = s.tot_mark
                ssum= ssum + mark
                if mark < smin:
                	smin = mark
                elif mark > smax:
                	smax = mark
                else:
                	pass
                if mark < 60 :
                    belowSix+=1
                elif mark < 70 :
                    six2sev+=1
                elif mark < 80 :
                    sev2eig+=1
                elif mark < 90:
                	eig2nin+=1
                else:
                	aboveNin+=1
                
            avg = ssum/num
            #:开始绘图
            heights = (belowSix, six2sev, sev2eig, eig2nin, aboveNin)
            ind = np.arange(N)  # the x locations for the groups
            width = 0.35       # the width of the bars
            rects = plt.bar(ind, heights, width, color='r')
            plt.ylabel('Scores')
            plt.title('Scores by group')
            plt.xticks(ind,('<60', '60-70', '70-80', '80-90', '>90'))
            def autolabel(rects):
            	# attach some text labels
            	for rect in rects:
            		height = rect.get_height()
            		plt.text(rect.get_x()+rect.get_width()/2., height, '%d'%int(height),
            				ha='center', va='bottom')
            autolabel(rects)
            plot.savefig('statistics.png')
            return render(request,'teacher2.html',{'picture':'statistics.png','total_pd':"",'total_xz':"",'avgage':avg,'smax':smax,'smin':smin})
            
    elif 'student' in request.POST:
    	
        sid = Student.obejects.filter(user =  student)
        theSheets = sheets.obejects.filter(student = sid)
        scorelist = {}
        for s in theSheets:
            pid = s.paper
            pname = paper.objects.filter(id = pid).name
            scorelist[pname] = s.tot_mark

        heights = scorelist.values
        N = heights.count()
        ind = np.arange(N)  # the x locations for the groups
        width = 0.2       # the width of the bars
        rects = plt.bar(ind, heights, width, color='r')
        plt.ylabel('Percentage')
        plt.title('Correctness by test points')
        xnames = scorelist.keys #各个考试
        plt.xticks(ind,xnames)
        def autolabel(rects):
        	# attach some text labels
        	for rect in rects:
        		height = rect.get_height()
        		plt.text(rect.get_x()+rect.get_width()/2., height, '%d'%int(height),
        				ha='center', va='bottom')
        autolabel(rects)
        plot.savefig('statistics.png')
        return render(request,'teacher2.html',{'picture':'statistics.png','total_pd':"",'total_xz':"",'avgage':"",'smax':"",'smin':""})
    	
    else:
    	
        error = '请输入试卷或学生'
        return render(request,'teacher2.html',{'picture':"",'total_pd':"",'total_xz':"",'avgage':"",'smax':"",'smin':""})
        
@login_required
def paperstatus(request,pid):
	paper = Paper.objects.get(id = pid)
	if paper.status == 'o':
		paper.status = 'c'
		paper.save()
	else:
		paper.status = 'o'
		paper.save()

	user = User.objects.get(id=request.user.id)
	ins = user.instructor
	
	tches = Teaches.objects.filter(instructor_id = ins.id)
	teaches = []
	for t in tches:
		teaches.append(t.section.course)
	iPaper = Paper.objects.all()
	instruPaper = []
	for p in iPaper:
		if p.course in teaches:
			instruPaper.append(p)
	myPaper = []
	myPaper = Paper.objects.filter(instructor_id = ins.id)
	
	return render(request,'teacher1.html',{'user':user,'allpaper_list':instruPaper,'mypaper_list':myPaper})
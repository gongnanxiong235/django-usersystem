from django.shortcuts import render,HttpResponse,redirect
from user import models
# Create your views here.

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        flag=models.User.objects.filter(username=username,password=password).exists()
        if not flag:
            return HttpResponse('账户名或者密码错误')
        else:
            # redirect跟的是项目路径
            rep=redirect('/user/index/')
            rep.set_cookie("username",username,max_age=5000)
            #path 是指定给哪个页面设定cookie
            rep.set_cookie('test','test',path='/user/test')

            return rep

    else:
        return render(request,"user/login.html")

def index(request):
    username=request.COOKIES.get("username")
    if username:
        # render跟的是html
        return render(request,'user/index.html',locals())
    else:
        return redirect('/user/login/')


def test(request):
    v=request.COOKIES.get('test')
    return HttpResponse(v)
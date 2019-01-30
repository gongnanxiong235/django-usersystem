from django.shortcuts import render,HttpResponse,redirect
from user import models
from django import views
#在CBV中使用装饰器
from django.utils.decorators import  method_decorator
# Create your views here.

def outer(func):
    def inner(request,*args,**kwargs):
        print(request.method)
        return func(request,*args,**kwargs)
    return inner

#登陆装饰器
def auth(func):
    def innder(request,*args,**kwargs):
        username=request.COOKIES.get('username')
        if not username:
            return redirect('/user/login/')
        return func(request,*args,**kwargs)
    return innder

#@method_decorator:实在CVB模式下使用装饰器的方法
@method_decorator(outer,name='dispatch')
class Login(views.View):
    #重写父类的dispath方法(dispath方法：根据反射进行分发)，可以在执行get post..... 方法之前进行一系列的操作(装饰器也可以做类似的操作)
    # @method_decorator(outer)
    def dispatch(self, request, *args, **kwargs):
        print("before")
        ret=super(Login,self).dispatch(request, *args, **kwargs)
        print("after")
        return ret

    # @method_decorator(outer)
    def get(self,request,*args,**kwargs):
        return render(request, "user/login.html",{'msg':''})

    # @method_decorator(outer)
    def post(self,request,*args,**kwargs):
        username = request.POST.get('username')
        password=request.POST.get('password')
        print(password)
        flag=models.User.objects.filter(username=username,password=password).exists()
        if not flag:
            msg="账户名账户名或密码错误"
            return render(request, "user/login.html",{'msg':msg})
        else:
            # redirect跟的是项目路径
            rep=redirect('/user/index')
            rep.set_cookie("username",username,max_age=5000)
            #加密的cookie，可以在表面上解决安全问题，但是可能被反解出来，所以也是不太安全的
            return rep

class Regist(views.View):
    def get(self,request,*args,**kwargs):
        return render(request, "user/regist.html")
# def login(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         flag=models.User.objects.filter(username=username,password=password).exists()
#         if not flag:
#             return HttpResponse('账户名或者密码错误')
#         else:
#             # redirect跟的是项目路径
#             rep=redirect('/user/index')
#             rep.set_cookie("username",username,max_age=5000)
#             #加密的cookie，可以在表面上解决安全问题，但是可能被反解出来，所以也是不太安全的
#             rep.set_signed_cookie('password','123456')
#             #path 是指定给哪个页面设定cookie
#             rep.set_cookie('test','test',path='/user/test')
#
#             return rep
#
#     else:
#         return render(request,"user/login.html")
@auth
def index(request):
    # username=request.COOKIES.get("username")
    # #获取加密的cookie
    # password=request.get_signed_cookie("password")
    # if username:
    #     # render跟的是html
    #     return render(request,'user/index.html',locals())
    # else:
    #     return redirect('/user/login/')
    username=request.COOKIES.get("username")
    return render(request,'user/index.html',locals())


def test(request):
    v=request.COOKIES.get('test')
    return HttpResponse(v)
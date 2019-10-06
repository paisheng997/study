from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views import View
from django.core.paginator import Paginator
from app01.models import *
# Create your views here.
from .models import *
class Register(View):
    def get(self,request,*args,**kwargs):
        return render(request,'saller/register.html')
    def post(self,request,*args,**kwargs):
        ret = ''
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        mysql_email = User.objects.filter(email=email).first()
        if not mysql_email:
            if password and re_password and password ==re_password:
                User.objects.create(email=email,password=password)
                return render(request,'saller/login.html')
            else:
                ret = '请输入正确的密码'
        else:
            ret = '该邮箱已注册'
        return render(request, 'saller/register.html' ,locals())
def logout(request):
    request.session.flush()
    req = HttpResponseRedirect('/Saller/login/')
    req.delete_cookie('email')
    return req
class Login(View):
    def get(self,request,*args,**kwargs):
        return render(request,'saller/login.html')
    def post(self,request,*agrs,**kwargs):
        from io import StringIO
        # s = StringIO()
        # s.write()
        # print(s.getvalue())
        email = request.POST.get('email')
        password = request.POST.get('password')
        yanzhengma = request.POST.get('yanzhengma')
        # print(request.session)
        yanzhengma2 = request.session.get('yanzhengma')
        if yanzhengma2.lower() !=yanzhengma.lower():
            ret = '验证码错误'
            return render(request,'saller/login.html',locals())
        user = User.objects.filter(email=email,password=password).first()
        if user:
            req = HttpResponseRedirect('/Saller/index/')
            req.set_cookie('email',email)
            req.set_cookie('id',user.id)
            request.session['email'] = email
            return req
        else:
            ret = '该用户不存在或密码不正确'
        return render(request,'saller/login.html',locals())
class Index(View):
    def get(self,request,*args,**kwargs):
        email = request.POST.get('email')
        return render(request,'saller/index.html',locals())
    def post(self,request,*args,**kwargs):
        return render(request,'saller/index.html')
def get_colcor():
    import random
    return (random.randint(1,255),random.randint(1,255),random.randint(1,255))
def get_fonts():
    import random
    fonts = ''
    for i in range(4):
        dig = str(random.randint(0,9))
        upper = chr(random.randint(65,90))
        lower = chr(random.randint(97,122))
        font = random.choice([dig,lower,upper])
        fonts = fonts + ' '+ font
    return fonts
def yanzhengma(request):
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO,StringIO
    import random
    ##宽高
    img = Image.new('RGB',(200,50),get_colcor())
    ##方法一直接保存图片保存后在读取
    # f = open('a.png','wb')
    # img.save(f,'png')
    # with open('a.png','rb') as f:
    #     data = f.read()
    ##方法二将生成的图片保存在内存当中
    # f = BytesIO()
    # img.save(f,'png')
    # data = f.getvalue()
    ##方法三完善文本
    draw  = ImageDraw.Draw(img)
    font = ImageFont.truetype('static/fonts/impact.ttf',32)
    yanzhengma = ''
    for i in range(1,6):
        dig = str(random.randint(0, 9))
        upper = chr(random.randint(65, 90))
        lower = chr(random.randint(97, 122))
        fonts = random.choice([dig, lower, upper])
        yanzhengma += fonts
        draw.text((i*30,0),fonts,get_colcor(),font=font)
    # s = StringIO()
    request.session['yanzhengma'] = yanzhengma
    # print(s.getvalue())
    ##造线，造点
    width = 200
    height = 50
    for i in range(10):
        x1 = random.randint(0,width)
        x2 = random.randint(0,width)
        y1 = random.randint(0,height)
        y2 = random.randint(0,height)
        draw.line((x1,y1,x2,y2),fill=get_colcor())
    for i in range(100):
        draw.point([random.randint(0,width),random.randint(0,height)],fill=get_colcor())
        x = random.randint(0,width)
        y = random.randint(0,height)
        draw.arc((x,y,x+4,y+4),0,90,fill=get_colcor())
    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return HttpResponse(data)
def personal(request):
    data = request.POST
    user = User.objects.get(id=request.COOKIES.get('id'))
    if request.method == 'POST':
        user.name = data.get('username')
        user.age = data.get('age')
        user.gender = data.get('gender')
        user.address  = data.get('address')
        user.photo = request.FILES.get('photo')
        user.phone = data.get('phone')
        user.save()
    return render(request,'saller/personal.html',locals())

from django.shortcuts import render
from app01.models import *
from django.core.paginator import Paginator
def about(request):
    return render(request,"about.html")

def index(request):
    article = Article.objects.all()[:6]
    recommend = Article.objects.filter(recommend=1)[:7]
    click = Article.objects.filter(click=1)[:12]
    return render(request,"index.html",locals())

def listpic(request):
    return render(request,"listpic.html")

def newslistpic(request,page=1):
    page = int(page)
    article = Article.objects.all().order_by("date")
    paginator = Paginator(article,6)
    page_obj = paginator.page(page)
    start = page - 3
    end = page + 2
    max_page = int(paginator.num_pages)
    # print(paginator.page_range) range(1, 20)前开后开的东西
    if page in range(1,3):
        start = 0
        end = 5
    if page in range(paginator.num_pages-2,paginator.num_pages+1):
        start = paginator.num_pages-5
        end = paginator.num_pages + 1
    page_range = paginator.page_range[start:end]
    # print(page_range)
    return render(request,"newslistpic.html",locals())
    # for i in range(100):
    #     a = Article()
    #     a.title = "title %d" % i
    #     a.content = "title %d" % i
    #     a.description = "title %d" % i
    #     a.picture = "images/1.jpg"
    #     a.author = Author.objects.get(id=1)
    #     a.save()
    #     a.type.add(Type.objects.get(id=1))
    #     a.save()
def details(request,id):
    id = int(id)
    article = Article.objects.get(id=id)
    return render(request,"details.html",locals())


import hashlib
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result
def reqtest(request):
    print(request.method)
    # data = request.GET
    # print(data)
    # print(request.FILES)
    # print(request.scheme)
    # print(request.path)
    # print(request.body)
    # print(request.META)
    # print(request.META['OS'])
    # print(request.META['HTTP_USER_AGENT'])
    # print(request.META['HTTP_HOST'])
    # print(request.META['HTTP_REFERER'])
    # print(request.POST)

    data = request.POST
    print(data)
    # if len(data)!=0:
    if 'username' in data and 'password' in data and 'password2' in data:
        username = data['username']
        password = data['password']
        password2 = data['password2']
        print(username)
        if password == password2:
            Author.objects.create(name=username,password=setPassword(password))
        else:
            print("两次密码不一样")
    return render(request,'formtest.html',locals())

from app01.forms import Register
def register(request):
    register_form = Register()
    if request.method == 'POST':
        data = Register(request.POST)
        print(data.is_valid())
        if data.is_valid():
            clean_data = data.cleaned_data
            username = clean_data['name']
            password = clean_data['password']
            print(username,password)
        else:
            print(data.errors)
    return render(request,'register.html',locals())

def ajax_get(request):
    return render(request,'ajax_get.html')
from django.http import JsonResponse
def ajax_get_data(request):
    res = {'code':10000,'msg':''}
    data = request.GET
    username = data['username']
    password = data['password']
    if username is None or password is None:
        res['code'] = 10001
        res['msg'] = '未收到数据'
    else:
        user = Author.objects.filter(name=username,password=setPassword(password)).first()
        if user:
            res['msg'] = '登陆成功'
        else:
            res['code'] = 10002
            res['msg'] = '用户名或密码错误'
    return JsonResponse(res)

def ajax_post(request):
    return render(request,'ajax_post.html')
def ajax_post_data(request):
    res = {'code':1000,'msg':''}
    data = request.POST
    username = data['username']
    if len(username) == 0:
        res['code'] = 10001
        res['msg'] = '用户名不能为空'
    else:
        user = Author.objects.filter(name=username).first()
        if user:
            res['code'] = 10002
            res['msg'] = '用户名已存在'
        else:
            res['code'] = 10000
            res['msg'] = '用户名合法'
    return JsonResponse(res)

from django.http import HttpResponseRedirect
def one_cookie(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        print(request.COOKIES)
        # print(username,password)
        user = Author.objects.filter(name=username).first()
        if user:
            if user.password == setPassword(password):
                # return HttpResponseRedirect('/index/')
                response = HttpResponseRedirect('/index/')
                # response = render(request,'index.html')
                response.set_cookie('name','admin')
                return response
                # return render(request,'index.html')
            else:
                # print(user.password)
                # print(setPassword(password))
                print('密码不正确')
    return render(request,'one_cookie.html')




#####################################后台视图
from django.views import View
from django.http import HttpResponse
class Register(View):
    def get(self,request,*args,**kwargs):
        return render(request,'saller/register.html')
    def post(self,request,*args,**kwargs):
        ret = ''
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        age = int(request.POST.get('age'))
        gender = int(request.POST.get('gender'))
        re_password = request.POST.get('re_password')
        mysql_email = Author.objects.filter(email=email).first()
        if not mysql_email:
            if password and re_password and password ==re_password:
                Author.objects.create(email=email,password=password,gender=gender,name=username,age=age)
                return HttpResponseRedirect('/login/')
            else:
                ret = '请输入正确的密码'
        else:
            ret = '该邮箱已注册'
        return render(request, 'saller/register.html' ,locals())

def logout(request):
    request.session.flush()
    req = HttpResponseRedirect('/login/')
    req.delete_cookie('email')
    return req
class Login(View):
    def get(self,request,*args,**kwargs):
        return render(request,'saller/login.html')
    def post(self,request,*agrs,**kwargs):
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        yanzhengma = request.POST.get('yanzhengma')
        yanzhengma2 = request.session.get('yanzhengma')
        if yanzhengma2.lower() != yanzhengma.lower():
            ret = '验证码错误'
            return render(request,'saller/login.html',locals())
        user = Author.objects.filter(email=email,password=password).first()
        if user:
            req = HttpResponseRedirect('/h_index/')
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
    print(yanzhengma)
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
    if request.method == 'POST':
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        content = data.get('content')
        type = data.get('type')
        type = Type.objects.filter(id=type).first()
        picture = request.FILES.get('picture')
        print(picture)
        article = Article()
        article.title = title
        article.description = description
        article.picture = picture
        article.content = content
        article.author = Author.objects.filter(email=request.COOKIES.get('email')).first()
        article.save()
        article.type.add(type)
        article.save()
    return render(request,'saller/personal.html')


def myarticles(request,page=1):
    email = request.COOKIES.get('email')
    page = int(page)
    articles = Article.objects.filter(author=Author.objects.filter(email=email).first())
    paginator = Paginator(articles, 6)
    page_obj = paginator.page(page)
    start = page - 3
    end = page + 2
    max_page = int(paginator.num_pages)
    # print(paginator.page_range) range(1, 20)前开后开的东西
    if page in range(1, 3):
        start = 0
        end = 5
    if page in range(paginator.num_pages - 2, paginator.num_pages + 1):
        start = paginator.num_pages - 5
        end = paginator.num_pages + 1
    page_range = paginator.page_range[start:end]
    return render(request,'saller/myarticles.html',locals())
def myarticle(request,id):
    id = int(id)
    article = Article.objects.get(id=id)
    return render(request,'saller/details.html',locals())
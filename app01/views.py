from django.shortcuts import render
from django.http import HttpResponse
from app01.models import *

# Create your views here.

def index(request):
    return HttpResponse("index")

def addperson(request):
    # Person.objects.create(name="张三",age=13,height=1.78,birthday="2017-12-23")
    # person = Person(name="李四",age=67,height=1.78)
    # person.save()
    # person = Person()
    # person.name = "李白"
    # person.age = 78
    # person.height = 1.89
    # person.save()
    data = dict(name="赵云",age=45,height=1.89)
    Person.objects.create(**data)
    return HttpResponse("插入数据")
def queryperson(request):
    data = Person.objects.all().values()
    data = Person.objects.all().first()
    data = Person.objects.get(name="张三")#只能有一个
    data = Person.objects.filter(name="赵云")
    data = Person.objects.all().order_by("age")
    data = Person.objects.all()[0:5]
    data = Person.objects.filter(id__lt=3)
    data = Person.objects.filter(id__in=[1,2,3])
    data = Person.objects.filter(name__contains="云")
    print(data,type(data))
    return HttpResponse("查询数据")
def updateperson(request):
    # data = Person.objects.all().first()
    # data.name = "张三三"
    # data.save()
    Person.objects.filter(id=5).update(name="韩信")
    return HttpResponse("修改数据")
def removeperson(request):
    Person.objects.filter(id=6).delete()
    return HttpResponse("删除数据")
def addmore(request):
    # Publish.objects.create(name="中国出版社",address="北京")
    # Publish.objects.create(name="河南出版社",address="开封")
    # Publish.objects.create(name="新疆出版社",address="伊利")
    # Publish.objects.create(name="浙江出版社",address="杭州")

    # Book.objects.create(name="平凡的世界",publish_id=1)
    # publish = Publish.objects.filter(id=2).first()
    # Book.objects.create(name="人性弱点",publish_id = publish.id)
    # Book.objects.create(name="骆驼祥子",publish=Publish.objects.get(name="新疆出版社"))
    # book = Book()
    # book.name = "犯罪心理学"
    # book.publish = Publish.objects.get(id=4)
    # book.save()
    publish = Publish.objects.get(name="河南出版社")
    publish.book_set.create(name="风雨哈佛路")
    return HttpResponse("一对多插入")
def querymore(request):
    # book = Book.objects.get(name="平凡的世界")
    # print(book.publish.name)
    # data = Book.objects.filter(publish=Publish.objects.get(name="河南出版社"))
    # for i in data:
    #     print(i.name)
    publish = Publish.objects.get(name="河南出版社")
    book = publish.book_set.all().filter(id=2)
    print(book)
    return HttpResponse("一对多查询")
def updatemore(request):
    # Publish.objects.filter(name="中国出版社").update(name="中国人民出版社")
    # book = Book.objects.filter(name="人性弱点").first()
    # book.publish = Publish.objects.filter(name="中国人民出版社").first()
    # book.save()
    # Book.objects.filter(name="人性弱点").update(publish=Publish.objects.filter(name="河南出版社").first())
    publish_obj = Publish.objects.filter(name="河南出版社").first()
    book = Book.objects.get(id=1)
    book1 = Book.objects.get(id=2)
    publish_obj.book_set.set([book,book1])
    return HttpResponse("一对多修改")
def removemore(request):
    Book.objects.filter(name="风雨哈佛路").delete()
    return HttpResponse("一对多删除")
def addmany(request):
    # Teacher.objects.create(name="老张",gender="男")
    # Teacher.objects.create(name="老李",gender="女")
    # Teacher.objects.create(name="老王",gender="男")
    # Teacher.objects.create(name="老赵",gender="女")
    # teacher = Teacher.objects.filter(name="老张").first()
    # teacher.person.create(name="曹操",age=90,height=1.90)
    # teacher = Teacher.objects.filter(name="老李").first()
    # student = Person.objects.get(id=1)
    # teacher.person.add(student)
    # teacher = Teacher.objects.get(name="老赵")
    # student = Person.objects.get(id=3)
    # student.teacher_set.add(teacher)
    person = Person.objects.get(name="韩信")
    teacher = Teacher.objects.get(name="老张")
    person.teacher_set.add(teacher)
    return HttpResponse("多对多插入")
def querymany(request):
    # teacher = Teacher.objects.get(name="老赵")
    # person = teacher.person.all()
    # print(person)
    person_obj = Person.objects.get(name="韩信")
    teacher = person_obj.teacher_set.all()
    print(teacher)
    return HttpResponse("多对多查询")
def updatemany(request):
    # teacher = Teacher.objects.get(name="老赵")
    # teacher.person.set([1,2,3])

    # teacher = Teacher.objects.get(name="老李")
    # person1 = Person.objects.get(name="韩信")
    # person2 = Person.objects.get(name="张三三")
    # person3 = Person.objects.get(name="李四")
    # teacher.person.set([person3,person1,person2])
    person_obj = Person.objects.get(name="韩信")
    teacher = Teacher.objects.get(name="老王")
    person_obj.teacher_set.set([teacher])
    return HttpResponse("多对多修改")
def removemany(request):
    # teacher = Teacher.objects.get(name="老赵")
    # person_obj = Person.objects.get(name="张三三")
    # teacher.person.remove(person_obj)
    person_obj = Person.objects.get(name="李四")
    teacher = Teacher.objects.get(name="老赵")
    person_obj.teacher_set.remove(teacher)
    return HttpResponse("多对多删除")
from django.db.models import Avg,Sum,Min,Max,Count,F,Q
def juhe(request):
    data = Person.objects.all().aggregate(Avg("age"),Max("age"),Min("age"),Sum("age"))
    print(data)
    return HttpResponse("聚合操作")
def Ffunc(request):
    # Book.objects.filter(id__in=[2,4]).update(num=30)
    data = Book.objects.filter(num__lt=F("saled"))
    print(data)
    return HttpResponse("F操作")
def Qfunc(request):
    data = Book.objects.filter(Q(num__lt=300)&Q(saled=100))
    data = Book.objects.filter(Q(num__lt=50)|Q(saled=1000))
    data = Book.objects.filter(~Q(num__lt=50)|~Q(saled=100))
    print(data)
    return HttpResponse("Q操作")
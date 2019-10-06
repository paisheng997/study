from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=32,verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")
    height = models.DecimalField(max_digits=5,decimal_places=2,verbose_name="身高")
    birthday = models.DateField(auto_now=True,verbose_name="生日")
    def __str__(self):
        return self.name
    class Meta:
        db_table = "person"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
class Publish(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
    class Meta:
        db_table = "publish"
class Book(models.Model):
    name = models.CharField(max_length=32)
    publish = models.ForeignKey(to=Publish,on_delete=models.CASCADE)
    num = models.IntegerField(default=200)
    saled = models.IntegerField(default=100)
    class Meta:
        db_table = "book"
class Teacher(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField(default=30)
    gender = models.CharField(max_length=32)
    person = models.ManyToManyField(to=Person)
    class Meta:
        db_table = "teacher"

GENDER_LIST = (
    (1,'男'),
    (2,'女'),
)
class Author(models.Model):
    name = models.CharField(max_length=32,verbose_name="姓名")
    password = models.CharField(max_length=64,default=123)
    age = models.IntegerField(verbose_name="年龄")
    gender = models.IntegerField(choices=GENDER_LIST,default=1,verbose_name="性别")
    email = models.CharField(max_length=32,verbose_name="邮箱")
    def __str__(self):
        return self.name
    class Meta:
        db_table = "author"
        verbose_name = "作者表"
        verbose_name_plural = verbose_name
class Type(models.Model):
    type_name = models.CharField(max_length=32,verbose_name="类型")
    description = RichTextField(verbose_name="描述")
    def __str__(self):
        return self.type_name
    class Meta:
        db_table = "type"
        verbose_name = "类型表"
        verbose_name_plural = verbose_name
class Article(models.Model):
    title = models.CharField(max_length=32)
    date = models.DateField(auto_now=True)
    content = RichTextField(verbose_name="内容")
    description = RichTextField(verbose_name="描述")
    picture = models.ImageField(upload_to='images')
    recommend = models.IntegerField(default=0,verbose_name="推荐")
    click = models.IntegerField(default=0,verbose_name="点击率")
    author = models.ForeignKey(to=Author,on_delete=models.PROTECT,verbose_name="作者")
    type = models.ManyToManyField(to=Type,verbose_name="类型")
    def __str__(self):
        return self.title
    class Meta:
        db_table = "article"
        verbose_name = "文章表"
        verbose_name_plural = verbose_name

class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    class Meta:
        db_table = 'user'
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=70)
    body = UEditorField(null=True, blank=True)
    created_time = models.DateTimeField(null=True,blank=True)
    modified_time = models.DateTimeField(null=True,blank=True)
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    music = models.CharField(max_length=30, blank=True)
    view_num = models.PositiveIntegerField(default=0)
    url_image = models.URLField(null=True, blank=True)
    editors_choice = models.BooleanField(default=False)
    cover = models.FileField(upload_to='cover_image', null=True, blank=True)
    author = models.ForeignKey(User, null=True, blank=True)
    #默认情况下 CharField 要求我们必须存入数据，否则就会报错。指定 CharField 的 blank=True 参数值后就可以允许空值了


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('firstapp:detail', kwargs={'page_num': self.page_num})


    def get_views(self):
        self.views += 1
        self.save(update_fields=['views'])


    class Meta:
        ordering = ['-created_time']


class Comment(models.Model):
    name = models.CharField(max_length=10)
    avatar = models.CharField(max_length=100, default="static/images/default.png")
    content = models.TextField()
    createtime = models.DateField(auto_now=True)
    belong_to = models.ForeignKey(to=Article, related_name='under_comments', null=True, blank=True)

    def __str__(self):
        return self.content


# with open('image.txt') as f:
#     fake = Factory.create()
#     for url in f.readlines():
#         v = Article(
#             title=fake.text(max_nb_chars=90),
#             body=fake.text(max_nb_chars=3000),
#             url_image=url,
#             editors_choice=fake.pybool()
#         )
#         v.save()

class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image')


class Tickets(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets')
    video = models.ForeignKey(to=Article, related_name='tickets')
    VOTE_CHOICE=(
        ('like','like'),
        ('dislike','dislike'),
        ('normal','normal'),
    )
    choice = models.CharField(choices=VOTE_CHOICE, max_length=10)

    def __str__(self):
        return str(self.id)

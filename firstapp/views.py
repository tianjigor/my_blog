# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from firstapp.models import Article, Comment, Tickets, Tag, Category
from firstapp.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from firstapp.forms import LoginForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def detail(request, page_num, error_form = None):
    form = CommentForm
    context = {}
    article = Article.objects.get(id=page_num)
    context['article'] = article
    if str(request.user) != 'AnonymousUser':
        voter_id = request.user.profile.id
        try:
            user_ticket_for_article = Tickets.objects.get(voter_id=voter_id, video_id=page_num)
            context['user_tickets'] = user_ticket_for_article
        except:
            pass
    like_count = Tickets.objects.filter(choice='like', video_id=page_num).count()
    context['like_count'] = like_count

    if error_form:
        context['form'] = error_form
    else:
        context['form'] = form

    return render(request, 'detail.html', context)

def detail_comment(request, page_num):
    form = CommentForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        content = form.cleaned_data["content"]
        a = Article.objects.get(id=page_num)
        c = Comment(name=name, content=content, belong_to=a)
        c.save()
        return redirect("firstapp:detail", page_num=page_num)
    else:
        return detail(request, page_num=page_num, error_form=form)


def detail_vote(request, page_num):
    voter_id = request.user.profile.id
    try:
        user_ticket_for_article = Tickets.objects.get(voter_id=voter_id, video_id=page_num)
        user_ticket_for_article.choice = request.POST['vote']
        user_ticket_for_article.save()
    except ObjectDoesNotExist:
        new_ticket = Tickets(voter_id=voter_id, video_id=page_num, choice=request.POST['vote'])
        new_ticket.save()

    return redirect(to='detail', page_num=page_num)

def pagination_data(paginator, page):
    # if not is_paginated:
    #     # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
    #     return {}

    # 当前页左边连续的页码号，初始值为空
    left = []

    # 当前页右边连续的页码号，初始值为空
    right = []

    # 标示第 1 页页码后是否需要显示省略号
    left_has_more = False

    # 标示最后一页页码前是否需要显示省略号
    right_has_more = False

    # 标示是否需要显示第 1 页的页码号。
    # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
    # 其它情况下第一页的页码是始终需要显示的。
    # 初始值为 False
    first = False

    # 标示是否需要显示最后一页的页码号。
    # 需要此指示变量的理由和上面相同。
    last = False

    # 获得用户当前请求的页码号
    page_number = int(page)

    # 获得分页后的总页数
    total_pages = paginator.num_pages

    # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
    page_range = list(paginator.page_range)

    if page_number == 1:
        # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
        # 此时只要获取当前页右边的连续页码号，
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
        # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        right = page_range[page_number:page_number + 2]

        # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
        # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
        if right[-1] < total_pages - 1:
            right_has_more = True

        # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
        # 所以需要显示最后一页的页码号，通过 last 来指示
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
        # 此时只要获取当前页左边的连续页码号。
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
        # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

        # 如果最左边的页码号比第 2 页页码号还大，
        # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
        if left[0] > 2:
            left_has_more = True

        # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
        # 所以需要显示第一页的页码号，通过 first 来指示
        if left[0] > 1:
            first = True
    else:
        # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
        # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]

        # 是否需要显示最后一页和最后一页前的省略号
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        # 是否需要显示第 1 页和第 1 页后的省略号
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
    }

    return data


def index(request, cate=None):
    context = {}
    if cate is None:
        Article_list = Article.objects.all()
    if cate == 'editors':
        Article_list = Article.objects.filter(editors_choice=True)
    else:
        Article_list = Article.objects.all()

    paginator = Paginator(Article_list, 3)

    page = request.GET.get('page')



    try:
        Article_list = paginator.page(page)
        pagination_datas = pagination_data(paginator, page)
    except PageNotAnInteger:
        Article_list = paginator.page(1)
        pagination_datas = pagination_data(paginator, 1)
    except EmptyPage:
        Article_list = paginator.page(paginator.num_pages)
        pagination_datas = pagination_data(paginator, paginator.num_pages)
    context['article_list'] = Article_list
    context['page'] = pagination_datas
    print pagination_datas
    return render(request, 'index.html', context)


def index_login(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to='index')
    context['form'] = form
    return render(request, 'login_regsiter.html', context)


def index_register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')
    context['form'] = form
    return render(request, 'login_regsiter.html', context)


def archives(request, year, month):
    article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'article_list': article_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'article_list': article_list})


def tag(request, pk):
    cate = get_object_or_404(Tag, pk=pk)
    article_list = Article.objects.filter(tags=cate)
    return render(request, 'blog/index.html', context={'article_list': article_list})

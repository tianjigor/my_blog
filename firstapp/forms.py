# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError


def words_validator(content):
    keyword = ['money', 'fapiao']
    for word in keyword:
        if word in content:
            raise ValidationError('Your comment contains invalid words,please check it again.')

def comment_validator(content):
    if len(content) < 4:
        raise ValidationError('not enough words')


class CommentForm(forms.Form):
    name = forms.CharField(max_length=50)
    content = forms.CharField(
        widget=forms.Textarea(),
        error_messages={
            'requied':'please write something'
            },
        validators=[words_validator ,comment_validator]
        )


class LoginForm(forms.Form):
    # 字段默认label 是通过将字段名中所有的下划线转换成空格并大写第一个字母生成的,对应Username,Password变量，也可以自己设置label作为变量渲染到html中
    username = forms.CharField()
    password = forms.CharField()

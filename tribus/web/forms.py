#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms




class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(),
        max_length=100, label=''
        )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=100, label=''
        )
#    rememberme = forms.BooleanField(
#        widget=forms.CheckboxInput(),
#        label=''
#        )


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(),
        max_length=100, label=''
        )
    email = forms.CharField(
        widget=forms.TextInput(),
        max_length=100, label=''
        )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        max_length=100, label=''
        )

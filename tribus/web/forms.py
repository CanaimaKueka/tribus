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


class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(),
        max_length=100, label=''
        )
    lastname = forms.CharField(
        widget=forms.TextInput(),
        max_length=100, label=''
        )
    firstname = forms.CharField(
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

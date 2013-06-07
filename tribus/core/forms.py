#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
    	widget=forms.TextInput(
    		attrs={
    		'placeholder': 'Enter your username',
    		'class': 'input-xlarge',
    		'autofocus': 'autofocus'
    		}
    		),
    	max_length=100, label=''
    	)
    password = forms.CharField(
    	widget=forms.PasswordInput(
    		attrs={
    		'placeholder': 'Enter your password',
    		'class': 'input-xlarge'
    		}
    		),
    	max_length=100, label=''
    	)

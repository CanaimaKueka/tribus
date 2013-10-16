#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from tribus.web.user.forms import SignupForm


def tour(request):
    return render('tour.html', {})

def index(request):

    if request.user.is_authenticated():
        render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-responsive']
        render_js = ['jquery', 'jquery.autogrow', 'jquery.timeago', 'bootstrap', 'angular',
                        'angular.resource', 'angular.infinite-scroll', 'dashboard.app',
                        'dashboard.jquery']

        return render(request, 'dashboard.html', {
            # 'newtribform': newtribform,
            'render_css': render_css,
            'render_js': render_js,
            })

    else:
        signupform = SignupForm()
        signupform.fields['username'].widget.attrs['class'] = 'input-large'
        signupform.fields['first_name'].widget.attrs['class'] = 'input-small'
        signupform.fields['last_name'].widget.attrs['class'] = 'input-small'
        signupform.fields['email'].widget.attrs['class'] = 'input-large'
        signupform.fields['password'].widget.attrs['class'] = 'input-large'

        render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-responsive']
        render_js = []

        return render(request, 'index.html', {
            'signupform': signupform,
            'render_css': render_css,
            'render_js': render_js,
            })
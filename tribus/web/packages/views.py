#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from tribus.web.packages.models import *
from tribus.web.packages.forms import busquedaPaquete
from tribus.config.pkgrecorder import raiz, relation_types


def frontpage(request):

    
    
    return render(request, 'packages/frontpage.html', {})


def profile(request, name):
    context = {}
    p = Package.objects.filter(Package = name)
    if p:
        context["paquete"] = p[0]
        details_list = Details.objects.filter(package = p[0])
        dict_details = {}
        print details_list
        for det in details_list:
            dict_details[det.Distribution] = {}
            dict_details[det.Distribution][det.Architecture] = {}
            dict_details[det.Distribution][det.Architecture]['data'] = det
            dict_details[det.Distribution][det.Architecture]['relations'] = {}
            r = Relation.objects.filter(details = det).order_by("alt_id", "related_package",
                                                                "version")
            for n in r:
                if n.relation_type in relation_types:
                    if not dict_details[det.Distribution][det.Architecture]['relations'].has_key(n.relation_type):
                        dict_details[det.Distribution][det.Architecture]['relations'][n.relation_type] = []
                    dict_details[det.Distribution][det.Architecture]['relations'][n.relation_type].append(n)
        context["raiz"] = raiz
        context["detalles"] = dict_details
        
        render_css = ['normalize', 'fonts', 'bootstrap', 'bootstrap-responsive',
                           'font-awesome', 'tribus', 'tribus-responsive']
        render_js = ['jquery', 'bootstrap']
        
        context['render_js'] = render_js
        context['render_css'] = render_css
        
        return render(request,'packages/packages.html', context)
    else:
        return render(request,'packages/404.html')


def by_category(request, category):
    l = Label.objects.filter(Name = category)
    context = {"categories":l}
    return render(request,'packages/categories.html', context)


def by_tag(request, tag):
    p = Package.objects.filter(Labels__Tags__Value = tag)
    context = {"tags":p}
    return render(request,'packages/tags.html', context)
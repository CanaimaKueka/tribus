#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from tribus.web.cloud.models import *
from tribus.config.pkgrecorder import LOCAL_ROOT, relation_types


def frontpage(request):
    return render(request, 'cloud/frontpage.html', {
        'render_js': ['angular', 'angular.bootstrap', 'angular.resource',
                        'controllers.angular', 'services.angular', 'elements.angular',
                        'cloud.angular', 'navbar.angular'],
        })


def profile(request, name):
    dict_details = {}
    package_info = get_object_or_404(Package, Package=name)
    details_list = Details.objects.filter(package=package_info)

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
                
    return render(request, 'cloud/packages.html', {
        'paquete': package_info,
        'raiz': LOCAL_ROOT,
        'detalles': dict_details,
        'render_js': ['angular', 'angular.autogrow', 'angular.bootstrap', 'angular.resource', 
                 'angular.infinite-scroll', 'controllers.angular', 'services.angular',
                 'elements.angular', 'cloud.angular', 'navbar.angular', 'md5'],
        })


def by_category(request, category):
    l = Label.objects.filter(Name = category)
    context = {"categories":l}
    return render(request,'cloud/categories.html', context)


def by_tag(request, tag):
    p = Package.objects.filter(Labels__Tags__Value = tag)
    context = {"tags":p}
    return render(request,'cloud/tags.html', context)
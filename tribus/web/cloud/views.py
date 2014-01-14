#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from tribus.web.cloud.models import *
from tribus.config.pkgrecorder import LOCAL_ROOT, relation_types, CANAIMA_ROOT, codenames
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from tribus.config.web import DEBUG


def frontpage(request):
    return render(request, 'cloud/frontpage.html', {
        'render_js': ['angular', 'angular.sanitize', 'angular.resource', 'angular.bootstrap',
                      'controllers.angular', 'services.angular', 'elements.angular',
                      'cloud.angular', 'navbar.angular'],
    })


def package_list(request):
    context = {}

    # Cargamos la librería AngujarJS junto con sus plugins
    render_js = [
        'angular',
        'angular.sanitize',
        'angular.resource',
        'angular.bootstrap']

    # Cargamos las funciones de Tribus para AngularJS
    render_js += ['controllers.angular', 'services.angular',
                  'elements.angular', 'search.angular', 'navbar.angular']

    context["render_js"] = render_js

    sqs = SearchQuerySet().models(Package).order_by('name')
    paginator = Paginator(sqs, 30)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        return render(request, 'cloud/package_list.html', {})

    context["page"] = page

    return render(request, 'cloud/package_list.html', context)


def profile(request, name):
    package_info = get_object_or_404(Package, Package=name)
    details_list = Details.objects.filter(package=package_info)
    distributions = []
    tmp_dict = {}
    for det in details_list:
        if codenames[det.Distribution] not in tmp_dict:
            tmp_dict[codenames[det.Distribution]] = {}

        tmp_dict[codenames[det.Distribution]]['codename'] = det.Distribution
        tmp_dict[codenames[det.Distribution]][
            'version'] = codenames[det.Distribution]

        if 'Architectures' not in tmp_dict[codenames[det.Distribution]]:
            tmp_dict[codenames[det.Distribution]]['Architectures'] = {}

        tmp_dict[codenames[det.Distribution]][
            'Architectures'][det.Architecture] = {}
        tmp_dict[
            codenames[
                det.Distribution]][
            'Architectures'][
            det.Architecture][
            'data'] = det

        tmp_dict[codenames[det.Distribution]][
            'Architectures'][det.Architecture]['relations'] = {}

        r = Relation.objects.filter(
            details=det).order_by(
            "alt_id",
            "related_package",
            "version")
        for n in r:
            if n.relation_type in relation_types:
                if n.relation_type not in tmp_dict[codenames[det.Distribution]]['Architectures'][det.Architecture]['relations']:
                    tmp_dict[
                        codenames[
                            det.Distribution]][
                        'Architectures'][
                        det.Architecture][
                        'relations'][
                        n.relation_type] = [
                    ]
                tmp_dict[codenames[det.Distribution]]['Architectures'][
                    det.Architecture]['relations'][n.relation_type].append(n)

    for dist in tmp_dict.values():
        distributions.append(dist)

    if DEBUG:
        file_root = LOCAL_ROOT
    else:
        file_root = CANAIMA_ROOT

    return render(request, 'cloud/packages.html', {
        'paquete': package_info,
        'raiz': file_root,
        'detalles': distributions,
        'render_js': ['angular', 'angular.sanitize', 'angular.resource', 'angular.bootstrap',
                      'angular.infinite-scroll', 'controllers.angular', 'services.angular',
                      'elements.angular', 'cloud.angular', 'navbar.angular', 'md5'],
    })


def by_category(request, category):
    l = Label.objects.filter(Name=category)
    context = {"categories": l}
    return render(request, 'cloud/categories.html', context)


def by_tag(request, tag):
    p = Package.objects.filter(Labels__Tags__Value=tag)
    context = {"tags": p}
    return render(request, 'cloud/tags.html', context)

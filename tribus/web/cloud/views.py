#!/usr/bin/env python
# -*- coding: utf-8 -*-

#=========================================================================
# TODO:
# 1. Traducir documentación.
#=========================================================================

from django.shortcuts import render, get_object_or_404
from tribus.web.cloud.models import Package, Details, Relation, Label
from tribus.config.pkgrecorder import LOCAL_ROOT, relation_types, CANAIMA_ROOT, codenames
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from tribus.config.web import DEBUG
from waffle.decorators import waffle_switch


@waffle_switch('cloud')
def frontpage(request):
    '''
    Muestra la portada de la nube de aplicaciones.
    
    **Contexto:**
    
    ``render_js``
        Lista de los modulos de angular.js usados por la plantilla.
    
    '''
    
    return render(request, 'cloud/frontpage.html', {
        'render_js': ['angular', 'angular.sanitize', 'angular.resource', 'angular.bootstrap',
                      'controllers.angular', 'services.angular', 'elements.angular',
                      'cloud.angular', 'navbar.angular'],
    })


@waffle_switch('cloud')
def package_list(request):
    '''
    Muestra una lista en orden alfabetico de todas 
    las aplicaciones disponibles en la plataforma de tribus.
    Solo se muestran 30 resultados por pagina. 
    
    **Contexto:**
    
    ``render_js``
        Lista de los modulos de angular usados por la plantilla.
        
    ``page``
        Resultados de la pagina actual.
        
    '''
    
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


@waffle_switch('cloud')
def profile(request, name):
    '''
    Muestra el perfil de una aplicación especifica. El perfil esta compuesto por:
    
    - Nombre y descripción de la aplicación.
    - Información básica de la aplicación.
    - Distribuciones en donde esta disponible la aplicación.
    - Información detallada de acuerdo a las distribuciones y arquitecturas disponibles.
    
    **Arguments**
    
    ``name``
        Nombre de la aplicación consultada.
    
    **Contexto:**
    
    ``render_js``
        Lista de los modulos de angular usados por la plantilla.
        
    ``paquete``
        Información básica de la aplicación consultada.
        
    ``raiz``
        Indica si las consultas se hacen a un repositorio de pruebas o al repositorio oficial.
        
    ``detalles``
        Lista que contiene información detallada de la aplicación segun se arquitectura y distribución.
        
    '''
    
    package_info = get_object_or_404(Package, Name=name)
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


# def by_category(request, category):
#     l = Label.objects.filter(Name=category)
#     context = {"categories": l}
#     return render(request, 'cloud/categories.html', context)


# def by_tag(request, tag):
#     p = Package.objects.filter(Labels__Tags__Value=tag)
#     context = {"tags": p}
#     return render(request, 'cloud/tags.html', context)

# -*- coding: utf-8 -*-
from django.shortcuts import render
from tribus.web.paqueteria.models import *
from tribus.web.paqueteria.forms import busquedaPaquete
from tribus.config.pkgrecorder import raiz, relation_types
import string

def index(request):
    return render(request,'paqueteria/buscador.html', {})

def categoria(request, categoria):
    x = Label.objects.filter(Name = categoria)
    contexto = {"i":x}
    return render(request,'paqueteria/categoria.html', contexto)

def tags (request, tag):
    print tag
    x = Package.objects.filter(Labels__Tags__Value = tag)
    contexto = {"i":x}
    return render(request,'paqueteria/tags.html', contexto)

def busquedaForm(request):
    frase = ""
    form = busquedaPaquete()
    if request.method =="POST":
        formulario = busquedaPaquete(request.POST)
        if formulario.is_valid():
            frase = formulario.cleaned_data["frase"]
            pqt = Package.objects.filter(Package = frase.strip())
            print (pqt[0].Package, len(pqt))
            if len(pqt)>1:
                contexto = {"i":pqt,'form':form}
                return render(request,'paqueteria/organizador_arquitectura.html', contexto)
            else:
                contexto = {"i":pqt[0],'form':form}
                return render(request,'paqueteria/detalles.html', contexto)
    else:
        contexto   = {'form':form, "frase":frase}
    return render(request,'paqueteria/buscador.html',contexto)

def urlPaquetes(request, nombre):
    contexto = {}
    p = Package.objects.get(Package = nombre)
    contexto["paquete"] = p
    details_list = Details.objects.filter(package = p)
    dict_details = {}
    
    for det in details_list:
        dict_details[det.Architecture] = {}
        dict_details[det.Architecture]['data'] = det
        dict_details[det.Architecture]['relations'] = {}
        r = Relation.objects.filter(details = det).order_by("alt_id", "related_package",
                                                            "version")
        for n in r:
            if n.relation_type in relation_types:
                if not dict_details[det.Architecture]['relations'].has_key(n.relation_type):
                    dict_details[det.Architecture]['relations'][n.relation_type] = []
                dict_details[det.Architecture]['relations'][n.relation_type].append(n)
        #print dict_details[det.Architecture]['relations']
    contexto["raiz"] = raiz
    contexto["detalles"] = dict_details
    
    render_css = ['normalize', 'fonts', 'bootstrap', 'bootstrap-responsive',
                       'font-awesome', 'tribus', 'tribus-responsive']
    render_js = ['jquery', 'bootstrap']
    
    contexto['render_js'] = render_js
    contexto['render_css'] = render_css
    
    return render(request,'paqueteria/paquete.html', contexto)
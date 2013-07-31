# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, render_to_response
from tribus.web.paqueteria.models import Paquete, Mantenedor, DependenciaSimple, DependenciaOR, Etiqueta
from django.core.context_processors import request
from tribus.web.paqueteria.forms import busquedaPaquete
import string

def index(request):
    pqt = Paquete.objects.all()
    contexto = {"pqt":pqt}
    return render(request,'paqueteria/paquetes.html', contexto)

def categoria(request, categoria):
    print categoria
    x = Etiqueta.objects.all().filter(nombre=categoria)
    contexto = {"i":x}
    return render(request,'paqueteria/categoria.html', contexto)

def tags (request, tag):
    print tag
    x = Paquete.objects.all().filter(Tags__valores__valor=tag)
    contexto = {"i":x}
    return render(request,'paqueteria/tags.html', contexto)


# def search (request):
#     query = request.Get.get('q', '')
#     if query:
#         qset =(
#               Q(Mantenedor__nombre__icontains = query) ||
#               Q(Paquete__nombre__icontains = query) |
#               Q(Paquete__descripcion__icontains = query)
#               )
#         result = Paquete.objects.filter(qset).distinct()
#     else:
#         result = []
#     return render_to_response ("encuentas/search.html",{
#                                         "request" : request,
#                                         "query" : query} 
#                                )

def inicio (request):
    return render(request, 'paqueteria/inicio.html')


def busquedaForm(request):
    frase = ""
    form = busquedaPaquete()
    if request.method =="POST":
        formulario = busquedaPaquete(request.POST)
        if formulario.is_valid():
            frase = formulario.cleaned_data["frase"]
            pqt = Paquete.objects.filter(Package = frase.strip())
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


def busqueda(request, pqt):
    form = busquedaPaquete()
    l = string.splitfields(pqt, "&")
    if len(l)>1:
        x = Paquete.objects.get(Package = l[0], Architecture = l[1])
    else:
        x = Paquete.objects.get(Package = l[0])
    print (x.Package)
    contexto = {"i":x,'form':form}
    return render(request,'paqueteria/detalles.html', contexto)
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, render_to_response
from tribus.web.paqueteria.models import Paquete, Mantenedor, DependenciaSimple, DependenciaOR, Etiqueta
from django.core.context_processors import request
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
#               Q(Mantenedor__nombre__icontains = query) |
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

def busqueda(request, pqt):
    print pqt
    x = Paquete.objects.filter(Package = pqt)
    contexto = {"i":x}
    return render(request,'paqueteria/arqs.html', contexto)

def info(request, args):
    l = string.splitfields(args, "-")
    x = Paquete.objects.get(Package = l[0], Architecture = l[1])
    contexto = {"i":x}
    return render(request,'paqueteria/detalles.html', contexto)
# -*- coding: utf-8 -*-
from django.contrib import admin
from tribus.web.paqueteria.models import *

class PaqueteAlin(admin.TabularInline):
    model = Paquete
    extra = 0
    
class AdminMantenedor(admin.ModelAdmin):
    fieldsets = (
        ('Nombre del mantenedor', {
        'classes': ('wide', 'extrapretty',),
            'fields': ('nombre_completo',)
        }),

        ('Correo electronico', {
        'classes': ('wide', 'extrapretty',),
            'fields': ('correo',)
        }),
    )
    
    #inlines = [PaqueteAlin] # Descomentar para mostrar los paquetes que corresponden a cada mantenedor
    
    list_display = ('nombre_completo', 'correo')
    list_filter = ['nombre_completo']
    search_fields = ['nombre_completo']
    
class AdminPaquete(admin.ModelAdmin):
    fieldsets = (
        ('Nombre del paquete', {
        'classes': ('wide', 'extrapretty'),
            'fields': ('Package',)
        }),
                 
        ('Mantenedor del paquete', {
        'classes': ('wide', 'extrapretty'),
            'fields': ('Maintainer',)
        }),

        ('Version', {
        'classes': ('wide', 'extrapretty'),
            'fields': ('Version',)
        }),
        
        ('Multi Arquitectura', {
        'classes': ('wide', 'extrapretty'),
            'fields': ('MultiArch',)
        }),
        
        ('Suma MD5', {
        'classes': ('wide', 'extrapretty'),
            'fields': ('MD5sum',)
        }),
                 
        ('Etiquetas del paquete', {
        'classes': ('wide', 'extrapretty'),
            'fields': ('Tags',)
        }),
    )
    
    list_display = ('Package', 'Version', 'MD5sum')
    list_filter = ['Architecture', 'Priority']
    search_fields = ['Package']
    
admin.site.register(Etiqueta)
admin.site.register(ValorTag)
admin.site.register(ProveeOR)
admin.site.register(ProveeSimple)
admin.site.register(SugerenciaOR)
admin.site.register(SugerenciaSimple)
admin.site.register(RecomendacionOR)
admin.site.register(RecomendacionSimple)
admin.site.register(PreDependenciaSimple)
admin.site.register(PreDependenciaOR)
admin.site.register(DependenciaSimple)
admin.site.register(DependenciaOR)
admin.site.register(Paquete, AdminPaquete)
admin.site.register(Mantenedor, AdminMantenedor)
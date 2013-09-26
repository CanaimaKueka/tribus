#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.serializers.json import json
from django.core.urlresolvers import reverse
from tribus.web.user.forms import LoginForm, SignupForm
from tribus.web.models import *


# Create your views here.

TWEETS_EN_PAGE = 10         #La cantidad de tweets que se muestran por página
TWEETS_EN_PROFILE = 10      #La cantidad de tweets que se muestran en prefiles
MENSAJES_POR_CHAT = 20      #La cantidad de mensajes que se muestran en el chat
LONGITUD_MENSAJE_CHAT = 100 #La longitud máxima del mensaje de chat
TIEMPO_CONEXION = 60        #El tiempo que pasa para marcar usuarios desconectados
CHAT_BAN = []               #Usuarios baneados del chat
CHAT_TIMEOUT = 10           #El tiempo máximo de espera para que se cargue el chat
CHAT_LOOP = .5              #El tiempo que pasa hasta que se vuelve a cargarse el bucle

try:
    import cPickle as pickle
except ImportError:
    import pickle

from urllib import urlencode
import datetime, re, random
from time import time, sleep



def tour(request):
    data = {}
    context = RequestContext(request)
    return render_to_response('tour.html', data, context)

def index(request, page = 1):

    if request.user.is_authenticated():

        tribs = []
        t0 = TWEETS_EN_PAGE * (int(page) - 1)
        t1 = TWEETS_EN_PAGE + t0

        #profile = request.user.get_profile()       # Give me the user profile
        followers = [followers for f in request.user.followers.all()]
        follows = [follows for f in request.user.follows.all()]
        follows.append(request.user)

        tribs = Trib.objects.filter(user__in = follows).order_by('-date')[t0:t1]


        # for t in tribs:
        #     t.profile = Profile.objects.get(user__username = t.user)
        #     if t.retweet == True:
        #         rt = Tweet.objects.get(pk = int(t.contenido))
        #         rt.retwitteado = 1
        #         rt.retweetter = t.user
        #         rt.rt_id = t.id
        #         tweets.append(rt)
        #     else:
        #         tweets.append(t)

        render_css = ['normalize', 'fonts', 'font-awesome', 'bootstrap',
                        'bootstrap-responsive', 'tribus', 'tribus-responsive']
        render_js = ['jquery', 'bootstrap']

        return render_to_response(
            'index.html', {
                'p' : request.user,
                'next' : int(page) + 1,
                'page' : page,
                'prev' : int(page) - 1,
                'tribs' : tribs,
                'tribs_c' : len(tribs),
                'follows_c' : len(follows),
                'followers_c' : len(followers),
                'render_css': render_css,
                'render_js': render_js,
                #'trending' : tt(5, 200),
                #'recommended' : randuser(request.user, 3),
            }, RequestContext(request))

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

        return render_to_response(
            'init.html', {
                'signupform': signupform,
                'render_css': render_css,
                'render_js': render_js,
            },


            RequestContext(request)
        )

# def dashboard(request, page = 1):
#     if page < 2:
#         page = 1
#     n = TWEETS_EN_PAGE * (int(page) - 1)
#     if request.user.is_authenticated():
#         p = Profile.objects.get(user = request.user)
#         users = Follow.objects.filter(follower = p, activo = True) #Busca los users que sigue el usuario
#         users = [u.followed for u in users] #Hace que users sea un array de los usuarios que sigue
#         users.append(request.user) #Le agrega el usuario actual
#         tweets_ = Tweet.objects.filter(user__in = users, activo = True).order_by('-fecha')[n:n + TWEETS_EN_PAGE]

#         #Procesa retweets
#         tweets = []
#         for t in tweets_:
#             t.profile = Profile.objects.get(user__username = t.user)
#             if t.retweet == True:
#                 rt = Tweet.objects.get(pk = int(t.contenido))
#                 rt.retwitteado = 1
#                 rt.retweetter = t.user
#                 rt.rt_id = t.id
#                 tweets.append(rt)
#             else:
#                 tweets.append(t)

#         return render_to_response('dashboard',
#         {
#             'logueado' : request.user,
#             'p' : Profile.objects.get(user = request.user),
#             'next' : int(page) + 1,
#             'page' : page,
#             'prev' : int(page) - 1,
#             'tweets' : tweets,
#             'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#             'u_siguiendo' : len(Follow.objects.filter(activo = True,
#                 follower = Profile.objects.get(user = request.user))),
#             'u_seguidores' : len(Follow.objects.filter(activo = True,
#                 followed = request.user)),
#             'index' : True,
#             'trending' : tt(5, 200),
#             'seguir' : randuser(request.user, 3),
#         }, RequestContext(request))
#     else:
#         return HttpResponseRedirect('/login/')


# def borrar(request, tweet_id):
#     t = get_object_or_404(Tweet, id = tweet_id)
#     if t.user == request.user or request.user.is_staff: #El usuario actual es el propietario del tweeet
#         t.activo = False
#         t.save()
#     return HttpResponseRedirect(reverse('twitter.views.index'))

# def buscar(request, page = 1):
#     if not request.user.is_authenticated():
#         return HttpResponse('Usted no esta logueado')
#     if page < 2:
#         page = 1
#     if request.GET.has_key('busqueda'):
#         n = TWEETS_EN_PAGE * (int(page) - 1)
#         t = Tweet.objects.filter(activo = True, contenido__icontains = request.GET['busqueda']).order_by('-fecha')[n:n + TWEETS_EN_PAGE]
#         return render_to_response('twitter/index.html',
#         {
#             'logueado' : request.user,
#             'p' : Profile.objects.filter(user = request.user),
#             'next' : int(page) + 1,
#             'page' : page,
#             'prev' : int(page) - 1,
#             'tweets' : t,
#             'page_prefix' : 'buscar/',
#             'page_sufix' : '?%s' % urlencode({'busqueda' : request.GET['busqueda']}),
#             'busqueda' : request.GET['busqueda'],
#             'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#             'u_seguidores' : len(Follow.objects.filter(activo = True,
#                 follower = Profile.objects.get(user = request.user))),
#             'u_siguiendo' : len(Follow.objects.filter(activo = True,
#                 followed = request.user)),
#         }, RequestContext(request))
#     else:
#         return HttpResponseRedirect(reverse('twitter.views.index'))

# def conf(request):
#     u = request.user
#     p = get_object_or_404(Profile, user = u)
#     try:
#         if not u.check_password(request.POST['oldpass']):
#             return render_to_response('twitter/conf.html',{
#                 'mensaje' : '<h3>Introduzca su contraseÃ±a actual correctamente</h3>',
#                 'nombre' : u.first_name,
#                 'apellido' : u.last_name,
#                 'email' : u.email,
#                 'ubicacion' : p.ubicacion,
#                 'bio' : p.frase,
#                 'logueado' : request.user,
#                 'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#                 'u_seguidores' : len(Follow.objects.filter(activo = True,
#                     follower = Profile.objects.get(user = request.user))),
#                 'u_siguiendo' : len(Follow.objects.filter(activo = True,
#                     followed = request.user)),
#                 'p' : Profile.objects.get(user = request.user),
#                 }, RequestContext(request))
#         if request.POST['procesa'] == 'profile':
#             u.first_name = request.POST['firstname']
#             u.last_name = request.POST['lastname']
#             u.email = request.POST['email']
#             u.save()

#             p.ubicacion = request.POST['ubicacion']
#             p.frase = request.POST['bio']
#             p.avatar = request.POST['avatar']
#             p.save()
#         elif request.POST['procesa'] == 'pass':
#             if request.POST['pass'] == request.POST['pass2']:
#                 u.set_password(request.POST['pass'])
#                 u.save()
#                 logout(request)
#                 return HttpResponseRedirect(reverse('twitter.views.index'))
#             else:
#                 return render_to_response('twitter/conf.html',{
#                     'mensaje' : 'Las contraseÃ±as no coinciden',
#                     'p' : Profile.objects.get(user = request.user),
#                     'nombre' : u.first_name,
#                     'apellido' : u.last_name,
#                     'email' : u.email,
#                     'ubicacion' : p.ubicacion,
#                     'bio' : p.frase,
#                     'logueado' : request.user,
#                     'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#                     'u_seguidores' : len(Follow.objects.filter(activo = True,
#                         follower = Profile.objects.get(user = request.user))),
#                     'u_siguiendo' : len(Follow.objects.filter(activo = True,
#                         followed = request.user)),
#                     }, RequestContext(request))
#         return HttpResponseRedirect(reverse('twitter.views.conf'))
#     except KeyError:
#         return render_to_response('twitter/conf.html',{
#             'p' : Profile.objects.get(user = request.user),
#             'nombre' : u.first_name,
#             'apellido' : u.last_name,
#             'email' : u.email,
#             'ubicacion' : p.ubicacion,
#             'bio' : p.frase,
#             'avatar' : p.avatar,
#             'logueado' : request.user,
#             'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#             'u_seguidores' : len(Follow.objects.filter(activo = True,
#                 follower = Profile.objects.get(user = request.user))),
#             'u_siguiendo' : len(Follow.objects.filter(activo = True,
#                 followed = request.user)),
#             }, RequestContext(request))

# def conversacion(request, conversacion, page = 1):
#     if page < 2:
#         page = 1
#     n = TWEETS_EN_PAGE * (int(page) - 1)
#     tweets = []
#     t = get_object_or_404(Tweet, pk = conversacion)
#     tweets.append(t)
#     while t.respuesta: #Mientras este contestando a otro tweet
#         t = get_object_or_404(Tweet, pk = int(t.respuesta))
#         tweets.append(t)
#     return render_to_response('twitter/index.html',
#     {
#         'logueado' : request.user,
#         'p' : Profile.objects.get(user = request.logueado),
#         'next' : int(page) + 1,
#         'page' : page,
#         'prev' : int(page) - 1,
#         'tweets' : tweets,
#         'page_prefix' : 'conversacion/%s/' % conversacion,
#         'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#         'u_siguiendo' : len(Follow.objects.filter(activo = True,
#             follower = Profile.objects.get(user = request.user))),
#         'u_seguidores' : len(Follow.objects.filter(activo = True,
#             followed = request.user)),
#     }, RequestContext(request))

# def follow(request):
#     try:
#         user = request.POST['user']
#     except KeyError:
#         return HttpResponseRedirect(reverse('twitter.views.index'))
    
#     u = get_object_or_404(User, username = user)
#     f = Follow.objects.filter(follower__user =request.user, followed = u)
#     if f: #Ya hay algun follow del mismo usuario, se cambia el activo en vez de crear uno nuevo
#         f = f[0]
#         f.activo = not f.activo #Si lo esta siguiendo lo deja de seguir, sino lo sigue
#         f.save()
#     else: #Crea un nuevo objecto folllow
#         f = Follow.objects.create(
#             fecha = datetime.datetime.now(),
#             activo = True,
#             follower = Profile.objects.get(user = request.user),
#             followed = u
#         )
#         f.save()
#     return HttpResponseRedirect(reverse('twitter.views.profile', args=(user,)))

# def profile(request, username, page = 1):
#     if page < 2:
#         page = 1
#     n = TWEETS_EN_PROFILE * (int(page) - 1)
#     u = get_object_or_404(User, username=username)

#     p = Profile.objects.get(user = request.user) #El perfil del usuario
#     f = Follow.objects.filter(follower = p, activo = True) #Los objetos follow activos
#     f = [user.followed for user in f] #Convierte f a un array de usuarios que sigue

#     #Procesa retweets
#     tweets_ = u.tweet_set.all().filter(activo = True).order_by('-fecha')
#     tweets = []
#     for t in tweets_:
#         t.profile = Profile.objects.get(user = t.user)
#         if t.retweet == True:
#             rt = Tweet.objects.get(pk = int(t.contenido))
#             rt.retwitteado = 1
#             rt.retweetter = t.user
#             rt.rt_id = t.id
#             tweets.append(rt)
#         else:
#             tweets.append(t)

#     return render_to_response('twitter/profile.html',
#     {
#         'following' : (u in f),
#         'length' : len(tweets),
#         'logueado' : request.user,
#         'p' : Profile.objects.get(user = request.user),
#         'next' : int(page) + 1,
#         'page' : page,
#         'prev' : int(page) - 1,
#         'profile' : get_object_or_404(Profile, user=u),
#         'tweets' : tweets[n:n + TWEETS_EN_PROFILE],
#         'user' : u,
#         'siguiendo' : f,
#         'seguidores' : Follow.objects.filter(activo = True, followed = u),
#         'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#         'u_siguiendo' : len(Follow.objects.filter(activo = True,
#             follower = Profile.objects.get(user = request.user))),
#         'u_seguidores' : len(Follow.objects.filter(activo = True,
#             followed = request.user)),
#     }, RequestContext(request))

# def responder(request, tweet_id):
#     return render_to_response('twitter/responder.html',
#     {
#         'logueado' : request.user,
#         'tweet' : get_object_or_404(Tweet, pk = tweet_id), 
#         'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#         'u_siguiendo' : len(Follow.objects.filter(activo = True,
#             follower = Profile.objects.get(user = request.user))),
#         'u_seguidores' : len(Follow.objects.filter(activo = True,
#             followed = request.user)),
#     }, RequestContext(request))

# def retweet(request, tweet_id):
#     if request.POST.has_key('confirma'):
#         #Procesa
#         t = Tweet.objects.create(
#             user = request.user,
#             fecha = datetime.datetime.now(),
#             contenido = str(tweet_id),
#             retweet = True #Indica que es retweet, el contenido es el id del tweet original
#         )
#         t.save()
#         return HttpResponseRedirect(reverse('twitter.views.index'))
#     else:
#         return render_to_response('twitter/retweet.html',
#         {
#             'logueado' : request.user,
#             'p' : Profile.objects.get(user = request.user),
#             'tweet' : get_object_or_404(Tweet, id = tweet_id),
#             'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#             'u_siguiendo' : len(Follow.objects.filter(activo = True,
#                 follower = Profile.objects.get(user = request.user))),
#             'u_seguidores' : len(Follow.objects.filter(activo = True,
#                 followed = request.user)),
#         }, RequestContext(request))

# def seguidores(request, method, username):
#     u = get_object_or_404(User, username = username)
#     p = get_object_or_404(Profile, user__username = username)
#     if method == 'seguidores':
#         u = Follow.objects.filter(followed = u, activo = True).order_by('-fecha')
#         u = [f.follower.user for f in u]
#     elif method == 'siguiendo':
#         u = Follow.objects.filter(follower = p, activo = True).order_by('-fecha')
#         u = [f.followed for f in u]
    
#     for n in range(len(u)):
#         u[n].profile = get_object_or_404(Profile, user = u[n])

#     return render_to_response(
#     'twitter/seguidores.html',
#     {
#         'logueado' : request.user,
#         'p' : Profile.objects.get(user = request.user),
#         'users' : u,
#         'ntweets' : len(Tweet.objects.filter(user = request.user, activo = True)),
#         'u_siguiendo' : len(Follow.objects.filter(activo = True,
#             follower = Profile.objects.get(user = request.user))),
#         'u_seguidores' : len(Follow.objects.filter(activo = True,
#             followed = request.user)),
#     }, RequestContext(request))

# def tweet(request):
#     try:
#         content = request.POST['content']
#     except KeyError:
#         return HttpResponseRedirect(reverse('twitter.views.index'))
#     try:
#         respuesta = int(request.POST['respuesta'])
#     except (KeyError, ValueError):
#         respuesta = None
    
#     if respuesta is None:
#         t = Tweet.objects.create(
#             user = request.user,
#             fecha = datetime.datetime.now(),
#             contenido = content,
#         )
#     else:
#         t = Tweet.objects.create(
#             user = request.user,
#             fecha = datetime.datetime.now(),
#             contenido = content,
#             respuesta = respuesta,
#         )
#     t.save()
#     return HttpResponseRedirect(reverse('twitter.views.index'))

# def tt(n = 1, limit = None):
#     hashtags = {}
#     if limit is None:
#         tweets = Tweet.objects.all()
#     else:
#         tweets = Tweet.objects.all().order_by('-fecha')[:limit]
#     for tweet in tweets:
#         f = re.findall('#[a-zA-Z0-9]+', tweet.contenido)
#         #print 'f',f
#         for hashtag in f:
#             hashtag = hashtag.lower()
#             if not hashtag in hashtags:
#                 hashtags[hashtag] = 1
#             else:
#                 hashtags[hashtag] += 1
    
#     ordenar = []
#     for hashtag in hashtags.keys():
#         ordenar.append((hashtags[hashtag], hashtag))
#     ordenar = sorted(ordenar)
#     ordenar.reverse()

#     final = []
#     for e in ordenar[:n]:
#         final.append(e[1][1:])
#     return final

# def randuser(user, n = 1):
#     users = User.objects.all()
#     final = []
#     for x in range(0,n):
#         """ Se vuelve a ejectutar salvo que se llegue al lÃ­mite o que se haya
#         encontrado un usuario """
#         rebuscar, i = True, 0
#         while rebuscar and i<len(users):
#             i += 1
#             r = random.randint(0, len(users) - 1)
#             u = users[r]
#             p = Profile.objects.get(user = user)
#             if (not Follow.objects.filter(follower = p, followed = u) and
#                 (not u in final) and (user != u)):
#                 """ Si el usuario aleatorio nunca fue seguido por el otro """
#                 rebuscar = False
#                 final.append(u)
#     return final


# def chat(request):
#     if not request.user.is_authenticated():
#         return HttpResponse('Debe loguarse')
#     if request.POST.get('accion', '') == 'send':
#         mensaje = request.POST.get('mensaje', '')
#         u_ = request.user
#         u = u_.username
#         left = '<a href="%s">@%s</a>: ' % (reverse('twitter.views.profile', args=(u,)),u)
#         mensaje = mensaje[:LONGITUD_MENSAJE_CHAT]
#         mensaje = mensaje.replace('&', '&amp;')
#         mensaje = mensaje.replace('<', '&lt;')
#         mensaje = mensaje.replace('>', '&gt;')
#         final = left + mensaje
#         m = Chat.objects.create(
#             usuario = u_,
#             mensaje = request.POST.get('mensaje', ''))
#         m.save()
    
#     #Actualiza el estado del usuario
#     f = Conectado.objects.filter(usuario = request.user)
#     if f:
#         #Ya se conectó alguna vez
#         f = f[0]
#         f.tiempo = time()
#         f.save()
#     else:
#         f = Conectado.objects.create(
#             usuario = request.user,
#             tiempo = time())
#         f.save()
#     c = []
#     for f in Conectado.objects.all():
#         if time() - float(f.tiempo) <= TIEMPO_CONEXION:
#             u = f.usuario
#             c.append(u.username)

#     obj_ = Chat.objects.all().order_by('-id')[:MENSAJES_POR_CHAT]
#     obj = []
#     for o in obj_:
#         u = o.usuario.username
#         mensaje = o.mensaje
#         mensaje = mensaje[:LONGITUD_MENSAJE_CHAT]
#         mensaje = mensaje.replace('&', '&amp;')
#         mensaje = mensaje.replace('<', '&lt;')
#         mensaje = mensaje.replace('>', '&gt;')
#         final = (u, mensaje)
#         obj.append(final)
#     json = {'conectados' : c, 'mensajes' : obj}
#     return HttpResponse(simplejson.dumps(json))

# def ajaxtw(request):
#     tweet_id = request.GET.get('id', '0')
#     busqueda = request.GET.get('busqueda', '')
#     perfil = request.GET.get('perfil', '')
#     if busqueda:
#         tweets_ = Tweet.objects.filter(activo = True, contenido__icontains = busqueda, \
#             id__gt = int(tweet_id))
#     elif perfil:
#         tweets_ = Tweet.objects.filter(activo = True, user__username = perfil,
#             id__gt = int(tweet_id))
#     else:
#         p = Profile.objects.get(user = request.user)
#         users = Follow.objects.filter(follower = p, activo = True) #Busca los users que sigue el usuario
#         users = [u.followed for u in users] #Hace que users sea un array de los usuarios que sigue
#         users.append(request.user) #Le agrega el usuario actual
#         tweets_ = Tweet.objects.filter(user__in = users, activo = True, \
#             id__gt = int(tweet_id))
#     tweets_ = tweets_.order_by('-fecha')[:TWEETS_EN_PAGE]
#     tweets = []
#     for t in tweets_:
#         if t.retweet:
#             rt = Tweet.objects.get(pk = int(t.contenido))
#             tweets.append({
#                 'user' : rt.user.username,
#                 'contenido' : rt.filtrar(),
#                 'pk' : rt.pk,
#                 'tpk' : t.pk,
#                 'name' : rt.user.get_full_name(),
#                 'fecha' : str(rt.fecha),
#                 'retweet' : t.user.username,
#                 'avatar' : Profile.objects.get(user = rt.user).avatar,
#                 })
#         else:
#             tweets.append({
#                 'user' : t.user.username,
#                 'contenido' : t.filtrar(),
#                 'pk' : t.pk,
#                 'tpk' : t.pk,
#                 'name' : t.user.get_full_name(),
#                 'fecha' : str(t.fecha),
#                 'retweet' : False,
#                 'avatar' : Profile.objects.get(user = t.user).avatar,
#                 })
#     return HttpResponse(simplejson.dumps(tweets))

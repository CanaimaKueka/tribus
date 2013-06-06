from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import re
from urllib import urlencode

# Create your models here.
class Tweet(models.Model):
	def __unicode__(self):
		return self.contenido
	user = models.ForeignKey(User)
	fecha = models.DateTimeField()
	contenido = models.CharField(max_length = 140)
	retweet = models.BooleanField(default = False, blank = True)
	activo = models.BooleanField(default  =True)
	respuesta = models.IntegerField(null = True, blank = True)
	def filtrar(self):
		"""Filtra XSS enlaza hashtags, menciones y enlaces """
		t = self.contenido

		#Anti XSS
		t = t.replace('&','&amp;')
		t = t.replace('<','&lt;')
		t = t.replace('>','&gt;')
		t = t.replace('\'','&#39;')
		t = t.replace('"','&quot;')

		hashtags = re.findall('#[a-zA-Z][a-zA-Z0-9_]*', t)
		for hashtag in hashtags:
			t = t.replace(hashtag, '<a href="/twitter/buscar/?%s">%s</a>' % (urlencode({'busqueda':hashtag}), hashtag))

		links = re.findall('http\\:\\/\\/[^ ]+', t)
		for link in links:
			t = t.replace(link, '<a href="%s">%s</a>' % (link, link))

		menciones = re.findall('\\@[a-zA-Z0-9_]+', t)
		for mencion in menciones:
			t = t.replace(mencion, '<a href="/twitter/profile/%s/">%s</a>' % (mencion[1:], mencion))

		return t


class Profile(models.Model):
	def __unicode__(self):
		return str(self.user)
	user = models.ForeignKey(User)
	frase = models.CharField(max_length = 160)
	ubicacion = models.CharField(max_length = 50)
	avatar = models.CharField(max_length = 256)

class Follow(models.Model):
	fecha = models.DateTimeField()
	activo = models.BooleanField()
	follower = models.ForeignKey(Profile)
	followed = models.ForeignKey(User)

class Chat(models.Model):
	usuario = models.ForeignKey(User)
	mensaje = models.CharField(max_length = 200)

class Conectado(models.Model):
	usuario = models.ForeignKey(User)
	tiempo = models.DecimalField(max_digits = 20, decimal_places = 5)

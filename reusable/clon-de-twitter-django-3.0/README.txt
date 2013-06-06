Clon de Twitter programado en Django
v3.0

sh4r3m4n
twitter.com/sh4r3m4n
licenciapaprahackear.wordpress.com

Esta aplicaci�n se encuentra bajo licencia Creative Commons, visible en
http://creativecommons.org/licenses/by/2.5/ar/

Instalaci�n:
1) Descomprima los ficheros del archivo descargado.
2) Copie el directorio twitter al directorio de su sitio Django
3) Copie el directorio templates al directorio de su sitio Django donde se
   encuentren las plantillas
4) Copie el directorio static al directorio de su sitio Django donde se
   encuentren los archivos est�ticos
5) En el archivo settings.py de su sitio Django, inserte la siguiente l�nea
   en INSTALLED_APPS:
    'twitter',
6) Inserte la siguiente l�nea en el urlpatterns del archivo urls.py de su
   sitio Django:
    url('^twitter/', include('twitter.urls')),
7) Ejecute el comando manage.py syncdb
8) Ponga en ejecuci�n el servidor ejecutando manage.py runserver

Cambios respecto a la tercera versi�n(entre otros):
 . Se agrega un chat en un panel lateral y en una ventana modal
 . Cuando se twetea algo nuevo, aparece un indicador "x nuevos tweets"
 . Cada usuario puede elegir su avatar, incluyendo la URL a una imagen en su
 perfil
 . Se redimensiona la imagen de perfil del panel izquiero en todas las p�ginas
 . Los d�gitos m�ximos del campo tiempo en el modelo conectados ocupa menos
   espacio, para ser compatible con MySQL
 . Documentaci�n en variables principales de views.py
 . Se borran URLs a views de prueba, no implementadas

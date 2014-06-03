======
Tribus
======



Documentación para usuarios
===========================

TODO

.. _tutorial:

Tutorial
--------

TODO

.. toctree::
    :hidden:

    tutorial

.. _usage_docs:

Documentación de uso
--------------------

TODO

.. toctree::
    :maxdepth: 1
    :glob:

    usage/*

.. _faq:

Preguntas más frecuentes
------------------------

TODO

.. toctree::
    :hidden:

    faq

Documentación para administradores de plataforma
================================================

Esta sección describe todos los procedimientos necesarios para entender cómo instalar y publicar una instancia funcional de Tribus, así como también personalizar la configuración dependiendo de las necesidades del usuario. No es necesario ser un operador de plataforma para instalar una instancia de Tribus, pero si debe estar familiarizado con los comandos básicos de consola bajo ambiente GNU/Linux.

.. _installation:

Instalación
-----------

La forma más fácil de instalar Tribus es a través de los paquetes de instalación hechos especialmente para tu distribución GNU/Linux. Estos paquetes permiten manejar las dependencias y la gestión de servicios de una manera más automatizada, sin que tengas que preocuparte de realizar configuraciones a mano. Para mayor información sobre las instrucciones de instalación y descarga de paquetes, consulta la página de :doc:`instalación <installation>`.

Aunque recomendamos el uso de los paquetes para tu distribución, existen otros métodos de instalación. Tribus puede instalarse a través de un gestor de paquetes python como ``setuptools``, ``pip`` o ``easy_install`` desde el repositorio de paquetes python `pypi <http://pypi.python.org/>`_. También puede instalarse de la misma forma a través de su código fuente, que puede obtenerse a clonando el repositorio git o descargando un archivo comprimido.

Para mayor información, consulte las :doc:`instrucciones detalladas de instalación <installation>`.

.. toctree::
    :hidden:

    installation

Configuración
-------------

TODO

.. toctree::
    :maxdepth: 2
    :glob:

    configuration/*


Documentación para desarrolladores
==================================

Esta sección describe cuales son las herramientas y normas para colaborar con el desarrollo de Tribus.

Generalmente se recomienda empezar leyendo sobre la :doc:`estructura del proyecto <development/where>`, permitiendo así encontrar las cosas más rápido y/o saber donde colocar ciertos elementos. También es indispensable leer el :doc:`protocolo de contribuciones <development/contributing>`, el cual contiene los pasos más importantes para agregar una contribución en Tribus. Seguidamente, las :doc:`herramientas de mantenimiento y desarrollo <development/maintaining>` describen un conjunto de rutinas que han sido escritas para asistir al desarrollador en sus tareas. También están disponibles los :doc:`estilos de programación <development/style>` sugeridos.

Para pasar directamente a una tarea, lee las :doc:`hojas de ruta <development/roadmap>` que están en desarrollo y sigue las instrucciones del :doc:`protocolo de contribuciones <development/contributing>`. También están disponibles las :doc:`listas de cambios <development/changelog>` para versiones pasadas.

.. toctree::
    :maxdepth: 2

    development/concepts
    development/where
    development/contributing
    development/maintaining
    development/style
    development/reusable
    development/roadmap
    development/changelog

.. _api_docs:

Documentación de la API
-----------------------

Incompleto

.. toctree::
    :maxdepth: 1
    :glob:

    development/api/*
	
Get a single user
~~~~~~~~~~~~~~~~~

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/details/55

.. http:method:: GET /api/0.1/user/details/{id}

   :arg id: user id.

.. http:response:: Retrieve user details by id.

   .. sourcecode:: js

		{
		  "date_joined": "2013-12-10T22:20:50.060012",
		  "description": "Developer",
		  "email": "alexander.salas@gmail.com",
		  "first_name": "Alexander Javier",
		  "id": 55,
		  "last_login": "2014-02-26T19:58:04.112944",
		  "last_name": "Salas Bastidas",
		  "location": null,
		  "resource_uri": "/api/0.1/user/details/55",
		  "telefono": null,
		  "user_profile": "/api/0.1/user/profile/55",
		  "username": "alexandersalas"
		}

Get the authenticated user
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/details

.. http:method:: GET /api/0.1/user/details

.. http:response:: Retrieve user details.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 1
		  },
		  "objects": [
			{
			  "date_joined": "2013-12-10T22:20:50.060012",
			  "description": "Developer",
			  "email": "alexander.salas@gmail.com",
			  "first_name": "Alexander Javier",
			  "id": 55,
			  "last_login": "2014-02-26T19:58:04.112944",
			  "last_name": "Salas Bastidas",
			  "location": null,
			  "resource_uri": "/api/0.1/user/details/55",
			  "telefono": null,
			  "user_profile": "/api/0.1/user/profile/55",
			  "username": "alexandersalas"
			}
		  ]
		}

Get all users
~~~~~~~~~~~~~
This provides all user profile.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/profile

.. http:method:: GET /api/0.1/user/details

.. http:response:: Retrieve the first 20 users profile on tribus.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": "/api/0.1/user/profile?limit=20&offset=20",
			"offset": 0,
			"previous": null,
			"total_count": 210
		  },
		  "objects": [
			{
			  "followers": [
				
			  ],
			  "follows": [
				
			  ],
			  "id": 37,
			  "resource_uri": "/api/0.1/user/profile/37",
			  "user": "/api/0.1/user/details/37"
			}
		  ]
		}
		
List followers of a user
~~~~~~~~~~~~~~~~~~~~~~~~
List a user’s followers.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/followers/55

.. http:method:: GET /api/0.1/user/followers/{id}

   :arg id: user id.

.. http:response:: Retrieve the first 20 followers from the id.

   .. sourcecode:: js

		Unimplemented

List the authenticated user’s followers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/followers

.. http:method:: GET /api/0.1/user/followers

.. http:response:: Retrieve the first 20 followers.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 8
		  },
		  "objects": [
			{
			  "date_joined": "2013-12-10T23:39:48.460212",
			  "description": "Este es mi perfil en Tribus!",
			  "email": "el.wuilmer@gmail.com",
			  "first_name": "Wuilmer",
			  "id": 59,
			  "last_login": "2014-02-26T20:29:58.903555",
			  "last_name": "Bolivar",
			  "location": null,
			  "resource_uri": "/api/0.1/user/followers/59",
			  "telefono": null,
			  "username": "ElWuilMeR"
			}
		  ]
		}
		
List of follows of a user
~~~~~~~~~~~~~~~~~~~~~~~~
List a user’s follows:

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/follows

.. http:method:: GET /api/0.1/user/follows/{id}

   :arg id: user id.

.. http:response:: Retrieve the first 20 followed users from the id.

   .. sourcecode:: js
   
		Unimplemented
		
List the authenticated user’s follows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/follows

.. http:method:: GET /api/0.1/user/follows

.. http:response:: Retrieve the first 20 follows.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 6
		  },
		  "objects": [
			{
			  "date_joined": "2013-12-10T23:39:48.460212",
			  "description": "Este es mi perfil en Tribus!",
			  "email": "el.wuilmer@gmail.com",
			  "first_name": "Wuilmer",
			  "id": 59,
			  "last_login": "2014-02-26T20:29:58.903555",
			  "last_name": "Bolivar",
			  "location": null,
			  "resource_uri": "/api/0.1/user/follows/59",
			  "telefono": null,
			  "username": "ElWuilMeR"
			}
		  ]
		}
		
Get all tribs
~~~~~~~~~~~~~
This provides all post on tribus ordering by publication date.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/tribs

.. http:method:: GET /api/0.1/user/tribs

.. http:response:: Retrieve the first 20 posts on tribus.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": "/api/0.1/user/tribs?limit=20&offset=20",
			"offset": 0,
			"previous": null,
			"total_count": 79
		  },
		  "objects": [
			{
			  "author_email": "luis@huntingbears.com.ve",
			  "author_first_name": "Luis Alejandro",
			  "author_id": 8,
			  "author_last_name": "MartÃ­nez Faneyth",
			  "author_username": "HuntingBears",
			  "id": "52a3f386ff600f7079173e7d",
			  "resource_uri": "/api/0.1/user/tribs/52a3f386ff600f7079173e7d",
			  "trib_content": "Este es mi primer mensaje en Tribus.",
			  "trib_pub_date": "2013-12-07T20:20:40.541Z"
			}
		  ]
		}
		
Get all tribs from author
~~~~~~~~~~~~~~~~~~~~~~~~~~
This provides all post from the author ordering by publication date.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/user/tribs/55

.. http:method:: GET /api/0.1/user/tribs/{author_id}

   :arg author_id: user id.

.. http:response:: Retrieve the first 20 tribs from the id author.

   .. sourcecode:: js
   
		Unimplemented

		
Get all comments of tribs
~~~~~~~~~~~~~~~~~~~~~~~~~
This provides all comments from all tribs ordering by publication date.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/tribs/comments

.. http:method:: GET /api/0.1/tribs/comments

.. http:response:: Retrieve the first 20 comments of all tribs.

   .. sourcecode:: js

		{
		  "meta": {
			"limit": 20,
			"next": "/api/0.1/tribs/comments?limit=20&offset=20",
			"offset": 0,
			"previous": null,
			"total_count": 58
		  },
		  "objects": [
			{
			  "author_email": "luis@huntingbears.com.ve",
			  "author_first_name": "Luis Alejandro",
			  "author_id": 8,
			  "author_last_name": "MartÃ­nez Faneyth",
			  "author_username": "HuntingBears",
			  "comment_content": "Este es mi primer comentario en Tribus.",
			  "comment_pub_date": "2013-12-07T20:20:55.370Z",
			  "id": "52a3f395ff600f7079173e7e",
			  "resource_uri": "/api/0.1/tribs/comments/52a3f395ff600f7079173e7e",
			  "trib_id": "52a3f386ff600f7079173e7d"
			}
		  ]
		}

		
Get all comments of trib
~~~~~~~~~~~~~~~~~~~~~~~~
This provides all comments from the trib id ordering by publication date.

Note: The pagination info is included in the meta object. It is important to follow these meta object values instead of constructing your own URLs.

::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/tribs/comments/52a3f386ff600f7079173e7d

.. http:method:: GET /api/0.1/tribs/comments/{trib_id}

   :arg trib_id: trib id.

.. http:response:: Retrieve the first 20 comments of the trib.

   .. sourcecode:: js

		Unimplemented
		
Search User or Package Resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. http:method:: GET /api/0.1/search?q={search_term}

   :arg search_term: Perform search with this term.
   
::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/search?q=luisalejandro
    

.. http:response:: Retrieve a list of Users objects that contain the search term.

   .. sourcecode:: js
   
		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 1
		  },
		  "objects": [
			{
			  "packages": [
				
			  ],
			  "users": [
				{
				  "fullname": "Luis Alejandro MartÃ­nez Faneyth",
				  "username": "luisalejandro"
				}
			  ]
			}
		  ]
		}
		
::

    http://tribus.canaima.softwarelibre.gob.ve/api/0.1/search?q=0ad
    

.. http:response:: Retrieve a list of Package objects that contain the search term.

   .. sourcecode:: js
   
		{
		  "meta": {
			"limit": 20,
			"next": null,
			"offset": 0,
			"previous": null,
			"total_count": 1
		  },
		  "objects": [
			{
			  "packages": [
				{
				  "name": "0ad-data"
				},
				{
				  "name": "0ad"
				},
				{
				  "name": "0ad-dbg"
				}
			  ],
			  "users": [
				
			  ]
			}
		  ]
		}

.. _roadmap:

Hojas de ruta
-------------

Las hojas de ruta contienen la planificación establecida para las próximas versiones Tribus.

Para mayor información, consulte :doc:`el Roadmap <development/roadmap>`.

.. _changelog:

Lista de cambios
----------------

La lista de cambios contiene información acerca de la lista de cambios que han sido introducidos para las diferentes versiones de Tribus.

Para mayor información, consulte :doc:`el Changelog <development/changelog>`.

.. _license:

Licencia de distribución
------------------------

Tribus está licenciado bajo **GPL-3**. Todas las contribuciones hechas por otros desarrolladores serán redistribuídas dentro de Tribus bajo la misma licencia, a menos que se especifique lo contrario. Es necesario hacer notar que las porciones de código que estén licenciadas bajo términos incompatibles con los de la licencia GPL-3 y deseen ser incorporados a Tribus, serán objeto de rechazo.

.. toctree::
    :maxdepth: 1

    copying
    contributors
    license

.. _help:

Obtener ayuda
=============

Si ya has leído el :ref:`tutorial`, la :ref:`usage_docs`, las :ref:`faq` y la :ref:`api_docs`, y no has podido encontrar la solución a tus problemas, puedes consultar a alguno de los recursos que se listan más abajo. Sin embargo, asegúrate de leer bien todos los recursos de documentación que están disponibles **antes** de hacer un ticket de error o enviar un correo a la lista.

.. _mail_list:

Foro
----

La manera más expedita de conseguir ayuda con Tribus es a través del `foro <https://groups.google.com/forum/#!forum/tribusdev>`_. Los desarrolladores de Tribus hacen su mejor esfuerzo para contestar rápidamente, ten un poco de paciencia si no te responden inmediatamente.

Bugs/ticket tracker
-------------------

Puedes revisar si ya se ha reportado un error relacionado con el problema que estás presentando en el gestor de `tickets <https://github.com/CanaimaGNULinux/tribus/issues>`_.

Twitter
-------

Tribus tiene una cuenta de twitter `@tribusdev <http://twitter.com/tribusdev>`_, la cual es utilizada para anuncios, información acerca del desarrollo, soporte e información relacionada.

Grupo en Facebook
-----------------

Diversas cosas pueden compartirse en el `Grupo de Facebook <https://www.facebook.com/groups/tribusdev>`_.

IRC
---

Existe un canal IRC, en donde los desarrolladores comúnmente se reúnen: `tribus en FreeNode <http://webchat.freenode.net/?channels=tribus&uio=MTE9NTE3a>`_.



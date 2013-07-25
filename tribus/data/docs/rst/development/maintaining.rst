==========================================
Herramientas de mantenimiento y desarrollo
==========================================

Tribus necesita de una serie de herramientas, servicios y configuraciones iniciales para poder ejecutar las tareas rutinarias de desarrollo (p. ej. iniciar el servidor de desarrollo de *Django*, autenticar usuarios de prueba contra *OpenLDAP*, et. al.). Conforme el proceso de desarrollo va avanzando, las dependencias que necesita Tribus para funcionar van cambiando y necesitan ser corregidas de la forma más sencilla posible.

Para facilitar esto, Tribus contiene una serie de comandos que asisten en las tareas de mantenimiento y desarrollo. Para ello, se utilizan una serie de scripts escritos en `Make <http://make.org/>`_ y `Fabric <http://fabfile.org>`_.

Se recomienda trabajar en un sistema Debian Sid, Debian Testing o en su defecto, Canaima 4.0 o Ubuntu 13.04.

.. _make_environment:

Recreando el ambiente de desarrollo
-----------------------------------

::

	make environment

Tribus utiliza `Virtualenv <http://virtualenv.org/>`_ para crear un entorno aislado de ejecución en Python. Esto permite que los accidentes e inestabilidades propias del proceso de desarrollo no afecten directamente el entorno de trabajo del desarrollador, mientras que a su vez, permite instalar las últimas versiones de paquetes python sin preocuparse de los problemas de dependencias del sistema huésped.

Este comando además instalará los paquetes indispensables para el funcionamiento de los servicios (OpenLDAP, PostgreSQL, Redis, Celery, et. al.), entre otras tareas:

* Instalar las dependencias de construcción listadas en ``tribus/config/data/debian-dependencies.list``.
* Configurar el Servidor OpenLDAP con las siguientes características:

	* Domain: ``tribus.org``
	* Base: ``dc=tribus,dc=org``
	* Admin DN: ``cn=admin,dc=tribus,dc=org``
	* Admin Password: ``tribus``

* Borrar todas las entradas de usuario del OpenLDAP.
* Agregar un usuario de pruebas ``uid=maria,dc=tribus,dc=org`` al OpenLDAP con contraseña ``123456`` (más detalles ``tribus/config/data/users.ldif``)
* Agregar un usuario de pruebas ``uid=luis,dc=tribus,dc=org`` al OpenLDAP con contraseña ``654321`` (más detalles ``tribus/config/data/users.ldif``)
* Cambiar la contraseña del servidor PostgreSQL a ``tribus``.
* Crea una base de datos con nombre ``tribus`` (si ya existe una, la borra primero).
* Crea un usuario de nombre ``tribus`` con contraseña ``tribus`` y le concede todos los privilegios sobre la base de datos ``tribus`` (si ya existe uno, lo borra primero).
* Crea un virtualenv en una carpeta ``virtualenv/`` en el directorio raíz (no preocuparse por el versionamiento de esta carpeta porque ya está ignorada en el ``.gitignore``).
* Activa el virtualenv y ejecuta las siguientes acciones:

	* Instala las dependencias python listadas en ``tribus/config/data/python-dependencies.list`` con ``pip install -r``.
	* Sincroniza la base de datos de Django (``python manage.py syncdb``).
	* Hace la migración inicial de las tablas con South (``python manage.py migrate``).


Iniciando el servidor de desarrollo
-----------------------------------

::

	make runserver

Este comando es un atajo para hacer ``python manage.py runserver`` dentro del virtualenv.


Sincronizando la base de datos
------------------------------

::

	make syncdb

Este comando es un atajo para hacer ``python manage.py runserver`` y ``python manage.py migrate`` dentro del virtualenv.


Compilando las fuentes
----------------------


::

	make build

Tribus está almacenado en el repositorio de código fuente en forma de código fuente. Es decir, procuramos que no existan archivos compilados sino los archivos fuentes. Por ejemplo, para las imágenes no almacenamos archivos PNG o JPG sino SVG, para la documentación no almacenamos archivos PDF o HTML sino RST o para las traducciones no almacenamos archivos MO sino PO. Pero Tribus no utiliza los archivos fuentes sino sus archivos compilados. Es por eso que para poder utilizar tribus en un ambiente de producción, o incluso para algunas pruebas, es necesario compilar las fuentes.

Este comando es un comando que agrupa otro conjunto de comandos para cada tipo de archivo fuente.

::

	make build_html

Compila la documentación desde ReStructuredText a HTML utilizando `Sphinx <http://sphinx.pocoo.org>`_.

::

	make build_mo

Compila los archivos de traducción desde .po a .mo utilizando `Babel <http://babel.org>`_.

::

	make build_man

Compila archivos de ReStructuredText a archivos de manual leíbles con ``man`` utilizando `Docutils <http://docutils.org>`_.

::

	make build_img

Compila archivos SVG a PNG utilizando `CairoSVG <http://cairosvg.org>`_.


Limpiando las fuentes
---------------------


::

	make clean

Si deseamos limpiar las fuentes del producto de la compilación, por ejemplo, borrar todos los archivos PNG, MO, etc, entonces utilizamos ``make clean``.

Este comando es un comando que agrupa otro conjunto de comandos para cada tipo de archivo fuente.

::

	make clean_html

Borra la documentación generada con ``make build_html``.

::

	make clean_mo

Borra los archivos MO generados con ``make build_mo``.

::

	make clean_img

Borra los archivos PNG generados con ``make build_png``.

::

	make clean_man

Borra los archivos de manual generados con ``make build_man``.

::

	make clean_pyc

Borra los archivos precompilados de ejecución de python.

::

	make clean_dist

Borra los archivos generados por el proceso de empaquetado de python.


Generando paquetes python
-------------------------

::

	make sdist

Crea un paquete fuente python.


::

	make bdist

Crea un paquete python instalable.


Instalando en el sistema huésped desde el código fuente
-------------------------------------------------------

::

	make install

Instala la aplicación en modo de producción, al estilo python.
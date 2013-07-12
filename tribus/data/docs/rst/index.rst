======
Tribus
======


.. include:: readme.rst


Desarrollo
==========

Esta aplicación está en período de desarrollo, así que lo más probable es que **no funcione**. Aún no existe un método de instalación para medios en producción, así que si deseas usarla, la forma más rápida es que nos eches una mano.

Este proyecto está siendo desarrollado en Python, utilizando el framework de desarrollo web Django. Como podrás ver estamos utiliizando GitHub para gestionar las colaboraciones, así que para empezar, haz un fork de este repositorio y clonalo en tu pc o clona el repositorio principal::

	git clone https://github.com/HuntingBears/tribus

Tribus tiene un entorno de desarrollo python que ya hemos automatizado para ti. Cuando hayas clonado el repositorio, ejecuta la orden ``make development`` en la carpeta raíz para crear el entorno de desarrollo (se te pedirá tu clave de root para instalar paquetes y necesitarás una conexión a internet). Luego para correr el servidor de desarrollo haz ``make runserver`` y apunta tu navegador a la dirección ``127.0.0.1:8000`` para que veas como va Tribus (si es que funciona).

Existe un diagrama del diseño de la aplicación en docs/mindmap.svg (si prefieres ver un archivo png, está docs/mindmap.png pero debes hacer "make mindmap" primero). El diagrama puede servirte como guía de referencia para ver todos los componentes de la plataforma, pero no lo utilices para empezar a desarrollar.

Para empezar a trabajar en una tarea específica de Tribus, debes revisar los tickets para ver cuales son las tareas disponibles. Allí se encuentran las tareas completadas, las tareas en proceso y las tareas por hacer. Cada tarea está descrita de la forma más detallada posible, para tomar una tarea simplemente haz un comentario en el ticket diciendo que tomarás la tarea. Si necesitas mayor información pregunta mediante comentarios en el ticket.

Cuando termines una tarea, haz una solicitud de pull request desde tu fork hacia el repositorio principal para que pueda ser incorporado. Demás está decir que todos los colaboradores tendrán sus reconocimientos de autor en las partes que correspondan.

.. toctree::
    :hidden:

    contributing
    roadmap
    reusable
    authors


Instalación
===========

La instalación se hace a través del método tradicional de instalación con setuptools/distutils. El esquema d eempaquetamiento para Debian aún no está implementado por ser una aplicación en desarrollo.

Para instalar::

	python setup.py install

Para generar un tarball instalable::

	python setup.py bdist

Para generar un tarball del código fuente::

	python setup.py sdist


Contacto
========

Tribus tiene una lista de correo para desarrollo en tribus-dev@googlegroups.com, puedes suscribirte y comunicarte por esa vía.

.. include:: links.rst
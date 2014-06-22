======
Tribus
======

.. include:: readme.rst

Esta sección describe todos los procedimientos necesarios para entender cómo instalar y publicar una instancia funcional de Tribus, así como también personalizar la configuración dependiendo de las necesidades del usuario. No es necesario ser un operador de plataforma para instalar una instancia de Tribus, pero si debe estar familiarizado con los comandos básicos de consola bajo ambiente GNU/Linux.

.. _installation:

Instalación
===========

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



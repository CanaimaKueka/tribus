=================================================
Protocolo para la incorporación de contribuciones
=================================================


El equipo de desarrolladores de Tribus está conformado por :doc:`varias personas <../contributors>` que dedican sus destrezas a mejorar Tribus. Sin embargo, cualquier otra persona es bienvenida a colaborar a través del sistema de tickets y pull-requests, el IRC o las listas de correo.


Primeros Pasos
==============

Tribus tiene un documento llamado :doc:`hojas de ruta <roadmap>` (roadmap), el cual define cuales son las tareas que se deben ejecutar para terminar con el desarrollo de una determinada versión de Tribus. Si quisieras contribuir al desarrollo de Tribus, la recomendación sería empezar a buscar una tarea disponible en la hoja de ruta activa para momento. Generalmente la primera hoja de ruta que se lista en el documento es la hoja de ruta activa.

Probablemente existan otras cosas que necesitan mejorarse dentro de Tribus y que no están listadas dentro de la hoja de ruta activa. Cualquier otra contribución que esté fuera de la hoja de ruta será recibida y considerada igualmente, aunque dependiendo de la magnitud de los cambios realizados, es posible que la contribución sea incorporada en una próxima versión. Échale un ojo a la estructura del proyecto y examina en qué otras cosas deseas ayudarnos.

Obteniendo el código
--------------------

Los desarrolladores de Tribus gestionan el código fuente del proyecto a través de `Git <http://git-scm.com>`_. Para seguir de cerca el desarrollo de Tribus a través de Git, en vez de estar descargando archivos comprimidos, tienes las siguientes opciones:

* Clonar el repositorio principal directamente desde la `cuenta oficial de los desarrolladores de Tribus en GitHub <https://github.com/tribusdev/tribus>`_, ``git://github.com/tribusdev/tribus.git``

* Hacer tu propia derivación del repositorio de Tribus en GitHub, visitando `la página del repositorio <https://github.com/tribusdev/tribus>`_ y haciendo click en el botón "fork" (necesitas una cuenta activa en GitHub). 

Reproduciendo el entorno de desarrollo
--------------------------------------

Por favor consultar :ref:`make_environment`.

Ramas y flujo de trabajo en el repositorio
==========================================

Si bien la metodología de desarrollo de Tribus aún no está escrita en piedra, esta sección describe la manera actual de organizar las ramas y el flujo de desarrollo dentro del repositorio. Esta información **debe ser tomada en cuenta** a la hora de enviar nuevas contribuciones.

* Las nuevas funcionalidades pueden provenir de la hoja de ruta activa, en donde se listan los tickets asignados correspondientes a cada nueva funcionalidad. También puede proponer nuevas funcionalidades realizando un pull-request.

* Las nuevas funcionalidades se realizan en ramas temporales, que por convención se deben llamar ``<número de ticket>-<descripción-corta>``. Por ejemplo, si usted es un colaborador que desea atender el ticket #23 que se trata acerca indexar los paquetes en la base de datos, ustede debe hacer una nueva rama a partir de la rama ``development`` y nombrarla ``23-indexar-paquetes-bd`` (o algo parecido) -- esto puede hacerse con el comando ``git branch 23-indexar-paquetes-bd development``.

	* Estas ramas no deben ser utilizadas por el público. Además, por su carácter temporal pueden aparecer y desaparecer conforme va avanzando el proceso de desarrollo.

* Las nuevas funcionalidades son incorporadas en la rama de desarrollo ``development`` cuando se acerca la fecha del lanzamiento de versiones alpha o *snapshots*. Para este momento debe publicarse el archivo comprimido de la versión alpha y marcar el último commit del snapshot con la etiqueta correspondiente a la versión (``git tag X.Y.Zdev1234567890``). Este trabajo es realizado por alguno de los mantenedores de Tribus.

* Los desarrolladores que están trabajando en ramas de funcionalidades, deberían hacer *merge* de la rama ``development`` periódicamente para que obtengan los últimos cambios de los otros desarrolladores. Hacer esto evitará problemas de conflictos en Git. También es recomendable hacer push a sus copias del repositorio de forma periódica para que los que están siguiendo el desarrollo de una funcionalidad en particular puedan estar actualizados.

* El lanzamiento de una versión estable ocurre cuando todas las funcionalidades de la hoja de ruta activa han sido completadas.

* Si bien intentamos no hacer commit de código roto en la rama ``development``, como en cualquier otro proyecto de código abierto sólo garantizamos que habrá código estable en la rama ``master`` o ``release``. Sólo sigue la rama ``development`` si eres un nuevo desarrollador, quieres seguir de cerca las nuevas funcionalidades y/o estás dispuesto a soportar una que otra sorpresa desagradable.
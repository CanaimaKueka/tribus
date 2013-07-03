=====================
Canaima Desarrollador
=====================

**Un conjunto de herramientas para la eliminación de las barreras tecnológicas**

Canaima Desarrollador (C-D) es un compendio de herramientas y ayudantes que facilitan el proceso de desarrollo de software para Canaima GNU/Linux. Está diseñado para *facilitar el trabajo* a aquellas personas que participan en dicho proceso con regularidad, como también para *iniciar a los que deseen aprender* de una manera rápida y práctica.

C-D sigue dos líneas de acción principales para lograr éste cometido: *la práctica* y *la formativa*. La práctica permite:

- Agilizar los procesos para la creación de paquetes binarios canaima a partir de paquetes fuentes correctamente estructurados.
- Automatización personalizada de la creación de Paquetes Fuentes acordes a las Políticas de Canaima GNU/Linux.
- Creación de un depósito personal, por usuario, donde se guardan automáticamente y en carpetas separadas los siguientes tipos de archivo:
  - Proyectos en proceso de empaquetamiento
  - Paquetes Binarios (*.deb)
  - Paquetes Fuente (*.tar.gz, *.dsc, *.changes, *.diff)
  - Registros provenientes de la creación de paquetes binarios (*.build)
- Versionamiento asistido (basado en git) en los proyectos, brindando herramientas para realizar las siguientes operaciones, con un alto nivel de automatización y detección de posibles errores:
  - git clone
  - git commit
  - git push
  - git pull
- Ejecución de tareas en masa (empaquetar, hacer pull, push, commit, entre otros), para agilizar procesos repetitivos.

En el otro aspecto, el formativo, C-D incluye:

- El Manual del Desarrollador, resumen técnico-práctico de las herramientas cognitivas necesarias para desarrollar paquetes funcionales para Canaima GNU/Linux.
- La Guía de Referencia para el Desarrollador, compendio extenso y detallado que extiende y complementa el contenido del Manual del Desarrollador.
- Éste manual para el uso de Canaima Desarrollador.

----------------------

**Índice de Contenidos**

.. toctree::
   :maxdepth: 2

   man-canaima-desarrollador.rst
   manual-desarrollador.rst
   guia-referencia.rst

----------------------

:)

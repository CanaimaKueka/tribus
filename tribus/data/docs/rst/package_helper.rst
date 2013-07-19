tbs package create
==================

Comportamiento automático
-------------------------

1.- Identificar el tipo de sistema de versionamiento (git, subversion, bazaar, mercurial, ninguno).
2.- Identificar el tipo de paquete fuente (nativo, quilt, etc).
3.- Desaplicar todos los parches.
4.- Verificar si existen nuevos cambios no versionados.
	Pistas:
	- Si existen cambios sólamente dentro de la carpeta debian/, entonces tenemos una revisión nueva.
	- Si existen cambios sólamente fuera de la carpeta debian/, entonces:
		- Tenemos un nuevo import desde upstream, por lo tanto tenemos una versión nueva.
			- Debe existir una etiqueta para el import desde upstream.
		- El mantenedor se equivocó e hizo cambios directamente sobre el código fuente del software.
	- Si existen cambios en la carpeta debian/ y fuera de ella, entonces:
		- El mantenedor se equivocó e hizo cambios directamente sobre el código fuente del software y además hizo cambios en la carpeta debian/.
		- El mantenedor importó una nueva versión desde upstream pero olvidó hacer commit e hizo cambios en la carpeta debian seguidamente.
	- Si no existen cambios, estamos haciendo un reempaquetamiento de una versión previa.
		- Debe existir una etiqueta para la versión empaquetada.
		- La versión es la misma, no debe haber ningún cambio en el paquete (empaquetamiento no-intrusivo).
5.- Identificar el tipo de empaquetado (--test, --final).
6.- Relacionar la versión anterior con un commit (a través de la etiqueta).
7.- Recolectar todos los commits realizados hasta la fecha.
8.- Crear la nueva entrada de Changelog.
	- Insertar todos los mensajes de commit desde la última versión.
		- Si no tenemos sistema de versionamiento, dejar el editor abierto para introducir manualmente los mensajes de changelog.
	- Determinar la nueva versión, prioridad y distribución destino.
	- Determinar autor y correo correctos del paquete.
9.- Recrear el paquete fuente en el formato correcto.
10.- Empaquetar.
11.- Firmar fuentes si tenemos llave gpg.
12.- Hacer etiqueta si era un empaquetado --final.
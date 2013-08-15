====================================
Normas de estilo para contribuciones
====================================

Tribus hace un esfuerzo por seguir el estándar `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_, especialmente en los siguientes puntos:

* Mantener el largo de las líneas por debajo de 80 caracteres, tanto para el código como para la documentación.
	
	* Se aceptan excepciones cuando se hace imposible cortar la línea sin romper la funcionalidad o cuando se hace necesario reescribir código sólamente para cumplir con esta regla.

* La sangría debe ser de 4 espacios. Nada de 8 espacios, 2 espacios, 3 espacios o tabulaciones.

* Nombres de clases en estilo ``CamelCase`` y ``minúsculas_separadas_por_guiones_bajos`` para métodos, funciones, atributos y todo lo demás.

Por otro lado, se hacen otras sugerencias específicas:

* En cualquier uso de parámetros, debe especificarse el nombre del mismo en conjunto con su valor. Por ejemplo, esto está bien: ``self.funcion(parametro_1='Valor 1', parametro_2='Valor 2')`` y esto está mal ``self.funcion('Valor 1', 'Valor 2')``.

* Se prefiere nombre de clases, funciones, atributos y métodos en inglés.

* Toda función o clase debe estar documentada de la forma en que autodoc de Sphinx la interpreta. La documentación debe estar en inglés.

* Toda configuración debe ser incluída dentro del paquete tribus.config y referenciada desde donde se necesita.

* Toda función o clase de bajo nivel, o constructora de otras funciones más complejas debe ser incluída dentro del paquete tribus.common y referenciada desde donde se necesita.

* Toda ilustración o imagen a incluir dentro de Tribus debe estar en formato SVG. Si usted desea incluir un archivo de imagen png o jpg que no puede ser vectorizado limpiamente, incrustelo primero en un svg.

* Si está haciendo una vista para tribus.web, no escriba elementos css nuevos sin antes revisar si existe algún elemento con las características que usted necesita.

* Se prefiere el uso de comillas simples para declarar cadenas de texto.
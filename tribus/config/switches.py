# En este archivo deben ir las configuraciones globales de switches
# flags y otros elementos de waffle

# Por cada switch es necesario agregar los siguientes datos:
# - Nombre simple
# - Nombre legible para humanos
# - Estado por defecto del switch

SWITCHES_CONFIGURATION = {
    'cloud': ('Package cloud', "on"),
    'profile': ('User profiles', "on"),
    'admin_first_time': ("Admin's first time configuration", "off")
}

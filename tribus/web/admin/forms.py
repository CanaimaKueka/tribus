from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.forms.util import flatatt
from fabric.api import local, env, settings, cd, lcd
from tribus import BASEDIR
from tribus.web.cloud.tasks import update_switches

switch_names = {
    'cloud':'Package cloud',
    'profile': 'User profiles',
    'admin_first_time': "Admin's first time configuration" 
}

# Esto no va aqui, poner en otro archivo
class AceCheckboxInput(forms.CheckboxInput):
    """
    Documentar para que estoy creando este tipo de widget
    """
    
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        if self.check_test(value):
            final_attrs['checked'] = 'checked'
        if not (value is True or value is False or value is None or value == ''):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        return format_html('<input{0} /><span class="lbl"></span>', flatatt(final_attrs))


class ActiveModulesForm(forms.Form):
    '''
    Documentar lo que se hace aqui y para que
    '''
    
    def __init__(self, *args, **kwargs):
        super(ActiveModulesForm, self).__init__(args, kwargs)
        request = args[0]
        if request.method == "GET":
            for k, v in args[1]:
                if k not in self.fields.keys():
                    if v.active:
                        self.fields[v.name] = forms.BooleanField(widget=AceCheckboxInput(attrs={'class':'ace ace-switch ace-switch-4 btn-flat',
                                                                                                'checked':'checked'},
                                                                                         ), label = k, required=False)
                        #self.fields[v.name] = forms.BooleanField(label = k, required = False)
                    else:
                        self.fields[v.name] = forms.BooleanField(widget=AceCheckboxInput(attrs={'class':'ace ace-switch ace-switch-4 btn-flat'}),
                                                                 label = k, required=False)
                        #self.fields[v.name] = forms.BooleanField(label = k, required = False)

        elif request.method == "POST":
#             for switch_name in switch_names.keys():
#                 if switch_name in request.POST:
#                     # Si esta presente en el POST es porque tiene un valor 
#                     # distinto al valor original, el cambio solo se hace dentro de este if
#                     print "SWITCH %s: %s" % (switch_name, request.POST.get(switch_name))
#                     with cd('%s' % BASEDIR):
#                         local('python manage.py switch %s on --create' % switch_name)
#                 else:
#                     print "SWITCH %s: off" % (switch_name)
#                     with cd('%s' % BASEDIR):
#                         local('python manage.py switch %s off --create' % switch_name)
            print "AQUI DEBERIA AGREGAR EL TASK"
            #update_switches.apply_async(queue='default')
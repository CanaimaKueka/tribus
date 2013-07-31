from babel.messages.frontend import (extract_messages as base_extract_messages,
									 init_catalog as base_init_catalog,
									 update_catalog as base_update_catalog)


class extract_messages(base_extract_messages):
    def run(self):
    	base_extract_messages.run(self)
    	# for lang in languages:
    	# 	srcdir = 'tribus/data/docs/rst'
    	# 	confdir = srcdir
    	# 	outdir = 'tribus/data/docs/html/'+lang
    	# 	buildername = 'gettext'
	    #     app = Sphinx(srcdir=, confdir=, outdir=, doctreedir=, buildername='gettext',
     #             confoverrides=None, status=sys.stdout, warning=sys.stderr,
     #             freshenv=False, warningiserror=False, tags=None)


class init_catalog(base_init_catalog):
    def run(self):
    	base_init_catalog.run(self)


class update_catalog(base_update_catalog):
    def run(self):
    	base_update_catalog.run(self)

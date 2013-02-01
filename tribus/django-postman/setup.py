from setuptools import setup, find_packages

setup(
    name='django-postman',
    version=__import__('postman').__version__,
    description='User-to-User messaging system for Django, with gateway to AnonymousUser,' \
        ' moderation and thread management, user & exchange filters, inbox/sent/archives/trash folders,' \
        ' support for apps: auto-complete, notification, mailer.',
    long_description=open('docs/index.rst').read().split('\n----\n', 1)[0],
    author='Patrick Samson',
    author_email='maxcom@laposte.net',
    url='http://bitbucket.org/psam/django-postman/overview',
    license='BSD',
    packages=find_packages(exclude=('docs',)),
    include_package_data=True,
    keywords='django messages messaging email moderation',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
    install_requires=[
        'Django',
    ],
)


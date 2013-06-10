from setuptools import setup

setup(
    name="tribus",
    version="0.1",
    author="Luis Alejandro Martínez Faneyth",
    author_email="luis@huntingbears.com.ve",
    description=("Red social para la gestión de comunidades de software libre"),
    license="GPL",
    keywords="git buildbot django",
    url="TODO",
    packages=['tribus'],
    install_requires=[
        'django',
        'django-auth-ldap',
        'redis',
        'hiredis',
    ],
    long_description='TODO',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

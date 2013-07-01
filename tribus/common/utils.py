#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def get_path(p=[]):
    p[0] = os.path.realpath(p[0])
    return os.path.normpath(os.path.join(*p))

def get_split_path(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join)
    in a platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return get_split_path(head, [tail] + result)


def get_packages(path, excludes=[], packages=[]):
    if os.path.isfile(get_path([path, '__init__.py'])):
        strippath=get_path([path, '..'])
        print strippath
    else:
        strippath=path
    for dirpath, dirnames, filenames in os.walk(path):
        if '__init__.py' in filenames:
            if dirpath.startswith(strippath):
                dirpath = dirpath[len(strippath):]
            package_name = '.'.join(get_split_path(dirpath))
            packages.append(package_name)
            for e in excludes:
                if package_name.startswith(e):
                    packages.remove(package_name)
    return packages


def get_packages_data(path, packages=[], package_data={}):
    for dirpath, dirnames, filenames in os.walk(path):
        parts = get_split_path(dirpath)
        package_name = '.'.join(parts)
        if '__init__.py' in filenames:
            packages.append(package_name)
        elif filenames:
            relative_path = []
            while '.'.join(parts) not in packages:
                relative_path.append(parts.pop())
            relative_path.reverse()
            path = os.path.join(*relative_path)
            package_files = package_data.setdefault('.'.join(parts), [])
            package_files.extend([os.path.join(path, f) for f in filenames])
    return package_files, package_data, packages


def get_data_files(path, dest, pattern):
    """
    Generate a pair of (directory, file-list) for installation.

    'd' -- A directory
    'e' -- A glob pattern
    """
    return (dest, [f for f in glob.glob('%s/%s' % (path, pattern)) if os.path.isfile(f)])

# def filter_names(names, excludes=[]):
#     """
#     Given a list of file names, return those names that should be copied.
#     """
#     names = [n for n in names if n not in excludes]
#     # This is needed when building a distro from a working
#     # copy (likely a checkout) rather than a pristine export:
#     for pattern in excludes:
#         names = [n for n in names
#                  if (not fnmatch.fnmatch(n, pattern))
#                  and (not n.endswith('.py'))]
#     return names



# def getDataFiles(dname, ignore=None, parent=None):
#     """
#     Get all the data files that should be included in this distutils Project.

#     'dname' should be the path to the package that you're distributing.

#     'ignore' is a list of sub-packages to ignore.  This facilitates
#     disparate package hierarchies.  That's a fancy way of saying that
#     the 'twisted' package doesn't want to include the 'twisted.conch'
#     package, so it will pass ['conch'] as the value.

#     'parent' is necessary if you're distributing a subpackage like
#     twisted.conch.  'dname' should point to 'twisted/conch' and 'parent'
#     should point to 'twisted'.  This ensures that your data_files are
#     generated correctly, only using relative paths for the first element
#     of the tuple ('twisted/conch/*').
#     The default 'parent' is the current working directory.
#     """
#     parent = parent or "."
#     ignore = ignore or []
#     result = []
#     for directory, subdirectories, filenames in os.walk(dname):
#         resultfiles = []
#         for exname in EXCLUDE_NAMES:
#             if exname in subdirectories:
#                 subdirectories.remove(exname)
#         for ig in ignore:
#             if ig in subdirectories:
#                 subdirectories.remove(ig)
#         for filename in _filterNames(filenames):
#             resultfiles.append(filename)
#         if resultfiles:
#             result.append((relativeTo(parent, directory),
#                            [relativeTo(parent,
#                                        os.path.join(directory, filename))
#                             for filename in resultfiles]))
#     return result

# def get_packages_list(dname, pkgname=None, results=None, ignore=None, parent=None):
#     """
#     Get all packages which are under dname. This is necessary for
#     Python 2.2's distutils.

#     'dname' should be the path to the package that you're distributing.

#     'ignore' is a list of sub-packages to ignore.  This facilitates
#     disparate package hierarchies.  That's a fancy way of saying that
#     the 'twisted' package doesn't want to include the 'twisted.conch'
#     package, so it will pass ['conch'] as the value.

#     'parent' is necessary if you're distributing a subpackage like
#     twisted.conch.  'dname' should point to 'twisted/conch' and 'parent'
#     should point to 'twisted'.  This ensures that your data_files are
#     generated correctly, only using relative paths for the first element
#     of the tuple ('twisted/conch/*').
#     The default 'parent' is the current working directory.
#     """
#     parent = parent or ""
#     prefix = []
#     if parent:
#         prefix = [parent]
#     bname = os.path.basename(dname)
#     ignore = ignore or []
#     if bname in ignore:
#         return []
#     if results is None:
#         results = []
#     if pkgname is None:
#         pkgname = []
#     subfiles = os.listdir(dname)
#     abssubfiles = [os.path.join(dname, x) for x in subfiles]
#     if '__init__.py' in subfiles:
#         results.append(prefix + pkgname + [bname])
#         for subdir in filter(os.path.isdir, abssubfiles):
#             get_packages_list(subdir, pkgname=pkgname + [bname],
#                         results=results, ignore=ignore,
#                         parent=parent)
#     res = ['.'.join(result) for result in results]
#     return res

# def getAllScripts():
#     # "" is included because core scripts are directly in bin/
#     projects = [''] + [x for x in os.listdir('bin')
#                        if os.path.isdir(os.path.join("bin", x))
#                        and x in twisted_subprojects]
#     scripts = []
#     for i in projects:
#         scripts.extend(getScripts(i))
#     return scripts

if __name__ == '__main__':
    p = get_packages(
        excludes=['tools', 'tests'],
        path='/home/canaima/desarrollo/tribus/tribus'
        )
    print p
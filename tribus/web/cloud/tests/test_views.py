#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

These are the tests for the tribus.web.cloud views.

"""

# from django.test.testcases import TestCase
# from django.core.urlresolvers import reverse
# from tribus.web.cloud.models import Package, Details, Relation


# class CloudViews(TestCase):

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def test_cloud_frontpage(self):
#         resp = self.client.get(reverse('tribus.web.cloud.views.frontpage'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertTrue('render_js' in resp.context)

#     def test_cloud_package_list(self):
#         # p = Package.objects.get_or_create(Package="blender")
#         # call_command('clear_index')
#         # call_command('update_index')
#         # No logro reconstruir los indices de busqueda en el entorno de
#         # pruebas

#         resp = self.client.get(reverse('tribus.web.cloud.views.package_list'))
#         self.assertEqual(resp.status_code, 200)
#         self.assertTrue('render_js' in resp.context)

#         # EN ESTE TEST SE DEBE PROBAR:
#         # - Si los elementos creados para el test se encuentran en el
#         #   contexto de la vista
#         # - Que muestre una pagina distinta si no hay paquetes indexados
#         # - Si hay varias paginas de resultados verificar que
#         #   los enlaces a esas paginas dan 200
#         # - Al buscar una pagina que no esta en las paginas de
#         #   resultados disponibles debe direccionar a una pagina
#         #   que indique que no hay resultados
#         # - Como se manejan los filtros aplicados para buscar en
#         #   la lista de paquetes

#     def test_cloud_profile(self):

#         package = {
#             'Name': 'blender',
#             'Description': 'Software de modelado 3d',
#             'Homepage': 'http://blender.org/',
#             'Section': 'graphics', 'Priority': 'optional',
#             'Bugs': 'http://bugs.debian.org/blender'
#         }

#         details_i386 = {
#             'Version': '2.63a-1',
#             'Architecture': 'i386',
#             'Size': '21957',
#             'InstalledSize': '55328',
#             'MD5sum': '3917d6227e61324a29459303c0531587',
#             'Filename': 'pool/main/b/blender/blender_2.63a-1_i386.deb',
#             'Distribution': 'kukenan'
#         }

#         details_amd64 = {
#             'Version': '2.63a-1',
#             'Architecture': 'amd64',
#             'Size': '21886',
#             'InstalledSize': '57306',
#             'MD5sum': 'c764e1a86b0bc3c43d1d749de68b1ef7',
#             'Filename': 'pool/main/b/blender/blender_2.63a-1_amd64.deb',
#             'Distribution': 'kukenan'
#         }

#         rel_fields = ['related_package',
#                       'order',
#                       'version',
#                       'alt_id',
#                       'relation_type']

#         rel_i386 = {
#             'python3.2': {
#                 'related_package': Package.objects.create(Name='python3.2'),
#                 'order': None,
#                 'version': None,
#                 'alt_id': 0,
#                 'relation_type': 'depends'
#             },
#             'libstdc++6': {
#                 'related_package': Package.objects.create(Name='libstdc++6'),
#                 'order': '>=',
#                 'version': '4.6',
#                 'alt_id': 0,
#                 'relation_type': 'depends'
#             },
#             'libavcodec53': {
#                 'related_package': Package.objects.create(Name='libavcodec53'),
#                 'order': '>=',
#                 'version': '5:0.8-2~',
#                 'alt_id': 1,
#                 'relation_type': 'depends'
#             },
#             'libavcodec-extra-53': {
#                 'related_package': Package.objects.create(Name='libavcodec-extra-53'),
#                 'order': '>=',
#                 'version': '5:0.8-2~',
#                 'alt_id': 1,
#                 'relation_type': 'depends'
#             },
#             'libglu1-mesa': {
#                 'related_package': Package.objects.create(Name='libglu1-mesa'),
#                 'order': None,
#                 'version': None,
#                 'alt_id': 2,
#                 'relation_type': 'depends'
#             },
#             'libglu1': {
#                 'related_package': Package.objects.create(Name='libglu1'),
#                 'order': None,
#                 'version': None,
#                 'alt_id': 2,
#                 'relation_type': 'depends'
#             }
#         }

#         rel_amd64 = {
#             'libc6': {
#                 'related_package': Package.objects.create(Name='libc6'),
#                 'order': '>=',
#                 'version': '2.7',
#                 'alt_id': 0,
#                 'relation_type': 'depends'
#             },
#             'libfftw3-3': {
#                 'related_package': Package.objects.create(Name='libfftw3-3'),
#                 'order': None,
#                 'version': None,
#                 'alt_id': 0,
#                 'relation_type': 'depends'
#             },
#             'libgl1-mesa-glx': {
#                 'related_package': Package.objects.create(Name='libgl1-mesa-glx'),
#                 'order': None,
#                 'version': None,
#                 'alt_id': 1,
#                 'relation_type': 'depends'
#             },
#             'libgl1': {
#                 'related_package': Package.objects.create(Name='libgl1'),
#                 'order': None,
#                 'version': None,
#                 'alt_id': 1,
#                 'relation_type': 'depends'
#             },
#             'libglu1-mesa': {
#                 'related_package': Package.objects.create(Name='libglu1-mesa'),
#                 'order': None,
#                 'version': None,
#                 'alt_id': 2,
#                 'relation_type': 'depends'
#             },
#             'libglu1': {
#                 'related_package': Package.objects.create(Name='libglu1'),
#                 'order': None,
#                 'version': None,
#                 'alt_id': 2,
#                 'relation_type': 'depends'
#             }
#         }

#         p, _ = Package.objects.get_or_create(**package)
#         d1, _ = Details.objects.get_or_create(**details_i386)
#         d2, _ = Details.objects.get_or_create(**details_amd64)

#         p.Details.add(d1)
#         p.Details.add(d2)

#         for relation in rel_i386.values():
#             r, _ = Relation.objects.get_or_create(**relation)
#             d1.Relations.add(r)

#         for relation in rel_amd64.values():
#             r, _ = Relation.objects.get_or_create(**relation)
#             d2.Relations.add(r)

#         resp1 = self.client.get(reverse('tribus.web.cloud.views.profile',
#                                         kwargs={'name': 'adobe-photoshop'}))
#         resp2 = self.client.get(reverse('tribus.web.cloud.views.profile',
#                                         kwargs={'name': 'blender'}))

#         self.assertEqual(resp1.status_code, 404)
#         self.assertEqual(resp2.status_code, 200)
#         self.assertTrue('render_js' in resp2.context)

#         for k, v in package.items():
#             self.assertEqual(
#                 str(getattr(resp2.context[0].get('paquete'), k)), v)

#         resp_details = resp2.context[0].get('detalles')[0].get('Architectures')

#         for k, v in details_i386.items():
#             self.assertEqual(
#                 str(getattr(resp_details.get('i386').get('data'), k)), v)

#         for k, v in details_amd64.items():
#             self.assertEqual(
#                 str(getattr(resp_details.get('amd64').get('data'), k)), v)

#         for rel in resp_details.get('i386').get('relations').get('depends'):
#             for field in rel_fields:
#                 self.assertEqual(
#                     str(getattr(rel, field)),
#                     str(rel_i386.get(rel.related_package.Name).get(field)))

#         for rel in resp_details.get('amd64').get('relations').get('depends'):
#             for field in rel_fields:
#                 self.assertEqual(
#                     str(getattr(rel, field)),
#                     str(rel_amd64.get(rel.related_package.Name).get(field)))

# import os
# import hashlib
# import inspect
# import shutil
# import stat
# import zipfile

# from juju.lib import serializer
# from juju.lib.testing import TestCase
# from juju.lib.filehash import compute_file_hash
# from juju.charm.metadata import MetaData
# from juju.charm.bundle import CharmBundle
# from juju.errors import CharmError
# from juju.charm.directory import CharmDirectory
# from juju.charm.provider import get_charm_from_path

# from juju.charm import tests

# repository_directory = os.path.join(
#     os.path.dirname(inspect.getabsfile(tests)), "repository")

# sample_directory = os.path.join(repository_directory, "series", "dummy")


# class BundleTest(TestCase):

#     def setUp(self):
#         directory = CharmDirectory(sample_directory)

#         # add sample directory
#         self.filename = self.makeFile(suffix=".charm")
#         directory.make_archive(self.filename)

#     def copy_charm(self):
#         dir_ = os.path.join(self.makeDir(), "sample")
#         shutil.copytree(sample_directory, dir_)
#         return dir_

#     def test_initialization(self):
#         bundle = CharmBundle(self.filename)
#         self.assertEquals(bundle.path, self.filename)

#     def test_error_not_zip(self):
#         filename = self.makeFile("@#$@$")
#         err = self.assertRaises(CharmError, CharmBundle, filename)
#         self.assertEquals(
#             str(err),
#             "Error processing %r: must be a zip file (File is not a zip file)"
#             % filename)

#     def test_error_zip_but_doesnt_have_metadata_file(self):
#         filename = self.makeFile()
#         zf = zipfile.ZipFile(filename, 'w')
#         zf.writestr("README.txt", "This is not a valid charm.")
#         zf.close()

#         err = self.assertRaises(CharmError, CharmBundle, filename)
#         self.assertEquals(
#             str(err),
#             "Error processing %r: charm does not contain required "
#             "file 'metadata.yaml'" % filename)

#     def test_no_revision_at_all(self):
#         filename = self.makeFile()
#         zf_dst = zipfile.ZipFile(filename, "w")
#         zf_src = zipfile.ZipFile(self.filename, "r")
#         for name in zf_src.namelist():
#             if name == "revision":
#                 continue
#             zf_dst.writestr(name, zf_src.read(name))
#         zf_src.close()
#         zf_dst.close()

#         err = self.assertRaises(CharmError, CharmBundle, filename)
#         self.assertEquals(
#             str(err), "Error processing %r: has no revision" % filename)

#     def test_revision_in_metadata(self):
#         filename = self.makeFile()
#         zf_dst = zipfile.ZipFile(filename, "w")
#         zf_src = zipfile.ZipFile(self.filename, "r")
#         for name in zf_src.namelist():
#             if name == "revision":
#                 continue
#             content = zf_src.read(name)
#             if name == "metadata.yaml":
#                 data = serializer.yaml_load(content)
#                 data["revision"] = 303
#                 content = serializer.yaml_dump(data)
#             zf_dst.writestr(name, content)
#         zf_src.close()
#         zf_dst.close()

#         charm = CharmBundle(filename)
#         self.assertEquals(charm.get_revision(), 303)

#     def test_competing_revisions(self):
#         zf = zipfile.ZipFile(self.filename, "a")
#         zf.writestr("revision", "999")
#         data = serializer.yaml_load(zf.read("metadata.yaml"))
#         data["revision"] = 303
#         zf.writestr("metadata.yaml", serializer.yaml_dump(data))
#         zf.close()

#         charm = CharmBundle(self.filename)
#         self.assertEquals(charm.get_revision(), 999)

#     def test_cannot_set_revision(self):
#         charm = CharmBundle(self.filename)
#         self.assertRaises(NotImplementedError, charm.set_revision, 123)

#     def test_bundled_config(self):
#         """Make sure that config is accessible from a bundle."""
#         from juju.charm.tests.test_config import sample_yaml_data
#         bundle = CharmBundle(self.filename)
#         self.assertEquals(bundle.config.get_serialization_data(),
#                           sample_yaml_data)

#     def test_info(self):
#         bundle = CharmBundle(self.filename)
#         self.assertTrue(bundle.metadata is not None)
#         self.assertTrue(isinstance(bundle.metadata, MetaData))
#         self.assertEquals(bundle.metadata.name, "dummy")
#         self.assertEqual(bundle.type, "bundle")

#     def test_as_bundle(self):
#         bundle = CharmBundle(self.filename)
#         self.assertEquals(bundle.as_bundle(), bundle)

#     def test_executable_extraction(self):
#         sample_directory = os.path.join(
#             repository_directory, "series", "varnish-alternative")
#         charm_directory = CharmDirectory(sample_directory)
#         source_hook_path = os.path.join(sample_directory, "hooks", "install")
#         self.assertTrue(os.access(source_hook_path, os.X_OK))
#         bundle = charm_directory.as_bundle()
#         directory = bundle.as_directory()
#         hook_path = os.path.join(directory.path, "hooks", "install")
#         self.assertTrue(os.access(hook_path, os.X_OK))
#         config_path = os.path.join(directory.path, "config.yaml")
#         self.assertFalse(os.access(config_path, os.X_OK))

#     def get_charm_sha256(self):
#         return compute_file_hash(hashlib.sha256, self.filename)

#     def test_compute_sha256(self):
#         sha256 = self.get_charm_sha256()
#         bundle = CharmBundle(self.filename)
#         self.assertEquals(bundle.compute_sha256(), sha256)

#     def test_charm_base_inheritance(self):
#         """
#         get_sha256() should be implemented in the base class,
#         and should use compute_sha256 to calculate the digest.
#         """
#         sha256 = self.get_charm_sha256()
#         bundle = CharmBundle(self.filename)
#         self.assertEquals(bundle.get_sha256(), sha256)

#     def test_file_handle_as_path(self):
#         sha256 = self.get_charm_sha256()
#         fh = open(self.filename)
#         bundle = CharmBundle(fh)
#         self.assertEquals(bundle.get_sha256(), sha256)

#     def test_extract_to(self):
#         filename = self.makeFile()
#         charm = get_charm_from_path(self.filename)
#         f2 = charm.extract_to(filename)

#         # f2 should be a charm directory
#         self.assertInstance(f2, CharmDirectory)
#         self.assertInstance(f2.get_sha256(), basestring)
#         self.assertEqual(f2.path, filename)

#     def test_extract_symlink(self):
#         extract_dir = self.makeDir()
#         charm_path = self.copy_charm()
#         sym_path = os.path.join(charm_path, 'foobar')
#         os.symlink('metadata.yaml', sym_path)

#         charm_dir = CharmDirectory(charm_path)
#         bundle = charm_dir.as_bundle()
#         bundle.extract_to(extract_dir)
#         self.assertIn("foobar", os.listdir(extract_dir))
#         self.assertTrue(os.path.islink(os.path.join(extract_dir, "foobar")))
#         self.assertEqual(os.readlink(os.path.join(extract_dir, 'foobar')),
#                         'metadata.yaml')

#         # Verify we can extract it over again
#         os.remove(sym_path)
#         os.symlink('./config.yaml', sym_path)
#         charm_dir = CharmDirectory(charm_path)
#         bundle = charm_dir.as_bundle()
#         bundle.extract_to(extract_dir)
#         self.assertEqual(os.readlink(os.path.join(extract_dir, 'foobar')),
#                         './config.yaml')

#     def test_extract_symlink_mode(self):
#         # lp:973260 - charms packed by different tools that record symlink
#         # mode permissions differently (ie the charm store) don't extract
#         # correctly.
#         charm_path = self.copy_charm()
#         sym_path = os.path.join(charm_path, 'foobar')
#         os.symlink('metadata.yaml', sym_path)
#         charm_dir = CharmDirectory(charm_path)
#         normal_path = charm_dir.as_bundle().path
#         zf_src = zipfile.ZipFile(normal_path, "r")
#         foreign_path = os.path.join(self.makeDir(), "store.charm")
#         zf_dst = zipfile.ZipFile(foreign_path, "w")
#         for info in zf_src.infolist():
#             if info.filename == "foobar":
#                 # This is what the charm store does:
#                 info.external_attr = (stat.S_IFLNK | 0777) << 16
#             zf_dst.writestr(info, zf_src.read(info.filename))
#         zf_src.close()
#         zf_dst.close()

#         bundle = CharmBundle(foreign_path)
#         extract_dir = self.makeDir()
#         bundle.extract_to(extract_dir)
#         self.assertIn("foobar", os.listdir(extract_dir))
#         self.assertTrue(os.path.islink(os.path.join(extract_dir, "foobar")))
#         self.assertEqual(os.readlink(os.path.join(extract_dir, 'foobar')),
#                         'metadata.yaml')

#     def test_as_directory(self):
#         filename = self.makeFile()
#         charm = get_charm_from_path(self.filename)
#         f2 = charm.as_directory()

#         # f2 should be a charm directory
#         self.assertInstance(f2, CharmDirectory)
#         self.assertInstance(f2.get_sha256(), basestring)
#         # verify that it was extracted to a new temp dirname
#         self.assertNotEqual(f2.path, filename)

#         fn = os.path.split(f2.path)[1]
#         # verify that it used the expected prefix
#         self.assertStartsWith(fn, "tmp")

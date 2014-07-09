# import gc
# import os
# import hashlib
# import inspect
# import shutil
# import zipfile

# from juju.errors import CharmError, FileNotFound
# from juju.charm.errors import InvalidCharmFile
# from juju.charm.metadata import MetaData
# from juju.charm.directory import CharmDirectory
# from juju.charm.bundle import CharmBundle
# from juju.lib import serializer
# from juju.lib.filehash import compute_file_hash
# from juju.charm import tests

# from juju.charm.tests.test_repository import RepositoryTestBase


# sample_directory = os.path.join(
#     os.path.dirname(
#         inspect.getabsfile(tests)), "repository", "series", "dummy")


# class DirectoryTest(RepositoryTestBase):

#     def setUp(self):
#         super(DirectoryTest, self).setUp()

#         # Ensure the empty/ directory exists under the dummy sample
#         # charm.  Depending on how the source code is exported,
#         # empty directories may be ignored.
#         empty_dir = os.path.join(sample_directory, "empty")
#         if not os.path.isdir(empty_dir):
#             os.mkdir(empty_dir)

#     def copy_charm(self):
#         dir_ = os.path.join(self.makeDir(), "sample")
#         shutil.copytree(sample_directory, dir_)
#         return dir_

#     def delete_revision(self, dir_):
#         os.remove(os.path.join(dir_, "revision"))

#     def set_metadata_revision(self, dir_, revision):
#         metadata_path = os.path.join(dir_, "metadata.yaml")
#         with open(metadata_path) as f:
#             data = serializer.yaml_load(f.read())
#         data["revision"] = 999
#         with open(metadata_path, "w") as f:
#             f.write(serializer.yaml_dump(data))

#     def test_metadata_is_required(self):
#         directory = self.makeDir()
#         self.assertRaises(FileNotFound, CharmDirectory, directory)

#     def test_no_revision(self):
#         dir_ = self.copy_charm()
#         self.delete_revision(dir_)
#         charm = CharmDirectory(dir_)
#         self.assertEquals(charm.get_revision(), 0)
#         with open(os.path.join(dir_, "revision")) as f:
#             self.assertEquals(f.read(), "0\n")

#     def test_nonsense_revision(self):
#         dir_ = self.copy_charm()
#         with open(os.path.join(dir_, "revision"), "w") as f:
#             f.write("shifty look")
#         err = self.assertRaises(CharmError, CharmDirectory, dir_)
#         self.assertEquals(
#             str(err),
#             "Error processing %r: invalid charm revision 'shifty look'" % dir_)

#     def test_revision_in_metadata(self):
#         dir_ = self.copy_charm()
#         self.delete_revision(dir_)
#         self.set_metadata_revision(dir_, 999)
#         log = self.capture_logging("juju.charm")
#         charm = CharmDirectory(dir_)
#         self.assertEquals(charm.get_revision(), 999)
#         self.assertIn(
#             "revision field is obsolete. Move it to the 'revision' file.",
#             log.getvalue())

#     def test_competing_revisions(self):
#         dir_ = self.copy_charm()
#         self.set_metadata_revision(dir_, 999)
#         log = self.capture_logging("juju.charm")
#         charm = CharmDirectory(dir_)
#         self.assertEquals(charm.get_revision(), 1)
#         self.assertIn(
#             "revision field is obsolete. Move it to the 'revision' file.",
#             log.getvalue())

#     def test_set_revision(self):
#         dir_ = self.copy_charm()
#         charm = CharmDirectory(dir_)
#         charm.set_revision(123)
#         self.assertEquals(charm.get_revision(), 123)
#         with open(os.path.join(dir_, "revision")) as f:
#             self.assertEquals(f.read(), "123\n")

#     def test_info(self):
#         directory = CharmDirectory(sample_directory)
#         self.assertTrue(directory.metadata is not None)
#         self.assertTrue(isinstance(directory.metadata, MetaData))
#         self.assertEquals(directory.metadata.name, "dummy")
#         self.assertEquals(directory.type, "dir")

#     def test_make_archive(self):
#         # make archive from sample directory
#         directory = CharmDirectory(sample_directory)
#         f = self.makeFile(suffix=".charm")
#         directory.make_archive(f)

#         # open archive in .zip-format and assert integrity
#         from zipfile import ZipFile
#         zf = ZipFile(f)
#         self.assertEqual(zf.testzip(), None)

#         # assert included
#         included = [info.filename for info in zf.infolist()]
#         self.assertEqual(
#             set(included),
#             set(("metadata.yaml", "empty/", "src/", "src/hello.c",
#                  "config.yaml", "hooks/", "hooks/install", "revision")))

#     def test_as_bundle(self):
#         directory = CharmDirectory(self.sample_dir1)
#         charm_bundle = directory.as_bundle()
#         self.assertEquals(type(charm_bundle), CharmBundle)
#         self.assertEquals(charm_bundle.metadata.name, "sample")
#         self.assertIn("sample-1.charm", charm_bundle.path)

#         total_compressed = 0
#         total_uncompressed = 0
#         zip_file = zipfile.ZipFile(charm_bundle.path)
#         for n in zip_file.namelist():
#             info = zip_file.getinfo(n)
#             total_compressed += info.compress_size
#             total_uncompressed += info.file_size
#         self.assertTrue(total_compressed < total_uncompressed)

#     def test_as_bundle_file_lifetime(self):
#         """
#         The temporary bundle file created should have a life time
#         equivalent to that of the directory object itself.
#         """
#         directory = CharmDirectory(self.sample_dir1)
#         charm_bundle = directory.as_bundle()
#         gc.collect()
#         self.assertTrue(os.path.isfile(charm_bundle.path))
#         del directory
#         gc.collect()
#         self.assertFalse(os.path.isfile(charm_bundle.path))

#     def test_compute_sha256(self):
#         """
#         Computing the sha256 of a directory will use the bundled
#         charm, since the hash of the file itself is needed.
#         """
#         directory = CharmDirectory(self.sample_dir1)
#         sha256 = directory.compute_sha256()
#         charm_bundle = directory.as_bundle()
#         self.assertEquals(type(charm_bundle), CharmBundle)
#         self.assertEquals(compute_file_hash(hashlib.sha256,
#                                             charm_bundle.path),
#                           sha256)

#     def test_as_bundle_with_relative_path(self):
#         """
#         Ensure that as_bundle works correctly with relative paths.
#         """
#         current_dir = os.getcwd()
#         os.chdir(self.sample_dir2)
#         self.addCleanup(os.chdir, current_dir)
#         charm_dir = "../%s" % os.path.basename(self.sample_dir1)

#         directory = CharmDirectory(charm_dir)
#         charm_bundle = directory.as_bundle()
#         self.assertEquals(type(charm_bundle), CharmBundle)
#         self.assertEquals(charm_bundle.metadata.name, "sample")

#     def test_charm_base_inheritance(self):
#         """
#         get_sha256() should be implemented in the base class,
#         and should use compute_sha256 to calculate the digest.
#         """
#         directory = CharmDirectory(self.sample_dir1)
#         bundle = directory.as_bundle()
#         digest = compute_file_hash(hashlib.sha256, bundle.path)
#         self.assertEquals(digest, directory.get_sha256())

#     def test_as_directory(self):
#         directory = CharmDirectory(self.sample_dir1)
#         self.assertIs(directory.as_directory(), directory)

#     def test_config(self):
#         """Validate that ConfigOptions are available on the charm"""
#         from juju.charm.tests.test_config import sample_yaml_data
#         directory = CharmDirectory(sample_directory)
#         self.assertEquals(directory.config.get_serialization_data(),
#                           sample_yaml_data)

#     def test_file_type(self):
#         charm_dir = self.copy_charm()
#         os.mkfifo(os.path.join(charm_dir, "foobar"))
#         directory = CharmDirectory(charm_dir)
#         e = self.assertRaises(InvalidCharmFile, directory.as_bundle)
#         self.assertIn("foobar' Invalid file type for a charm", str(e))

#     def test_internal_symlink(self):
#         charm_path = self.copy_charm()
#         external_file = self.makeFile(content='baz')
#         os.symlink(external_file, os.path.join(charm_path, "foobar"))

#         directory = CharmDirectory(charm_path)
#         e = self.assertRaises(InvalidCharmFile, directory.as_bundle)
#         self.assertIn("foobar' Absolute links are invalid", str(e))

#     def test_extract_symlink(self):
#         charm_path = self.copy_charm()
#         external_file = self.makeFile(content='lorem ipsum')
#         os.symlink(external_file, os.path.join(charm_path, "foobar"))

#         directory = CharmDirectory(charm_path)
#         e = self.assertRaises(InvalidCharmFile, directory.as_bundle)
#         self.assertIn("foobar' Absolute links are invalid", str(e))

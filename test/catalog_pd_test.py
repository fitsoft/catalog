import os
import unittest
from catalog_pd import CatalogPd

class TestCalculate(unittest.TestCase):
    def setUp(self):
        pkg_path = os.getcwd()
        self.sample_path = os.path.join(pkg_path, 'samples')

    def test_set_catalog_version_to_original_format(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.set_catalog_version(test_file)
        self.assertEqual(catalog_test.catalog_version,'ORIGINAL_FORMAT')

    def test_set_catalog_version_to_2016_format(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_2.xlsx')
        catalog_test.set_catalog_version(test_file)
        self.assertEqual(catalog_test.catalog_version, '2016_FORMAT')

    def test_set_catalog_version_to_alternate_format(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_3.xlsx')
        catalog_test.set_catalog_version(test_file)
        self.assertEqual(catalog_test.catalog_version, 'ALTERNATE_FORMAT')

    def test_read_catalog_ok(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.read_catalog(test_file)
        self.assertEqual(catalog_test.error, False)

    def test_read_catalog_not_ok(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_invalid.xlsx')
        catalog_test.read_catalog(test_file)
        self.assertEqual(catalog_test.error, True)



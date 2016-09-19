import numpy
import os
import unittest
from catalog_pd import CatalogPd

class TestCatalogPd(unittest.TestCase):
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

    def test_init_fvariables_ok(self):
        file_name = 'catalog ZONE_1.xlsx'
        catalog_test = CatalogPd()
        catalog_test.init_fvariables(file_name)
        self.assertEqual(catalog_test.error, False)

    def test_init_fvariables_error(self):
        file_name = 'catalog_no_zone.xlsx'
        catalog_test = CatalogPd()
        catalog_test.init_fvariables(file_name)
        self.assertEqual(catalog_test.error, True)

    def test_prepare_kpi_name_matrix(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.add_catalog(test_file)
        catalog_test.prepare_kpi_name_matrix()
        matrix_shape = catalog_test.kpi_name_matrix.shape
        all_zeros = not(catalog_test.kpi_name_matrix.any())
        got = (matrix_shape == (100,100) and all_zeros)
        self.assertEqual(got, True)

    def test_prepare_calc_method_matrix(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.add_catalog(test_file)
        catalog_test.prepare_calc_method_matrix()
        matrix_shape = catalog_test.calc_method_matrix.shape
        all_zeros = not (catalog_test.calc_method_matrix.any())
        got = (matrix_shape == (100, 100) and all_zeros)
        self.assertEqual(got, True)

    def test_compute_kpi_name_batch(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.add_catalog(test_file)
        catalog_test.prepare_kpi_name_matrix()
        catalog_test.compute_kpi_name_batch()
        self.assertEqual(catalog_test.kpi_name_matrix.any(), True)

    def test_compute_calc_method_batch(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.add_catalog(test_file)
        catalog_test.prepare_calc_method_matrix()
        catalog_test.compute_calc_method_batch()
        self.assertEqual(catalog_test.calc_method_matrix.any(), True)

    def test_compute_matrixes(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.add_catalog(test_file)
        catalog_test.prepare_kpi_name_matrix()
        while not catalog_test.kpi_done:
            catalog_test.compute_kpi_name_batch()
        catalog_test.compute_matrixes("KPI Name")
        matrix_shape = catalog_test.matrix.shape
        self.assertEqual(matrix_shape,(100,100))

    def test_compute_clusters(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.add_catalog(test_file)
        catalog_test.prepare_kpi_name_matrix()
        while not catalog_test.kpi_done:
            catalog_test.compute_kpi_name_batch()
        catalog_test.compute_matrixes("KPI Name")
        catalog_test.compute_clusters(90)
        self.assertEqual('Group count' in catalog_test.catalog.columns, True)

    def test_open_report(self):
        catalog_test = CatalogPd()
        catalog_test.open_report()
        self.assertEqual(catalog_test.writer_report.engine, 'xlsxwriter')

    def test_write_vba_module(self):
        catalog_test = CatalogPd()
        catalog_test.open_report()
        catalog_test.write_vba_module()
        self.assertEqual(catalog_test.writer_report.book.vba_codename, 'ThisWorkbook')
        if os.path.isfile(catalog_test.report_file):
            os.remove(catalog_test.report_file)

    def test_write_to_excel(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.add_catalog(test_file)
        catalog_test.prepare_kpi_name_matrix()
        while not catalog_test.kpi_done:
            catalog_test.compute_kpi_name_batch()
        catalog_test.compute_matrixes("KPI Name")
        catalog_test.compute_clusters(90)
        catalog_test.open_report()
        catalog_test.write_to_excel(catalog_test.writer_report,catalog_test.catalog,'Groups')
        self.assertTrue(os.path.isfile(catalog_test.report_file))
        os.remove(catalog_test.report_file)

    def test_write_summary(self):
        catalog_test = CatalogPd()
        test_file = os.path.join(self.sample_path, 'catalog_type_1.xlsx')
        catalog_test.add_catalog(test_file)
        catalog_test.prepare_kpi_name_matrix()
        while not catalog_test.kpi_done:
            catalog_test.compute_kpi_name_batch()
        catalog_test.compute_matrixes("KPI Name")
        catalog_test.compute_clusters(90)
        catalog_test.open_report()
        catalog_test.write_summary(catalog_test.writer_report, test_file, "KPI Name", 90)
        self.assertTrue(os.path.isfile(catalog_test.report_file))
        os.remove(catalog_test.report_file)

import unittest
import support
import tempfile
import xlsxwriter


class TestSupport(unittest.TestCase):
    def test_add_to_format(self):
        temp_wb = tempfile.NamedTemporaryFile()
        workbook = xlsxwriter.Workbook(temp_wb)
        test_format = {'bold': 1, 'font_size': 16, 'fg_color': '#00FF00'}
        new_format = workbook.add_format()
        support.add_to_format(new_format, test_format, workbook)
        self.assertTrue(new_format in workbook.formats)

    def test_box(self):
        temp_wb = tempfile.NamedTemporaryFile()
        workbook = xlsxwriter.Workbook(temp_wb)
        sheet = workbook.add_worksheet()
        test_format = {'bold': 1, 'font_size': 16, 'fg_color': '#00FF00'}
        got = support.box(workbook, sheet, 1, 1, 5, 5, test_format)
        exp = 0
        self.assertEqual(got, exp)

    def test_get_date_time(self):
        date_string = support.get_date_time()
        self.assertIsInstance(date_string, str)

    def test_compute_similarity_is_min(self):
        string = "identical strings"
        got = support.compute_similarity(string, string)
        exp = 0
        self.assertEqual(got, exp)

    def test_compute_similarity_is_max(self):
        string_1 = "abcdefghij"
        string_2 = "mnopqrstuv"
        got = support.compute_similarity(string_1, string_2)
        exp = 1
        self.assertEqual(got, exp)
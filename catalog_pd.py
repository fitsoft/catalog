import datetime
from distutils.dir_util import mkpath
from fuzzywuzzy import fuzz
from itertools import combinations
import numpy as np
import os
import pandas as pd
from scipy.io import mmread
from scipy.io import mmwrite
from sklearn.cluster import DBSCAN
import sys
import xlrd
import xlsxwriter

pd.options.mode.chained_assignment = None

COL_DICT = {'Name': 'KPI name', 'KPI': 'KPI ID',
            'Owner': 'KPI owner', 'Achievement Rule': 'Partial achievement',
            'Source': 'Source', 'Calculation Method': 'Calculation method'}

COL_DICT1 = {'Name': 'KPI name', 'KPI': 'KPI ID',
             'Owner': 'KPI owner', 'Achievement Rule': 'Partial achievement',
             'Source': 'Source', 'Calculation Method': 'Calculation method',
             'Created at Zone': 'Zone'}

COL_DICT2 = {'KPI - Name': 'KPI name', 'Code': 'KPI ID',
             'Owner': 'KPI owner',
             'Partial Achievement Rule': 'Partial achievement',
             'Source': 'Source', 'Calculation Method': 'Calculation method',
             'Zone': 'Zone'}

COLS_OUTPUT = ['KPI name', 'KPI ID', 'Calculation method', 'Source',
               'Partial achievement', 'KPI owner', 'Zone', 'Type']


HEADER = {
    'bold': 1,
    'border': 1,
    'fg_color': '#FF0000',
    'font_color': '#FFFFFF'}

GROUP = {'bg_color': '#330000'}


# xlsxwriter box functions
def add_to_format(existing_format, dict_of_properties, workbook):
    """Give a format you want to extend and a dict of the properties you want to
    extend it with, and you get them returned in a single format"""
    new_dict = {}
    for key, value in existing_format.__dict__.iteritems():
        if (value != 0) and (value != {}) and (value is not None):
            new_dict[key] = value
    del new_dict['escapes']
    return(workbook.add_format(dict(new_dict.items() +
                                    dict_of_properties.items())))


def box(workbook, sheet_name, row_start, col_start,
        row_stop, col_stop, format):
    """Makes an RxC box. Use integers, not the 'A1' format"""

    rows = row_stop - row_start + 1
    cols = col_stop - col_start + 1

    for x in xrange((rows) * (cols)):  # Total number of cells in the rectangle
        box_form = workbook.add_format()   # The format resets each loop
        row = row_start + (x // cols)
        column = col_start + (x % cols)

        format_box = format.copy()
        if x < (cols):                     # If it's on the top row
            format_box['top'] = 1
        if x >= ((rows * cols) - cols):    # If it's on the bottom row
            format_box['bottom'] = 1
        if x % cols == 0:                  # If it's on the left column
            format_box['left'] = 1
        if x % cols == (cols - 1):         # If it's on the right column
            format_box['right'] = 1
        box_form = add_to_format(box_form, format_box, workbook)
        sheet_name.write(row, column, "", box_form)


def resource_path(relative):
    """Return path to resources"""
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")), relative)


def get_date_time():
    """Return formatted current date/time"""
    date_time = datetime.datetime.now()
    return date_time.strftime("%d-%m-%Y_%H%M")


def compute_similarity(s1, s2):
    """Compute similarity between two input strings"""
    return 1.0 - (0.01 * max(
        fuzz.ratio(s1, s2),
        fuzz.token_sort_ratio(s1, s2),
        fuzz.token_set_ratio(s1, s2)))


class CatalogPd(object):
    """Process catalog files for clustering"""
    NA_VALUES = ['-1.#IND', '1.#QNAN', '1.#IND', '-1.#QNAN', '#N/A', 'N/A',
                 '#NA', 'NULL', 'NaN', '-NaN', 'nan', '-nan']

    def __init__(self):
        # set application path
        if getattr(sys, 'frozen', False):
            self.app_path = os.path.dirname(sys.executable)
        elif __file__:
            self.app_path = os.path.dirname(__file__)
        self.error = False
        self.error_type = ""
        self.catalog = pd.DataFrame()
        self.catalog_version = None
        self.output_file = None
        self.name = None
        self.ext = None
        self.path = None
        self.zone = None
        self.fname = None
        self.df = None
        # init matrix related properties
        self.kpi_name = None
        self.kpi_len = None
        self.X = None
        self.kpi_iter = None
        self.kpi_done = False
        self.calc_method = None
        self.calc_len = None
        self.Y = None
        self.calc_method_iter = None
        self.calc_done = None
        self.kpi_row = None
        self.calc_row = None
        self.total_groups = 0
        self.total_items_in_groups = 0

    def add_catalog(self, file):
        """Add catalog file for processing"""
        self.init_fvariables(file)
        self.set_catalog_version(file)
        if not self.error:
            self.read_catalog(file)
            self.catalog = pd.concat(
                [self.df, self.catalog], ignore_index=True)

    def read_catalog(self, file):
        """Retrieve catalog information"""
        self.set_catalog_version(file)
        if not self.error:
            self.df.dropna(subset=['KPI name'], inplace=True)
            if not len(self.df):
                self.error = True
                error_msg = 'Empty catalog file\r\n\r\n %s \r\n\r\n '
                self.error_type = error_msg % file
            else:
                if 'Zone' not in self.df.columns:
                    self.df['Zone'] = self.zone
                self.df = self.df[COLS_OUTPUT]

    def set_catalog_version(self, file):
        """Determine catalog version (3 possible catalog formats)"""
        self.catalog_version = None
        self.error = False

        workbook = xlrd.open_workbook(file)
        sheet = workbook.sheet_by_index(0)
        # lets read column F and find headers
        column = sheet.col_values(5, 0, 10)
        if 'KPI owner' in column or \
                'Valid until' in column:
            self.df = pd.read_excel(
                file, keep_default_na=False, na_values=self.NA_VALUES)
            self.catalog_version = 'ORIGINAL_FORMAT'
            self.df = self.df[COL_DICT.values()]
            self.df['Type'] = 'CATALOG'
            return

        elif 'Achievement Rule' in column:
            idx = column.index('Achievement Rule')
            self.df = pd.read_excel(file, skiprows=idx, keep_default_na=False,
                                    na_values=self.NA_VALUES)
            self.catalog_version = '2016_FORMAT'
            self.df = self.df[COL_DICT1.keys()]
            self.df.columns = [COL_DICT1[el] for el in self.df.columns]
            self.df['Type'] = 'CATCHBALL'
            return

        elif 'Calculation Method' in column:
            idx = column.index('Calculation Method')
            self.df = pd.read_excel(file, skiprows=idx, keep_default_na=False,
                                    na_values=self.NA_VALUES)
            self.catalog_version = 'ALTERNATE_FORMAT'
            self.df = self.df[COL_DICT2.keys()]
            self.df.columns = [COL_DICT2[el] for el in self.df.columns]
            self.df['Type'] = 'CATCHBALL'
            return
        self.error = True
        error_msg = 'Unrecognized catalog file\r\n\r\n %s \r\n\r\n'
        self.error_type = error_msg % file

    def init_fvariables(self, file):
        """Set path,extention,etc. information related to input file"""
        self.path, self.fname = os.path.split(file)
        self.name, self.ext = self.fname.split(os.extsep)
        self.catalog_version = None
        try:
            self.zone = self.name.split(' ')[1]
        except IndexError:
            self.error = True
            self.error_type = "Error in file name \r\n\r\n%s\r\n\r\n" % file

    def prepare_kpi_name_matrix(self):
        """Initialize kpi name matrix"""
        self.kpi_name = self.catalog['KPI name'].values.tolist()
        self.kpi_len = len(self.kpi_name)
        self.X = np.zeros((self.kpi_len, self.kpi_len))
        self.kpi_iter = iter(range(self.kpi_len))
        self.kpi_done = False

    def prepare_calc_method_matrix(self):
        """Initialize calculation method matrix"""
        self.calc_method = self.catalog['Calculation method'].values.tolist()
        self.calc_len = len(self.calc_method)
        self.Y = np.zeros((self.calc_len, self.calc_len))
        self.calc_method_iter = iter(range(self.calc_len))
        self.calc_done = False

    def compute_kpi_name_batch(self, batch_size=10):
        """Compute kpi name batch"""
        try:
            for count in range(batch_size):
                self.kpi_row = next(self.kpi_iter)
                for j in range(self.kpi_len):
                    if self.X[self.kpi_row, j] == 0.0:
                        self.X[self.kpi_row, j] = compute_similarity(
                            self.kpi_name[self.kpi_row].lower(),
                            self.kpi_name[j].lower())
                        self.X[j, self.kpi_row] = self.X[self.kpi_row, j]
        except StopIteration:
            self.kpi_done = True
            self.X *= self.X
            mmwrite("X2.mtx", self.X)
            self.X = None

    def compute_calc_method_batch(self, batch_size=10):
        """Compute calculation method batch"""
        try:
            for count in range(batch_size):
                self.calc_row = next(self.calc_method_iter)
                for j in range(self.calc_len):
                    if self.Y[self.calc_row, j] == 0.0:
                        self.Y[self.calc_row, j] = compute_similarity(
                            self.calc_method[self.calc_row],
                            self.calc_method[j])
                        self.Y[j, self.calc_row] = self.Y[self.calc_row, j]
        except StopIteration:
            self.calc_done = True
            self.Y *= self.Y
            mmwrite("Y2.mtx", self.Y)

    def compute_matrixes(self, criteria):
        """Comput matrixes according to criteria"""
        INV_SQRT_2 = (1 / 2.0)**.5
        if criteria == 0:
            self.X = mmread("X2.mtx")
            self.X += mmread("Y2.mtx")
        elif criteria == 1:
            self.X = mmread("X2.mtx")
        elif criteria == 2:
            self.X = mmread("Y2.mtx")
        self.X **= 0.5
        if criteria == 0:
            self.X *= INV_SQRT_2
        self.matrix = self.X
        # clean up
        if os.path.isfile("X2.mtx"):
            os.remove("X2.mtx")
        if os.path.isfile("Y2.mtx"):
            os.remove("Y2.mtx")

    def compute_clusters(self, percentage):
        """Compute clusters"""
        eps = (100 - percentage) / 100.0
        kpi_name = self.catalog['KPI name'].values.tolist()
        calc_method = self.catalog['Calculation method'].values.tolist()

        clust = DBSCAN(eps=eps, min_samples=1, metric="precomputed")
        clust.fit(self.matrix)
        preds = clust.labels_
        clabels = np.unique(preds)

        perc = np.zeros(len(self.catalog))
        self.total_groups = 0
        self.total_items_in_groups = 0
        for i in range(clabels.shape[0]):
            if clabels[i] < 0:
                continue
            cmem_ids = np.where(preds == clabels[i])[0]
            cmembers = []
            if len(cmem_ids) > 1:
                self.total_groups += 1
                self.total_items_in_groups += len(cmem_ids)

            # build groups
            mgroup = list(combinations(cmem_ids, 2))
            ave = 0
            for el in mgroup:
                ave += (1 - self.matrix[el[0]][el[1]])

            if mgroup:
                ave = ave / float(len(mgroup))
                for el in cmem_ids:
                    perc[el] = ave

            for cmem_id in cmem_ids:
                cmembers.append(kpi_name[cmem_id])
                # number groups from 1
                self.catalog.set_value(cmem_id, 'Group', i + 1)

        # add group count
        for i, row in self.catalog.iterrows():
            count = self.catalog[self.catalog['Group'] ==
                                 row['Group']].count().ix[0]
            self.catalog.set_value(i, 'Group count', count)

        self.catalog['Similarity'] = perc
        self.catalog.sort(['Group count', 'Group'],
                          ascending=[0, 1], inplace=True)

    def write_to_excel(self, writer, df, sheet_name):
        """Write output excel spreasheet"""
        df.fillna('', inplace=True)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        worksheet = writer.sheets[sheet_name]
        header_format = writer.book.add_format(HEADER)
        group_format = writer.book.add_format(GROUP)
        wrap_format = writer.book.add_format()
        wrap_format.set_text_wrap()

        header = list(df.columns)
        header.append('Status')
        worksheet.set_row(0, 22)
        for i, el in enumerate(header):
            worksheet.write(0, i, el, header_format)

        # add picklist
        worksheet.set_column('A:A', 40)
        worksheet.set_column('C:C', 110)
        val_dict = {'validate': 'list', 'source': ['Approved', 'Not Approved']}
        for i in range(2, len(df) + 2):
            worksheet.data_validation(
                chr(ord('A') + len(header) - 1) + str(i), val_dict)
            worksheet.write(
                i - 1, 2, df.iloc[i - 2]['Calculation method'], wrap_format)
        worksheet.freeze_panes(1, 2)
        worksheet.set_zoom(75)

    def write_summary(self, writer, files, criteria, percentage):
        """Write summary to excel spreadsheet"""
        title_format = {'bold': 1, 'font_size': 16, 'fg_color': '#FCD5b4'}
        foreground_fomat = {'fg_color': '#FCD5b4'}
        white_foreground = {'fg_color': '#FFFFFF', }
        right_col_format = {'align': 'center', 'bold': 1, 'border': 1}
        file_format = {'align': 'left', 'bold': 1}
        left_col_format = {'bold': 1, 'border': 1, 'align': 'center',
                           'fg_color': '#FDE9D9', 'font_color': '#E46D0A'}
        file_title_format = {'bold': 1, 'border': 1, 'align': 'center',
                             'fg_color': '#708090', 'font_color': '#FFFFFF'}
        percentage_format = {'align': 'center', 'border': 1,
                             'num_format': '0 %', 'bold': 1}

        emptyDF = pd.DataFrame()
        emptyDF.to_excel(writer, sheet_name="Summary", index=False)
        worksheet = writer.sheets["Summary"]
        left_format = writer.book.add_format(left_col_format)
        right_format = writer.book.add_format(right_col_format)
        white_format = writer.book.add_format(foreground_fomat)
        title_format = writer.book.add_format(title_format)
        file_format = writer.book.add_format(file_format)
        file_title = writer.book.add_format(file_title_format)
        perc_format = writer.book.add_format(percentage_format)

        col_widths = [3, 50, 70, 3]
        worksheet.set_column('A:A', col_widths[0])
        worksheet.set_column('B:B', col_widths[1])
        worksheet.set_column('C:C', col_widths[2])
        worksheet.set_column('D:D', col_widths[3])
        worksheet.insert_image('B1', './data/.resources/logo.png')
        row = 6
        for i in range(4):
            for j in range(5):
                worksheet.write(j, i, "", white_format)
        worksheet.set_row(4, 22)
        box(writer.book, worksheet, 0, 0, 4, 3, foreground_fomat)
        box(writer.book, worksheet, 5, 0, 17 + len(files), 3, white_foreground)

        worksheet.write(
            4, 1, "Catalog: Duplicate KPIs detection", title_format)

        for i, el in enumerate(files):
            worksheet.write(i + row, 2, el, file_format)
            if i == 0:
                worksheet.write(row, 1, "Processed files:", file_title)
        row += len(files) + 3

        perc = self.total_items_in_groups * 100 / float(len(self.catalog))
        items_in_group = "%d (%2.0f %%)" % (self.total_items_in_groups, perc)

        worksheet.insert_image(
            'A' + str(row - 1), './data/.resources/arrow.png')
        worksheet.set_row(row - 1, 20)
        worksheet.write(row, 1, 'Similarity % Selected:', left_format)
        worksheet.write(row, 2, percentage / 100.0, perc_format)
        row += 1

        worksheet.write(row, 1, 'Criteria:', left_format)
        crit_dict = {0: 'KPI Name + Calculation Method',
                     1: 'KPI Name', 2: 'Calculation Method'}
        worksheet.write(row, 2, crit_dict[criteria], right_format)
        row += 1

        worksheet.write(row, 1, 'Zones / Functions analyzed:', left_format)
        zones_list = self.catalog['Zone'].dropna().unique()
        zones = ' + '.join(zones_list.tolist())
        worksheet.write(row, 2, zones, right_format)
        row += 1

        worksheet.write(row, 1, 'Source Type:', left_format)
        type = ' + '.join(self.catalog['Type'].unique().tolist()).title()
        worksheet.write(row, 2, type, right_format)
        row += 1

        worksheet.write(row, 1, 'Total items:', left_format)
        worksheet.write(row, 2, len(self.catalog), right_format)
        row += 1

        worksheet.write(row, 1, 'Total groups:', left_format)
        worksheet.write(row, 2, self.catalog.Group.max(), right_format)
        row += 1

        worksheet.write(row, 1, 'Total groups (+1 element):', left_format)
        worksheet.write(row, 2, self.total_groups, right_format)
        row += 1

        worksheet.write(row, 1, 'Total items in groups:', left_format)
        worksheet.write(row, 2, items_in_group, right_format)

    def open_report(self):
        """Open report"""
        self.report_path = os.path.join(self.app_path, 'data')
        mkpath(self.report_path)

        self.output_file = get_date_time() + '.xlsx'
        self.report_file = os.path.join(self.report_path, self.output_file)
        self.writer_report = pd.ExcelWriter(
            self.report_file, engine='xlsxwriter')

    def write_vba_module(self):
        """Add VBA module to xls spreadsheet"""
        self.writer_report.book.filename = self.report_file[:-1] + 'm'
        self.writer_report.book.add_vba_project(
            './data/.resources/vbaProject.bin')
        self.writer_report.book.set_vba_name('ThisWorkbook')

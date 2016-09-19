import datetime
from fuzzywuzzy import fuzz
import xlsxwriter


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


def box(workbook, sheet_name, box_coordinates, cell_format):
    """Makes an RxC box. Use integers, not the 'A1' format"""
    row_start, col_start, row_stop, col_stop = box_coordinates
    rows = row_stop - row_start + 1
    cols = col_stop - col_start + 1

    for item in xrange((rows) * (cols)):  # Total number of cells in the rectangle
        box_form = workbook.add_format()   # The format resets each loop
        row = row_start + (item // cols)
        column = col_start + (item % cols)

        format_box = cell_format.copy()
        if item < (cols):                     # If it's on the top row
            format_box['top'] = 1
        if item >= ((rows * cols) - cols):    # If it's on the bottom row
            format_box['bottom'] = 1
        if item % cols == 0:                  # If it's on the left column
            format_box['left'] = 1
        if item % cols == (cols - 1):         # If it's on the right column
            format_box['right'] = 1
        box_form = add_to_format(box_form, format_box, workbook)
        ret_value = sheet_name.write(row, column, "", box_form)
        if ret_value:
            return ret_value
    return 0


def get_date_time():
    """Return formatted current date/time"""
    date_time = datetime.datetime.now()
    return date_time.strftime("%d-%m-%Y_%H%M")


def compute_similarity(string_1, string_2):
    """Compute similarity between two input strings"""
    return 1.0 - (0.01 * max(
        fuzz.ratio(string_1, string_2),
        fuzz.token_sort_ratio(string_1, string_2),
        fuzz.token_set_ratio(string_1, string_2)))

import os
import sys
import time
import threading
from os.path import expanduser
from PySide import QtCore
from PySide import QtGui
import catalog_window
import catalog_pd


# Main Window Class
class CatalogMainWindow(QtGui.QMainWindow, catalog_window.Ui_Catalog):
    status_signal = QtCore.Signal(str, int)
    progress_signal = QtCore.Signal(int)
    done_signal = QtCore.Signal()
    error_msg = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(CatalogMainWindow, self).__init__(parent)
        self.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/icon.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        self.connect(self.fileList,
                     QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem *)"),
                     self.remove_item)

        self.status_signal.connect(self.set_message)
        self.error_msg.connect(self.show_message)
        self.progress_signal.connect(self.progress_bar.setValue)
        self.progress_bar.setTextVisible(False)
        self.done_signal.connect(self.reset_gui)

        self.progress_bar.setValue(0)
        self.file_list = []
        self.working = False
        self.spinBox.setValue(80)
        self.thread = None
        self.app_path = None
        self.report_path = None
        self.report_path = None

    # ---------------------------------------------
    # SLOT FUNCTIONS
    # ---------------------------------------------
    @QtCore.Slot(str, int)
    def set_message(self, msg, duration=0):
        if duration == 0:
            self.statusbar.showMessage(msg)
        else:
            self.statusbar.showMessage(msg, duration)

    @QtCore.Slot("")
    def on_browseReportsButton_clicked(self):
        if getattr(sys, 'frozen', False):
            self.app_path = os.path.dirname(sys.executable)
        elif __file__:
            self.app_path = os.path.dirname(__file__)
        self.report_path = os.path.join(self.app_path, 'data')
        self.report_path = self.report_path.replace("/", "\\")
        from subprocess import call
        call(["explorer", self.report_path])

    @QtCore.Slot("")
    def on_appendButton_clicked(self):
        if self.working:
            return
        # clear status bar
        self.status_signal.emit("", 0)
        path = QtGui.QFileDialog.getOpenFileNames(caption="Choose files",
                                            dir=os.path.join(
                                                expanduser("~"), "Desktop"),
                                            filter="*.xls*")[0]
        for el in path:
            self.file_list.append(str(el))
        self.file_list = list(set(self.file_list))
        self.fileList.clear()
        self.fileList.addItems(self.file_list)

    @QtCore.Slot("")
    def on_processButton_clicked(self):
        if self.working:
            return
        self.statusbar.showMessage('Please wait...')
        if self.file_list:
            index = self.comboBox.currentIndex()
            self.thread = threading.Thread(target=self.worker,
                                           args=(self.spinBox.value(), index))
            self.thread.setDaemon(True)
            self.thread.start()
        else:
            self.statusbar.showMessage('No file selected for processing',
                                       2000)

    @QtCore.Slot("")
    def on_exitButton_clicked(self):
        pass

    @QtCore.Slot(str, int)
    def status_message(self, msg, duration=0):
        if duration == 0:
            self.statusbar.showMessage(msg)
        else:
            self.statusbar.showMessage(msg, duration)

    # ------------------------------------------------------
    # Signal functions
    # ------------------------------------------------------
    def emit_status_signal(self, string):
        self.status_signal.emit(string)

    def emit_progress_signal(self, integer):
        self.progress_signal.emit(integer)

    def emit_done_signal(self):
        self.done_signal.emit()

    # ------------------------------------------------------
    # Slot functions
    # ------------------------------------------------------
    def remove_item(self, item):
        if not self.working:
            idx = self.fileList.currentRow()
            self.fileList.takeItem(idx)
            del self.file_list[idx]

    def reset_gui(self):
        self.fileList.clear()
        self.file_list = []
        self.progress_bar.setValue(0)

    def show_message(self, error_description):
        error = QtGui.QMessageBox(self)
        error.critical(self, 'CatalogTool', error_description)

    def worker(self, percentage, criteria):
        self.working = True
        invalid_files = False
        if criteria == 0:
            factor = 50
            offset = 50
        else:
            factor = 100
            offset = 0
        df = catalog_pd.CatalogPd()
        for el in self.file_list:
            self.status_signal.emit('Importing file: ' + el + '. Please wait...', 0)
            df.add_catalog(el)
            self.status_signal.emit('', 0)
            if df.error:
                invalid_files = True
                self.error_msg.emit(df.error_type)
                break
            else:
                self.status_signal.emit('File ' + el + ' imported successfully', 0)
                # keep message ON
                time.sleep(1)
        if not invalid_files:
            try:
                if criteria != 2:
                    df.prepare_kpi_name_matrix()
                    self.status_signal.emit(
                        'Computing KPI Name similarity matrix', 0)
                    while not df.kpi_done:
                        df.compute_kpi_name_batch()
                        self.progress_signal.emit(
                            int((df.kpi_row + 1) * factor / df.kpi_len))

                if criteria != 1:
                    self.status_signal.emit(
                        'Computing Calculation Method similarity matrix', 0)
                    df.prepare_calc_method_matrix()
                    while not df.calc_done:
                        df.compute_calc_method_batch()
                        progress = int((df.calc_row + 1) * factor /
                                       df.calc_len) + offset
                        self.progress_signal.emit(progress)

                df.compute_matrixes(criteria)
                df.compute_clusters(percentage)
                df.open_report()
                df.write_summary(df.writer_report,
                                 self.file_list, criteria, percentage)
                df.write_to_excel(df.writer_report, df.catalog, "Groups")
                df.write_vba_module()
                self.file_list = []
                self.progress_signal.emit(100)
                self.status_signal.emit("Processing completed", 0)

            except MemoryError:
                self.error_msg.emit("Memory error\r\n\r\n")
            except Exception, err:
                self.error_msg.emit("Unhandled Error:" +
                                    err.message + "\r\n\r\n")

        self.emit_done_signal()
        self.working = False

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = CatalogMainWindow()
    form.show()
    app.exec_()

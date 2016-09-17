# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui

# Form implementation generated from reading ui file
# 'c:\Users\Clara\Dropbox\Software\Quilmes\Software\Catalog\Catalog.ui'
#
# Created: Thu Dec 17 07:54:49 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!


class Ui_Catalog(object):

    def setupUi(self, Catalog):
        Catalog.setObjectName("Catalog")
        Catalog.resize(800, 403)
        Catalog.setMinimumSize(QtCore.QSize(800, 400))
        Catalog.setMaximumSize(QtCore.QSize(155555, 155555))
        Catalog.setStyleSheet("QMainMenu{\n"
                              "image: url(:/images/images/Entypo_e776(0)_64.png);\n"
                              "}")
        self.centralwidget = QtGui.QWidget(Catalog)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setMinimumSize(QtCore.QSize(530, 0))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/images/images/eagle.png"))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.spinBox = QtGui.QSpinBox(self.centralwidget)
        self.spinBox.setMaximumSize(QtCore.QSize(60, 16777215))
        self.spinBox.setMinimum(75)
        self.spinBox.setMaximum(99)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_2.addWidget(self.spinBox)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fileList = QtGui.QListWidget(self.centralwidget)
        self.fileList.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.fileList.setFont(font)
        self.fileList.setObjectName("fileList")
        self.horizontalLayout.addWidget(self.fileList)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(14)
        self.verticalLayout.setContentsMargins(16, 12, 16, 12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.appendButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(
            self.appendButton.sizePolicy().hasHeightForWidth())
        self.appendButton.setSizePolicy(sizePolicy)
        self.appendButton.setMinimumSize(QtCore.QSize(200, 0))
        self.appendButton.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.appendButton.setFont(font)
        self.appendButton.setStyleSheet("QPushButton\n"
                                        "\n"
                                        "{\n"
                                        "background-color: rgb(255, 109, 33);\n"
                                        "    color: rgb(255, 255, 255);\n"
                                        "border-width: 2px;\n"
                                        "  border-radius: 8px;\n"
                                        "    border-style: solid;\n"
                                        "border-color:  rgb(255, 109, 33);\n"
                                        "border-style: outset;\n"
                                        "}\n"
                                        " \n"
                                        "QPushButton:pressed\n"
                                        "{\n"
                                        "    background-color: rgb(245, 100, 30);\n"
                                        "     border-style: inset;\n"
                                        "    \n"
                                        "}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/images/plus.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.appendButton.setIcon(icon)
        self.appendButton.setObjectName("appendButton")
        self.verticalLayout.addWidget(self.appendButton)
        self.processButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(
            self.processButton.sizePolicy().hasHeightForWidth())
        self.processButton.setSizePolicy(sizePolicy)
        self.processButton.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.processButton.setFont(font)
        self.processButton.setStyleSheet("QPushButton\n"
                                         "\n"
                                         "{\n"
                                         "background-color: rgb(255, 109, 33);\n"
                                         "    color: rgb(255, 255, 255);\n"
                                         "border-width: 2px;\n"
                                         "  border-radius: 8px;\n"
                                         "    border-style: solid;\n"
                                         "border-color:  rgb(255, 109, 33);\n"
                                         "border-style: outset;\n"
                                         "}\n"
                                         "QPushButton:pressed\n"
                                         "{\n"
                                         "    background-color: rgb(245, 100, 30);\n"
                                         "     border-style: inset;\n"
                                         "    \n"
                                         "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/images/play.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.processButton.setIcon(icon1)
        self.processButton.setObjectName("processButton")
        self.verticalLayout.addWidget(self.processButton)
        self.browseReportsButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(
            self.browseReportsButton.sizePolicy().hasHeightForWidth())
        self.browseReportsButton.setSizePolicy(sizePolicy)
        self.browseReportsButton.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.browseReportsButton.setFont(font)
        self.browseReportsButton.setStyleSheet("QPushButton\n"
                                               "\n"
                                               "{\n"
                                               "background-color: rgb(255, 109, 33);\n"
                                               "    color: rgb(255, 255, 255);\n"
                                               "border-width: 2px;\n"
                                               "  border-radius: 8px;\n"
                                               "    border-style: solid;\n"
                                               "border-color:  rgb(255, 109, 33);\n"
                                               "border-style: outset;\n"
                                               "}\n"
                                               " QPushButton:pressed\n"
                                               "{\n"
                                               "    background-color: rgb(245, 100, 30);\n"
                                               "     border-style: inset;\n"
                                               "    \n"
                                               "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/images/search.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.browseReportsButton.setIcon(icon2)
        self.browseReportsButton.setObjectName("browseReportsButton")
        self.verticalLayout.addWidget(self.browseReportsButton)
        self.exitButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(
            self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy)
        self.exitButton.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("QPushButton\n"
                                      "\n"
                                      "{\n"
                                      "background-color: rgb(255, 109, 33);\n"
                                      "    color: rgb(255, 255, 255);\n"
                                      "border-width: 2px;\n"
                                      "  border-radius: 8px;\n"
                                      "    border-style: solid;\n"
                                      "border-color:  rgb(255, 109, 33);\n"
                                      "border-style: outset;\n"
                                      "}\n"
                                      "QPushButton:pressed\n"
                                      "{\n"
                                      "    background-color: rgb(245, 100, 30);\n"
                                      "     border-style: inset;\n"
                                      "    \n"
                                      "}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(
            ":/images/images/arrow-right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon3)
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout.addWidget(self.exitButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.progress_bar = QtGui.QProgressBar(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.progress_bar.setFont(font)
        self.progress_bar.setStyleSheet("QProgressBar::chunk {\n"
                                       "/*background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,\n"
                                       "stop: 0 #78d,\n"
                                       "stop: 0.4999 #46a,\n"
                                       "stop: 0.5 #45a,\n"
                                       "stop: 1 #238 );*/\n"
                                       "background:  rgb(255, 109, 33);\n"
                                       "border-bottom-right-radius: 7px;\n"
                                       "border-bottom-left-radius: 7px;\n"
                                       "border: 1px solid black;\n"
                                       "\n"
                                       "}")
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setAlignment(
            QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.progress_bar.setInvertedAppearance(False)
        self.progress_bar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progress_bar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progress_bar)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        Catalog.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Catalog)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        Catalog.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Catalog)
        self.statusbar.setObjectName("statusbar")
        Catalog.setStatusBar(self.statusbar)

        self.retranslateUi(Catalog)
        QtCore.QObject.connect(
            self.exitButton, QtCore.SIGNAL("clicked()"), Catalog.close)
        QtCore.QMetaObject.connectSlotsByName(Catalog)

    def retranslateUi(self, Catalog):
        Catalog.setWindowTitle(QtGui.QApplication.translate(
            "Catalog", "ABInBev - Catalog Toolkit", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate(
            "Catalog", "Both", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate(
            "Catalog", "KPI Name", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate(
            "Catalog", "Calculation Method", None, QtGui.QApplication.UnicodeUTF8))
        self.appendButton.setText(QtGui.QApplication.translate(
            "Catalog", "ADD CATALOG", None, QtGui.QApplication.UnicodeUTF8))
        self.processButton.setText(QtGui.QApplication.translate(
            "Catalog", "COMPUTE", None, QtGui.QApplication.UnicodeUTF8))
        self.browseReportsButton.setText(QtGui.QApplication.translate(
            "Catalog", "BROWSE REPORTS", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate(
            "Catalog", "EXIT", None, QtGui.QApplication.UnicodeUTF8))

import resources

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Catalog = QtGui.QMainWindow()
    ui = Ui_Catalog()
    ui.setupUi(Catalog)
    Catalog.show()
    sys.exit(app.exec_())

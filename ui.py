# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AddressScraperWindow(object):
    def setupUi(self, AddressScraperWindow):
        AddressScraperWindow.setObjectName(_fromUtf8("AddressScraperWindow"))
        AddressScraperWindow.resize(1200, 800)
        self.centralwidget = QtGui.QWidget(AddressScraperWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.address_box = QtGui.QTextEdit(self.centralwidget)
        self.address_box.setGeometry(QtCore.QRect(20, 60, 261, 300))
        self.address_box.setObjectName(_fromUtf8("address_box"))
        self.address_list_label = QtGui.QLabel(self.centralwidget)
        self.address_list_label.setGeometry(QtCore.QRect(20, 30, 181, 16))
        self.address_list_label.setObjectName(_fromUtf8("address_list_label"))
        
        
        self.result_box = QtGui.QTextEdit(self.centralwidget)
        self.result_box.setGeometry(QtCore.QRect(20, 420, 261, 300))
        self.result_box.setObjectName(_fromUtf8("result_box"))
        
        
        self.process_button = QtGui.QPushButton(self.centralwidget)
        self.process_button.setGeometry(QtCore.QRect(20, 750, 75, 23))
        self.process_button.setObjectName(_fromUtf8("process_button"))
        
        self.reset_button = QtGui.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(QtCore.QRect(100, 750, 75, 23))
        self.reset_button.setObjectName(_fromUtf8("reset_button"))
        
        
        self.quit_button = QtGui.QPushButton(self.centralwidget)
        self.quit_button.setGeometry(QtCore.QRect(180, 750, 75, 23))
        self.quit_button.setObjectName(_fromUtf8("close_button"))
        
        
        
        self.web_view = QWebView(self.centralwidget)
        self.web_view.setGeometry(QtCore.QRect(300, 60, 1200, 800))
        self.web_view.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.web_view.setObjectName(_fromUtf8("web_view"))
        AddressScraperWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AddressScraperWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 819, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        AddressScraperWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AddressScraperWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        AddressScraperWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AddressScraperWindow)
        QtCore.QMetaObject.connectSlotsByName(AddressScraperWindow)

    def retranslateUi(self, AddressScraperWindow):
        AddressScraperWindow.setWindowTitle(_translate("AddressScraperWindow", "Address Scraper", None))
        self.address_list_label.setText(_translate("AddressScraperWindow", "Enter List Of Addresses", None))
        
        self.process_button.setText(_translate("AddressScraperWindow", "Get Data", None))
        
        self.reset_button.setText(_translate("AddressScraperWindow", "Reset", None))
        
        self.quit_button.setText(_translate("AddressScraperWindow", "Quit", None))



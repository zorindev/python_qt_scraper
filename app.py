import sys
import os

import unicodedata
from bs4 import BeautifulSoup
import re
from lxml import html
from PyQt4 import QtGui, uic
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebView

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PyQt4.QtCore import pyqtSlot


import ui

import time

from __builtin__ import True

Ui_MainWindow = ui.Ui_AddressScraperWindow


class AddressScraper(QtGui.QMainWindow, Ui_MainWindow):
    
    hard_stop = False
    
    address_to_search = ""
    address_to_process_index = 0
    
    address = ""
    first_name = ""
    last_name = ""
    mail_address = ""
    mail_city = ""
    mail_state = ""
    mail_zip = ""
    
    report_csv = "";
    report_header = str("PROPERTY ADDRESS, FIRST NAME, LAST NAME, MAIL ADDRESS, MAIL CITY, MAIL STATE, MAIL ZIP")
    
    direction_types = {
        'Any': 0,
        'E'  : 1, 
        'N'  : 2, 
        'NE' : 3, 
        'NW' : 4, 
        'S'  : 5,
        'W'  : 6
    }
    
    street_types = {
        'Any': 0,
        'AVE': 1,
        'BLVD': 2,
        'CR': 3,
        'CT': 4,
        'DR': 5,
        'HWY': 6,
        'LN' : 7, 
        'PKWY': 8,
        'PL': 9,
        'RD': 10,
        'ST': 11,
        'TERR': 12,
        'TRFY': 13,
        'WAY': 14           
    }
    
    def __init__(self):
        """
        init QT app
        """
        # setup UI
        self.ui = Ui_MainWindow()
        
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.ui.setupUi(self)
        
        
        # init controls and signals
        self.connect(self.ui.process_button, QtCore.SIGNAL("clicked()"), self.process_addresses)
        self.connect(self.ui.reset_button, QtCore.SIGNAL("clicked()"), self.reset)
        self.connect(self.ui.quit_button, QtCore.SIGNAL("clicked()"), self.quit)
        
        self.connect(self, SIGNAL("moveToNextAddress()"), self.next)
        
        # show
        self.show()
        
        
    def quit(self):
        """
        sys exit
        """
        
        print "in quit"
        sys.exit()
        
    
    def u2str(self, charz):
        """
        converts unicode to str
        """
        
        return unicodedata.normalize('NFKD', charz).encode('ascii','ignore')
    
    
    def next(self):
        """
        """
        
        print "in next: ", self.address_to_process_index, len(self.addresses)
        
        if(self.address_to_process_index < len(self.addresses)): 
            # call next address
            self.address_to_process_index += 1
            
            print "address index is less than number of addresses so we are going to run process_address with index being set to ", self.address_to_process_index
            
            
            self.process_addresses()
            
            print "we have returned from process_addresses() into next() and will return again"
              
            
        else:
            
            
            return
    
    
    def scrape_data(self):
        """
        scrapes data 
        """
        
        print " IN SCRAPE DATA ", self.address_to_search, self.address_to_process_index
        self.disconnect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.scrape_data)
        
        htmlstr = str(self.ui.web_view.page().currentFrame().toHtml())
        soup = BeautifulSoup(htmlstr, "html.parser")
        
        # col2&3
        try:
            full_name = self.u2str(soup.find('body').findAll('table')[1].findAll('tr')[5].findAll('td')[1].text).strip()

            self.last_name = full_name.split(" ")[0]
            self.first_name = " ".join(full_name.split(" ")[1:])
            
            print "last name", self.last_name
            print "fist name", self.first_name
            
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
            self.last_name = ""
            self.first_name = ""
        
        # col4
        try:
            self.mail_address = self.u2str(soup.find('body').findAll('table')[1].findAll('tr')[7].findAll('td')[0].text).strip()
            
            print "mail address, ", self.mail_address
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
            self.mail_address = ""
        
        
        # col 5, 6, & 7
        try:
            _data = self.u2str(soup.find('body').findAll('table')[1].findAll('tr')[8].findAll('td')[0].text).split(" ")
            
            self.mail_city = " ".join(_data[:len(_data) - 2])
            self.mail_state = str(_data[-2]).strip()
            self.mail_zip = str(_data[-1]).strip()
            
            print "_data for city: ", _data
            print "city: ", self.mail_city
            print "state: ", self.mail_state
            print "zip: ", self.mail_zip
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
            self.mail_address = "";
            self.mail_state = "";
            self.mail_zip = "";
            
            
        self.report_csv += str(self.address_to_search) + ", "
        self.report_csv += str(self.first_name) + ", "
        self.report_csv += str(self.last_name) + ", "
        self.report_csv += str(self.mail_address) + ", "
        self.report_csv += str(self.mail_city) + ", "
        self.report_csv += str(self.mail_state) + ", "
        self.report_csv += str(self.mail_zip) + "\n"
        
        if(self.hard_stop == False):
            report_text = self.ui.result_box.toPlainText()
            report_text += " Processed \n"
            self.ui.result_box.setText(report_text)
        
        
        self.emit(SIGNAL("moveToNextAddress()"))
         

        
        
    def click_link(self):
        """
        clicks the link
        """
        print " IN CLICK LINK: ", self.address_to_search, self.address_to_process_index
        self.disconnect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.click_link)
        
        
        htmlstr = str(self.ui.web_view.page().currentFrame().toHtml())
        soup = BeautifulSoup(htmlstr, "html.parser")
        
        try:
            link = self.u2str(soup.find('body').findAll('table')[2].findAll('tr')[1].findAll('td')[0].text).strip()
            
            if(link):
        
                doc = self.ui.web_view.page().currentFrame().documentElement()
                self.connect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.scrape_data)
                doc.evaluateJavaScript("location.href = document.getElementsByTagName('table')[2].getElementsByTagName('tr')[1].getElementsByTagName('td')[0].getElementsByTagName('a')[0].href")
                
            else:
                
                self.emit(SIGNAL("moveToNextAddress()"))
                
        except Exception, e:
            
            report_text = self.ui.result_box.toPlainText()
            report_text += " Not Found \n"
            self.ui.result_box.setText(report_text)
            
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
            self.emit(SIGNAL("moveToNextAddress()"))
            
        
        
    
    def submit_form(self):
        """
        fills and submits form
        """
        
        print " IN SUBMIT FORM", self.address_to_search, self.address_to_process_index
        
        self.disconnect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.submit_form)
        
        
        invalid_address = False
        
        #if(self.hard_stop == False):
        report_string = str((self.address_to_process_index + 1)) + ": " + self.address_to_search + " ... "
        print report_string + "\n"
        
        report_text = self.ui.result_box.toPlainText()
        report_text += "\n" + report_string
        self.ui.result_box.setText(report_text)
        
        #else:
        #    return
            
        
        
        doc = self.ui.web_view.page().currentFrame().documentElement()
        parsed_address = self.address_to_search.split(" ")
        
        no = ""
        direction = ""
        strt_name = ""
        #strt_type = ""
        if(len(parsed_address) > 3):
            no = parsed_address[0]
            direction = str(parsed_address[1])
            strt_name = str(parsed_address[2])
            #strt_type = str(parsed_address[3])
            
        elif(len(parsed_address) == 3):
            no = str(parsed_address[0])
            strt_name = str(parsed_address[1])
            #strt_type = str(parsed_address[2])
            
        else:
            invalid_address = True
            
            
        """    
            report_text = self.ui.result_box.toPlainText()
            report_text += " Not Found 1 \n"
            self.ui.result_box.setText(report_text)
            
            print " address could not be processed, moving to next address "
            self.disconnect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.submit_form)
            self.emit(SIGNAL("moveToNextAddress()"))
        """
            
        
        if(not str(no).isdigit()):
            invalid_address = True
        
        """
            report_text = self.ui.result_box.toPlainText()
            report_text += " Not Found 2 \n"
            self.ui.result_box.setText(report_text)
            
            print " first part of address must be numeric. address will not be processed. moving to next address "
            self.disconnect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.submit_form)
            self.emit(SIGNAL("moveToNextAddress()"))
        """
        
        
        
        web_address_number_box = doc.findFirst("input[name='strNo']")
        web_address_number_box.setAttribute('value', no)
        
        web_address_name_box = doc.findFirst("input[name='strNm']")
        web_address_name_box.setAttribute('value', strt_name)
        
        
        try:
            if(len(direction) > 0):
                option = doc.findFirst("select[name='strPref'] > option[value='" + direction + "']")
                option.setAttribute('selected', 'true')
                select = doc.findFirst("select[name='strPref']")
                select.evaluateJavaScript('this.selectedIndex = ' + str(self.direction_types[direction]))
        except:
            invalid_address = True
            
        """    
        option = doc.findFirst("select[name='strType'] > option[value='" + strt_type + "']")
        option.setAttribute('selected', 'true')
        select = doc.findFirst("select[name='strType']")
        select.evaluateJavaScript('this.selectedIndex = ' + str(self.street_types[strt_type]))
        """
          
        """  
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            
            report_text = self.ui.result_box.toPlainText()
            report_text += " Address could not be parsed \n"
            self.ui.result_box.setText(report_text)
            
            print " address could not be processed, moving to next address "
            
            self.emit(SIGNAL("moveToNextAddress()"))
        """
            
        
        
        if(not invalid_address):
            
            print " we have returned from next() into submit_form() with index being ", self.address_to_process_index, " and address being ", self.address_to_search, " and we return to load() "
            self.connect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.click_link)
            doc.evaluateJavaScript("document.form1.submit();")
            
        else:
            
            report_text = self.ui.result_box.toPlainText()
            report_text += " Not Found \n"
            self.ui.result_box.setText(report_text)
            
            print " first part of address must be numeric. address will not be processed. moving to next address "
            self.emit(SIGNAL("moveToNextAddress()"))
            
        
        
        
        
        
    def update_status(self, status):
        """
        updates status box
        """
        
        pass
        
            
    def file_save(self):
        """
        save file dialog
        """
        
        
        if(len(self.report_csv) > 0):
            
            
            try:
                self.report_csv = self.report_header + "\n" + self.report_csv 
                
                name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
                file = open(name,'w')
                file.write(self.report_csv)
                file.close()
    
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
            
        
            self.report_csv = ""
            self.address_to_process_index = 0
            self.address_to_search = ""
            self.disconnect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.submit_form)
            self.hard_stop = True
            
            
    
    
    def showdialog(self, message_txt, window_title):
        """
        pass
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
    
        msg.setText(message_txt)
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle(window_title)
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #msg.buttonClicked.connect(msgbtn)
        
        retval = msg.exec_()
        print "value of pressed message box button:", retval
        
        
    def validate_address_input(self, address_str):
        """
        parses address input
        """
        rtn = address_str.split("\n")
        
        rtn = [str(x) for x in rtn if x]
        
        return rtn
    
    
      
    def load(self):
        """
        do the load and call fil_form
        """
        
        if(self.address_to_process_index == 0):
            self.ui.result_box.setText("")
        
        print " we are in load with index being ", self.address_to_process_index, " ad address being ", self.address_to_search, " and we are going t call submit_form() "
        
        url = "https://hosturl/realEstate.jsp" 
        self.ui.web_view.load(QUrl(url))
        self.connect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.submit_form)
        
        print " we are in load with index being ", self.address_to_process_index, " ad address being ", self.address_to_search, " and we are returning from load "
        
        
       
        
        
    
    def process_addresses(self):
        """
        processes addresses
        """
        
        self.addresses = self.validate_address_input(self.ui.address_box.toPlainText())
        
        
        self.ui.process_button.setEnabled(False)
        self.ui.reset_button.setEnabled(False)
        
        if(self.hard_stop == False):
            
            if(len(self.addresses) > 0 and len(self.addresses[0]) > 0):
            
                if(self.address_to_process_index == len(self.addresses)):
                    
                    # DEBUG
                    self.file_save()
                    
                    print "we are now returning because the file was saved and load will not be called again"
                    
                    
                    self.report_csv = ""
                    self.address_to_process_index = 0
                    self.address_to_search = ""
                    self.disconnect(self.ui.web_view, QtCore.SIGNAL("loadFinished(bool)"), self.submit_form)
        
        
                    self.ui.reset_button.setEnabled(True)
                    
                    return
                
                else:
                    
                    print "we are in process_addreess and going to call load with ", self.address_to_process_index
                    
                    self.address_to_search = str(self.addresses[self.address_to_process_index]).strip()
                    
                    if(len(self.address_to_search) > 0):
                        self.load()
                    
                        print " we have returned from load() "
                    
                    else:
                        
                        self.emit(SIGNAL("moveToNextAddress()"))
            
        
        
                
    def reset(self):
        """
        """
        
        print "in reset"

        self.ui.result_box.setText("")
        self.ui.address_box.setText("")
        
        self.report_csv = ""
        self.address_to_process_index = 0
        self.address_to_search = ""
        
        self.ui.process_button.setEnabled(True)
        
        self.hard_stop = False
            

def resource_path(relative_path):
     if hasattr(sys, '_MEIPASS'):
         return os.path.join(sys._MEIPASS, relative_path)
     return os.path.join(os.path.abspath("."), relative_path)
     
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = AddressScraper()
    window.show()
    sys.exit(app.exec_())

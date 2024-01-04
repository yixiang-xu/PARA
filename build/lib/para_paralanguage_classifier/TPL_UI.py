#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Changes for version 0.1 - first row header, txt/xlsx, status bar, multiple column analysis without reload.
import csv
import os
import sys
import json
from TPL_Int_Score import TPL_Int_Score
import traceback
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import concurrent.futures
#from icon_fix import images
import warnings
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
warnings.simplefilter(action='ignore')
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()


class TPL_Result(QtCore.QObject):
    def __init__(self, result):
        QtCore.QObject.__init__(self)
        self.results = result
        
class ThreadProcess(QThread):
    """
    Runs a counter thread.
    """
    countChanged = pyqtSignal(int)
    results = QtCore.pyqtSignal(object)
    
    def __init__(self, texts, application_path, support_file_ls, brown_dict):
        QThread.__init__(self)
        self.texts = texts
        self.application_path = application_path
        self.support_file_ls =  support_file_ls
        self.brown_dict = brown_dict
        
    def run(self):
        scores = []
        n = len(self.texts)
        self.PARA = TPL_Int_Score(self.application_path + self.support_file_ls[0], self.application_path + self.support_file_ls[1],\
                                    self.application_path + self.support_file_ls[2], self.application_path + self.support_file_ls[3],\
                                        self.application_path + self.support_file_ls[4], self.application_path + self.support_file_ls[5],\
                                            self.application_path + self.support_file_ls[6], self.application_path + self.support_file_ls[7],\
                                    self.brown_dict)

        
        count = 0
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for i in executor.map(self.PARA.run, self.texts):
                scores.append(i)
                count += 1            
                progress_num = int((count/n) * 100)            
                self.countChanged.emit(progress_num)
        self.results.emit(TPL_Result(scores))
        #return scores

def base_path():
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return sys._MEIPASS
    except Exception:
        return os.path.abspath(".")
            
class TPL_GUI(QtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(TPL_GUI, self).__init__(parent)
        self.application_path = base_path()
        self.support_path = "/TPL_support_files/"
        self.support_file_ls = ["Keyword List_Without Symbol.xlsx", "Excluded Acronyms.xlsx","Keyword List_With Symbol.xlsx", "cursing_lexicon.txt", \
                                    "emoticon_a.txt", "emoticon_vk.txt", "emoticon_tk.txt","Emoji Dictionary.xlsx"]
        self.user_settings_file = 'user_config.json'        
        self.brown_corpus = "brown.json" # Pre-downloaded this file from NLTK to package with software. 
        self.fileName = None
        self.dataRows = 0
        self.dataColumns = 0
        # Need to update with new logo later on
        self.setWindowIcon(QIcon(self.application_path + self.support_path + 'icon.ico'))
        self.setting = Settings(self)
        self.setting.resize(350,350)        
        self.info = Info(self)
        self.info.resize(350,350) 

        self.help = Help(self)
        self.help.resize(600,350) 
        
        self.result_variable_index = {'Pitch': 0, 'Rhythm': 1, 'Stress': 2, 'Emphasis': 3, 'Tempo': 4, 'Volume': 5, 'Censorship': 6, 'Spelling': 7, 'Alternant': 8, 'Differentiator': 9, 'Alphahaptics': 10, 'Alphakinesics': 11, 'Formatting': 12, 'Tactile_Emoticon': 13, 'Bodily_Emoticon': 14, 'Nonbodily_Emoticon': 15, 'Tactile_Emoji': 16, 'Bodily_Emoji': 17, 'Nonbodily_Emoji': 18, 'Emoji_Count': 19, 'Emoji_Index': 20, 'Emoticon_Index': 21, 'TPL_Index':22}
    
        
        
        # Building Toolbars
        toolbar = QtWidgets.QToolBar()
        
        
        settingsAct = QtWidgets.QAction(QIcon(self.application_path + self.support_path + 'settings.png'), 'Settings', self)        
        settingsAct.triggered.connect(self.adjustSettings)        
        toolbar.addAction(settingsAct)
        
        helpAct = QtWidgets.QAction(QIcon(self.application_path + self.support_path + 'help.png'), 'Help', self)        
        helpAct.triggered.connect(self.showHelp)        
        toolbar.addAction(helpAct)
        
        infoAct = QtWidgets.QAction(QIcon(self.application_path + self.support_path + 'info.png'), 'Information', self)        
        infoAct.triggered.connect(self.showInfo)        
        toolbar.addAction(infoAct)
        
        try:
            with open(self.application_path + self.support_path + self.brown_corpus, "r") as inp_file:
                self.brown_dict = set(json.load(inp_file)["Brown Corpus"])
        except Exception as e:
            print(e)
            
        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)

        self.pushButtonLoad = QtWidgets.QPushButton(self)
        self.pushButtonLoad.setText("Upload File")
        self.pushButtonLoad.clicked.connect(self.on_pushButtonLoad_clicked)

        self.pushButtonAnalyze = QtWidgets.QPushButton(self)
        self.pushButtonAnalyze.setText("Analyze")
        self.pushButtonAnalyze.clicked.connect(self.on_pushButtonAnalyze_clicked)
        self.pushButtonAnalyze.setEnabled(False)
        
        self.pushButtonWrite = QtWidgets.QPushButton(self)
        self.pushButtonWrite.setText("Save Results")
        self.pushButtonWrite.clicked.connect(self.on_pushButtonWrite_clicked)
        self.pushButtonWrite.setEnabled(False)
        self.firstRowHeaderCB = QtWidgets.QCheckBox('First row is header', self)
        #self.firstRowHeaderCB.toggle()
        self.firstRowHeader = False
        self.firstRowHeaderCB.stateChanged.connect(self.setFirstRowHeader)
        self.firstRowHeaderCB.setEnabled(False)
        
        self.pbar = QtWidgets.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setHidden(True)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.tableView)
        self.layoutVertical.addWidget(self.pbar)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addWidget(self.pushButtonLoad)
        self.buttonLayout.addWidget(self.pushButtonAnalyze)
        self.buttonLayout.addWidget(self.pushButtonWrite)
        self.layoutVertical.addLayout(self.buttonLayout)
        self.cbLayout = QtWidgets.QHBoxLayout()
        self.cbLayout.addWidget(self.firstRowHeaderCB)
        self.layoutVertical.addLayout(self.cbLayout)        
        self.layoutVertical.setMenuBar(toolbar)
        self.statusBar = QtWidgets.QStatusBar()
        self.layoutVertical.addWidget(self.statusBar)
        self.statusBar.setStyleSheet("QStatusBar{padding-left:8px;color:blue;font-weight:bold;}")
        self.statusBar.showMessage('Status: Waiting for file upload.')

    @QtCore.pyqtSlot()    
    def showHelp(self):
        self.help.show()
    
    @QtCore.pyqtSlot()    
    def showInfo(self):
        self.info.show()
        
    @QtCore.pyqtSlot()    
    def adjustSettings(self):
        # set current setting as previous before making changes
        self.previous_position = {self.setting.result_variable_order[ix]: ix + self.dataColumns for ix in range(len(self.setting.result_variable_order))}        
        self.setting.show()
        
    
    def setFirstRowHeader(self, state):        
        try:    
            if state > 0:
                self.firstRowHeader = True
                firstRowItems = self.model.takeRow(0)
                for header_ix in range(len(firstRowItems)):
                    if firstRowItems[header_ix] is None:
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Critical)
                        msg.setText("Error")
                        msg.setInformativeText('First row has a blank cell. It cannot be made as header.')
                        msg.setWindowTitle("Error")
                        msg.exec_()
                        return
                header = []        
                for header_ix in range(len(firstRowItems)):
                    self.model.setHorizontalHeaderItem(header_ix,firstRowItems[header_ix])
                    header.append(firstRowItems[header_ix].text())
                self.dataHeader = header
                self.headerItems = firstRowItems
            else:
                self.firstRowHeader = False
                if self.dataHeader is not None:                
                    self.model.insertRow(0,[QtGui.QStandardItem(i) for i in self.dataHeader])
                    header = []
                    newHeaderItems = [QtGui.QStandardItem(str(i + 1)) for i in range(len(self.headerItems))]
                    for header_ix in range(len(newHeaderItems)):
                        self.model.setHorizontalHeaderItem(header_ix,newHeaderItems[header_ix])
                        header.append(newHeaderItems[header_ix].text())
                    self.dataHeader = header
                    self.headerItems = newHeaderItems
        except Exception as e:
            print(e)
    
    def loadFile(self, fileName):        
        if fileName == None or len(str(fileName).strip()) == 0:
            return
        
        if not(fileName.endswith('.csv') or fileName.endswith('.xlsx') or fileName.endswith('.xls') or fileName.endswith('.txt')):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Unsupported file format. Please select csv, txt or xlsx formats')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        self.model.clear()
        self.fileName = fileName
        if self.firstRowHeader:
            self.dataHeader = None
            self.firstRowHeaderCB.toggle()
        if fileName.endswith('.csv'):
            self.loadCsv(fileName)
        elif fileName.endswith('.xlsx') or fileName.endswith('.xls'):
            self.loadExcel(fileName)
        elif fileName.endswith('.txt'):
            self.loadTxt(fileName)
        
            
        self.dataRows = self.model.rowCount()
        self.dataColumns = self.model.columnCount()
        self.pushButtonAnalyze.setEnabled(True)
        self.pushButtonWrite.setEnabled(False)
        self.statusBar.setStyleSheet("QStatusBar{padding-left:8px;color:blue;font-weight:bold;}")
        self.firstRowHeaderCB.setEnabled(True)
        self.statusBar.showMessage('Status: Select a column and click analyze.')
        
    def loadCsv(self, fileName):
        with open(fileName, "r", encoding="utf-8-sig",errors="replace") as fileInput:#adding errors replace to ignore unicode error.
            for row in csv.reader(fileInput):                  
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]            
                self.model.appendRow(items)        
    
    def loadTxt(self, fileName):
        with open(fileName, "r", encoding="utf-8-sig",errors="replace") as fileInput:
            line = fileInput.readline()            
            while line:
                self.model.appendRow([QtGui.QStandardItem(line.strip())])
                line = fileInput.readline()
                

    def loadExcel(self, fileName):
        df = pd.read_excel(fileName, index_col=None,header=None)
        df = df.applymap(str)
        for ix,row in df.iterrows():
            try:
                items = [
                    QtGui.QStandardItem(field.strip())
                    for field in row
                ]    
            except AttributeError:
            # data is not a string, cannot strip
                items = [
                    QtGui.QStandardItem(field)
                    for field in row
                ]        
            self.model.appendRow(items) 
        
    def writeCsv(self, fileName):
        fn = fileName.split('.')
        fn = fn[0] + '_Column_' + str(self.analyzed_column + 1)+'_TPL_Resuts.csv'
        is_hidden_column = {columnNumber:self.tableView.isColumnHidden(columnNumber) for columnNumber in range(self.model.columnCount())}
        try:
            with open(fn, "w", encoding="utf-8-sig", errors='replace',newline='') as fileOutput:
                writer = csv.writer(fileOutput)
                fields = []
                if self.firstRowHeader:
                    for item in self.dataHeader:
                        fields.append(item)
                else:
                    for item in range(self.model.columnCount() - len(self.setting.result_variable_order)):
                        fields.append('')

                for item in self.setting.result_variable_order:
                    if self.setting.result_settings[item] != 0:
                        fields.append(item)

                writer.writerow(fields)
                for rowNumber in range(self.model.rowCount()):
                    fields = []
                    for columnNumber in range(self.model.columnCount()):
                        if not is_hidden_column[columnNumber]:
                            fields.append(self.model.data(
                                self.model.index(rowNumber, columnNumber),
                            QtCore.Qt.DisplayRole
                        ))
                    #print(fields)
                    writer.writerow(fields)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Success!")
            msg.setInformativeText('Results saved to:' + fn)
            msg.setWindowTitle("Info")
            msg.exec_()
            self.statusBar.setStyleSheet("QStatusBar{padding-left:8px;color:blue;font-weight:bold;}")
            self.statusBar.showMessage('Status: Results saved. Select a column or load another file for analysis.')
            self.pushButtonAnalyze.setEnabled(True)
        except Exception as e:
            #print(e)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('File: ' + fn + ' is accessed by another application. ')
            msg.setWindowTitle("Error")
            msg.exec_()
            
        

    def do_TPL(self):        
        
        indexes = self.tableView.selectionModel().selectedColumns()
        mdl = indexes[0]
        selected_column = indexes[0].column()
        
        texts = [self.model.data(self.model.index(rowNumber, selected_column),
                        QtCore.Qt.DisplayRole
                        )
                    for rowNumber in range(self.model.rowCount())
                ]
        
        self.analyzed_column = selected_column
        self.calc = ThreadProcess(texts, self.application_path + self.support_path, self.support_file_ls, self.brown_dict)
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.results.connect(self.show_results)
        self.calc.start()
        

    def onCountChanged(self, value):
        self.pbar.setValue(value)
        if value == 100:
            self.pbar.setHidden(True)
            self.pushButtonWrite.setEnabled(True)
            self.pushButtonAnalyze.setEnabled(True)
            
    def show_results(self,result):
        analyzed_res = result.results
        
        if len(analyzed_res) == 0:
            return
        self.result = result # storing this for change of order from settings - not use here
        ix = 0
        #for var in self.result_variable_order:
        #    if result_settings[var] == 1:
        #        self.model.setHorizontalHeaderItem(self.dataRows + ix,QtGui.QStandardItem(var))
        #        ix += 1
        #        var_result = [QtGui.QStandardItem(item[result_variable_index[var]]) for item in analyzed_res]
        
        result_columns = []
        
        items_in_analyzed_res = []
        for item in analyzed_res:
            if len(item) > 0:
                items_in_analyzed_res = item
                break
        for ix in items_in_analyzed_res:# Getting first item that had result and skipping blank rows.
            result_columns.append([])
        
        for item in analyzed_res:
            if len(item) > 0:
                for ix in range(len(item)): 
                    s = str(item[ix])
                    if '.' in s:
                        s = s[:s.index('.')+5] # limiting to 4 digits after decimal
                    result_columns[ix].append(QtGui.QStandardItem(s))
            else:# display empty cell for blank rows
                for ix in range(len(items_in_analyzed_res)):
                    result_columns[ix].append(QtGui.QStandardItem(''))
        
        for col in result_columns:
            self.model.appendColumn(col)
        
        headers = sorted(self.result_variable_index, key=self.result_variable_index.get)
        
        ix = 0
        for item in headers:            
            self.model.setHorizontalHeaderItem(self.dataColumns + ix,QtGui.QStandardItem(item))
            ix += 1
        
                
        self.previous_position = {item:self.result_variable_index[item] + self.dataColumns for item in self.result_variable_index}
        self.refresh_results()
        self.statusBar.setStyleSheet("QStatusBar{padding-left:8px;color:green;font-weight:bold;}")
        self.statusBar.showMessage('Status: Analysis completed.')
        
    
    def refresh_results(self):
        var_col_position = self.previous_position#{item:self.result_variable_index[item] + self.dataColumns for item in self.result_variable_index}
        required_position = {self.setting.result_variable_order[ix]: ix + self.dataColumns for ix in range(len(self.setting.result_variable_order))}
        horizontal_header = self.tableView.horizontalHeader()
        
        for item in required_position:
            
            if var_col_position[item] != required_position[item]:
                
                for key, value in var_col_position.items(): 
                    if required_position[item] == value: 
                         temp_ix = key
                         break                                                
                horizontal_header.swapSections(var_col_position[item],required_position[item])
                var_col_position[temp_ix] = var_col_position[item]
                var_col_position[item] = required_position[item]
        
        
        #print(required_position)
        #print(self.setting.result_settings)
        for item in required_position:
            if self.setting.result_settings[item] == 0:
                self.tableView.setColumnHidden(required_position[item], True)
            else:                
                self.tableView.setColumnHidden(required_position[item], False)
            
    
    @QtCore.pyqtSlot()
    def on_pushButtonAnalyze_clicked(self):
        try:  
            indexes = self.tableView.selectionModel().selectedColumns()
            if len(indexes)!= 1:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('Select one column to analyze!')
                msg.setWindowTitle("Error")
                msg.exec_()         
            else:
                result_selected = False
                for ix in indexes:
                    if ix.column() >= self.dataColumns:
                        result_selected = True
                        break
                
                if result_selected:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText("Error")
                    msg.setInformativeText('Select a column that is part of data to analyze.')
                    msg.setWindowTitle("Error")
                    msg.exec_()
                else:
                    while self.model.columnCount() > self.dataColumns:
                        self.model.removeColumn(self.model.columnCount()-1)    
                    
                    
                    self.pbar.setHidden(False)
                    self.pushButtonAnalyze.setEnabled(False)
                    self.statusBar.setStyleSheet("QStatusBar{padding-left:8px;color:blue;font-weight:bold;}")
                    self.statusBar.showMessage('Status: Processing...')                
                    self.do_TPL()
                    self.firstRowHeaderCB.setEnabled(False)
        except Exception as e:
                print(e)
            
    
    @QtCore.pyqtSlot()
    def on_pushButtonWrite_clicked(self):
        self.writeCsv(self.fileName)

    @QtCore.pyqtSlot()
    def on_pushButtonLoad_clicked(self):
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath() , 'Comma seperated values (*.csv);;Text files - one entry per line (*.txt);;Excel with one sheet(*.xlsx *.xls)')
        self.loadFile(self.fileName)

class Help(QtWidgets.QWidget):
    def __init__(self, main_window, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.main_window = main_window
        self.info_layout = QtWidgets.QVBoxLayout()
        
        self.textArea = QtWidgets.QTextEdit()
        self.cursor = QtGui.QTextCursor(self.textArea.document())
        with open(main_window.application_path + main_window.support_path + 'help.html', "rb") as inp_file:
            help = inp_file.read()
            self.cursor.insertHtml(help.decode())
        self.info_layout.addWidget(self.textArea)
        self.setLayout(self.info_layout)

class Info(QtWidgets.QWidget):
    def __init__(self, main_window, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.main_window = main_window
        self.info_layout = QtWidgets.QVBoxLayout()
        
        self.textArea = QtWidgets.QTextEdit()
        self.cursor = QtGui.QTextCursor(self.textArea.document())
        with open(main_window.application_path + main_window.support_path + 'tpl_overview.html', "rb") as inp_file:
            ov = inp_file.read()
            self.cursor.insertHtml(ov.decode())
        self.info_layout.addWidget(self.textArea)
        self.setLayout(self.info_layout)
        self.textArea.moveCursor(QtGui.QTextCursor.Start)
        self.textArea.ensureCursorVisible()

class Settings(QtWidgets.QWidget):
    """Class to customize settings"""
    def __init__(self, main_window, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.main_window = main_window
        self.widget_layout = QtWidgets.QVBoxLayout()
        try:
            with open('user_settings.json','r') as fp:
                setting = json.load(fp)
            self.result_settings = setting['selected']
            self.result_variable_order = setting['order']
        except Exception as e:
            #print(e)
            #print('Initializing default')
            self.result_settings = {'Pitch': 1, 'Rhythm': 1, 'Stress': 1, 'Emphasis': 1, 'Tempo': 1, 'Volume': 1, 'Censorship': 1, 'Spelling': 1, 'Alternant': 1, 'Differentiator': 1, 'Alphahaptics': 1, 'Alphakinesics': 1, 'Formatting': 1, 'Tactile_Emoticon': 1, 'Bodily_Emoticon': 1, 'Nonbodily_Emoticon': 1, 'Tactile_Emoji': 1, 'Bodily_Emoji': 1, 'Nonbodily_Emoji': 1, 'Emoji_Count': 1, 'Emoji_Index': 1, 'Emoticon_Index': 1, 'TPL_Index':1}
            self.result_variable_order = ['Pitch', 'Rhythm', 'Stress', 'Emphasis', 'Tempo', 'Volume', 'Censorship', 'Spelling', 'Alternant', 'Differentiator', 'Alphahaptics', 'Alphakinesics', 'Formatting', 'Tactile_Emoticon', 'Bodily_Emoticon', 'Nonbodily_Emoticon', 'Tactile_Emoji', 'Bodily_Emoji', 'Nonbodily_Emoji', 'Emoji_Count', 'Emoji_Index', 'Emoticon_Index', 'TPL_Index']
        # Create ListWidget and add 10 items to move around.
        self.list_widget = QtWidgets.QListWidget()
        for i in self.result_variable_order:
            item = QtWidgets.QListWidgetItem()
            item.setText(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if self.result_settings[i] == 0:
                item.setCheckState(QtCore.Qt.Unchecked)
            else:
                item.setCheckState(QtCore.Qt.Checked)
            self.list_widget.addItem(item)

        # Enable drag & drop ordering of items.
        self.list_widget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        
        self.pushButtonSelectAll = QtWidgets.QPushButton(self)
        self.pushButtonSelectAll.setText("Select All")
        self.pushButtonSelectAll.clicked.connect(self.on_pushButtonSelectAll_clicked)
        
        self.pushButtonUnSelectAll = QtWidgets.QPushButton(self)
        self.pushButtonUnSelectAll.setText("Unselect All")
        self.pushButtonUnSelectAll.clicked.connect(self.on_pushButtonUnSelectAll_clicked)
        
        self.pushButtonSave = QtWidgets.QPushButton(self)
        self.pushButtonSave.setText("Update Settings")
        self.pushButtonSave.clicked.connect(self.on_pushButtonSave_clicked)
        
        self.pushButtonCancel = QtWidgets.QPushButton(self)
        self.pushButtonCancel.setText("Cancel")
        self.pushButtonCancel.clicked.connect(self.on_pushButtonCancel_clicked)
        
        self.widget_layout.addWidget(self.list_widget)
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addWidget(self.pushButtonSelectAll)
        self.buttonLayout.addWidget(self.pushButtonUnSelectAll)
        self.buttonLayout.addWidget(self.pushButtonSave)
        self.buttonLayout.addWidget(self.pushButtonCancel)
        self.note_text = QtWidgets.QTextEdit()
        self.note_text.setText("Note: Drag and drop to rearrange order.")
        self.note_text.setDisabled(True)
        self.note_text.setMaximumSize(320,30)
        self.note_text.setFrameStyle(QtWidgets.QFrame.NoFrame)
        #self.note_text.setStyleSheet("background-color: gray")
        self.widget_layout.addWidget(self.note_text)
        self.widget_layout.addLayout(self.buttonLayout)
        self.setLayout(self.widget_layout)

    @QtCore.pyqtSlot()
    def on_pushButtonSelectAll_clicked(self):        
        for ix in self.result_settings:
            items = self.list_widget.findItems(ix, QtCore.Qt.MatchRegExp)            
            for item in items:                
                item.setCheckState(QtCore.Qt.Checked)
        
        
    @QtCore.pyqtSlot()
    def on_pushButtonUnSelectAll_clicked(self):
        for ix in self.result_settings:
            items = self.list_widget.findItems(ix, QtCore.Qt.MatchRegExp)            
            for item in items:
                item.setCheckState(QtCore.Qt.Unchecked)
    
    @QtCore.pyqtSlot()
    def on_pushButtonCancel_clicked(self):
        self.hide()
        
    @QtCore.pyqtSlot()
    def on_pushButtonSave_clicked(self):
        new_result_settings = {}# To store the order temprorily
        new_result_selected = {}# To store the current selection
        for ix in self.result_settings:
            items = self.list_widget.findItems(ix, QtCore.Qt.MatchRegExp)            
            for item in items:                
                new_result_settings[item.text()] = self.list_widget.indexFromItem(item).row()
                new_result_selected[item.text()] = 1 if item.checkState() else 0
        new_result_order = sorted(new_result_settings, key=new_result_settings.get)
        self.result_settings = new_result_selected
        self.result_variable_order = new_result_order
        try:
            with open('user_settings.json','w') as fp:
                json.dump({'selected':new_result_selected,'order':new_result_order}, fp)
            
        except Exception as e:
            print(e)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Failed to save results to user settings!')
            msg.setWindowTitle("Error")
            msg.exec_() 
        self.main_window.refresh_results()
        self.main_window.statusBar.setStyleSheet("QStatusBar{padding-left:8px;color:green;font-weight:bold;}")
        self.main_window.statusBar.showMessage('Status: Settings updated sucessfully.')
        self.hide()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Textual Paralanguage (TPL) Classifier')

    main = TPL_GUI()
    main.resize(800,540)
    main.show()

    sys.exit(app.exec_())
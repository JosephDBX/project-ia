from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.Qt import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QToolBar, QAction, QWidget, QFileDialog

import pandas as pd

from models.icon import Icon
from models.genericconnect import GenericConnect

Ui_MainWindow, QBaseClass = uic.loadUiType('./views/mainwindow.ui')

from .home import Home
from .analytics import Analytics

from .databasedialogcontroller import DatabaseDialogController

class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        #self.setStyleSheet('background-color: #05A; color: #FFF;')
        #self.TabContainer.setStyleSheet('background-color: #05A; color: #FFF;')

        # Load Widgets
        self.home = Home(self.onLoadCSV, self.onLoadDB)

        # ToolBar & Tabs
        self.setup()

    def setCurrentTab(self, widget: QWidget):
        self.TabContainer.setCurrentWidget(widget)

    def closeTab(self, currentIndex):
        currentWidget = self.TabContainer.widget(currentIndex)
        currentWidget.deleteLater()
        self.TabContainer.removeTab(currentIndex)

    def setup(self):
        # icons
        self.homeIcon = Icon('home.svg', '#0A0').getIcon()
        self.csvIcon = Icon('file-csv.svg', '#D50').getIcon()
        self.dbIcon = Icon('database.svg', '#666').getIcon()

        # Setup ToolBar
        toolBar = QToolBar('Left Menu', self)
        toolBar.setFloatable(False)
        toolBar.setMovable(False)
        toolBar.setIconSize(QSize(64, 64))
        toolBar.setStyleSheet('background-color: #004; color: #FFF;')

        # Tabs Properties
        self.TabContainer.setTabsClosable(True)
        self.TabContainer.tabCloseRequested.connect(self.closeTab)
        
        # Home
        home = QAction(self.homeIcon, 'Home', self)
        home.triggered.connect(self.onHome)
        self.TabContainer.addTab(self.home, self.homeIcon, 'Home')

        # CSV
        loadCSV = QAction(self.csvIcon, 'Load CSV', self)
        loadCSV.triggered.connect(self.onLoadCSV)

        # DB
        loadDB = QAction(self.dbIcon, 'Load From DataBase', self)
        loadDB.triggered.connect(self.onLoadDB)

        # Add to ToolBar
        toolBar.addAction(home)
        toolBar.addAction(loadCSV)
        toolBar.addAction(loadDB)
        self.addToolBar(Qt.LeftToolBarArea, toolBar)

    def onHome(self):
        try:
            self.setCurrentTab(self.home)
        except:
            self.home = Home(self.onLoadCSV, self.onLoadDB)
            self.TabContainer.addTab(self.home, self.homeIcon, 'Home')
            self.setCurrentTab(self.home)

    def onLoadCSV(self):
        try:
            self.setCurrentTab(self.analytics)
        except:
            path = QFileDialog.getOpenFileName(self, 'Open CSV', '', 'CSV(*.csv)')
            if path[0] != '':
                df:pd.DataFrame = pd.read_csv(path[0])
                self.analytics = Analytics(df, path[0])
                self.TabContainer.addTab(self.analytics, self.csvIcon, 'Analytics CSV')
                self.setCurrentTab(self.analytics)

    def onLoadDB(self):
        try:
            self.setCurrentTab(self.analyticsDB)
        except:
            dialog = DatabaseDialogController(self, self.onConnect)
            dialog.exec_()

    def onConnect(self, DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE, CHARSET, TABLE_NAME, QUERY, STATE):
        connect = GenericConnect(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE, CHARSET)
        title = ''
        if STATE:
            df:pd.DataFrame = connect.getTableDataFrame(TABLE_NAME)
            title = 'Table={}'.format(TABLE_NAME)
        else:
            df:pd.DataFrame = connect.getQueryDataFrame(QUERY)
            title = QUERY
        if not df.empty:
            self.analyticsDB = Analytics(df, title)
            self.TabContainer.addTab(self.analyticsDB, self.dbIcon, 'Analytics DB')
            self.setCurrentTab(self.analyticsDB)
        else:
            QMessageBox.warning(self, 'No Connection', "Can't connect to Database")
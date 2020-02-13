from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

Ui_Home, QBaseClass = uic.loadUiType('./views/home.ui')

from models.icon import Icon

class Home(QWidget, Ui_Home):
    def __init__(self, onLoadCSV, onLoadDB):
        QWidget.__init__(self)
        Ui_Home.__init__(self)
        self.setupUi(self)

        self.csvIcon = Icon('file-csv.svg', '#D50').getIcon()
        self.dbIcon = Icon('database.svg', '#666').getIcon()

        # push CSV
        self.pushCSV.setIcon(self.csvIcon)
        self.pushCSV.clicked.connect(onLoadCSV)
        
        # push DB
        self.pushDB.setIcon(self.dbIcon)
        self.pushDB.clicked.connect(onLoadDB)
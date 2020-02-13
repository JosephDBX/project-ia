from models.icon import Icon
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

Ui_DatabaseDialog, QBaseApp = uic.loadUiType('./views/databasedialog.ui')


class DatabaseDialogController(QDialog, Ui_DatabaseDialog):
    def __init__(self, parent, method):
        QDialog.__init__(self, parent)
        Ui_DatabaseDialog.__init__(self)
        self.setupUi(self)

        self.onConnect = method

        # icons
        plugIcon = Icon('plug.svg', '#060').getIcon()

        self.pushConnect.clicked.connect(self.onPushConnect)
        self.pushConnect.setIcon(plugIcon)

        self.checkBoxTable.stateChanged.connect(self.onStateChanged)
        self.checkBoxTable.setChecked(True)

    def onPushConnect(self):
        DB_USER = self.lineEditUser.text()
        DB_PASS = self.lineEditPass.text()
        DB_HOST = self.lineEditHost.text()
        DB_PORT = self.spinPort.value()
        DATABASE = self.lineEditName.text()
        CHARSET = self.lineEditCharset.text()
        TABLE_NAME = self.lineEditTableName.text()
        QUERY = self.lineEditQuery.text()
        self.onConnect(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE,
                       CHARSET, TABLE_NAME, QUERY, self.checkBoxTable.checkState())
        self.accept()

    def onStateChanged(self, state):
        if self.checkBoxTable.checkState():
            self.lineEditTableName.setEnabled(True)
            self.lineEditQuery.setEnabled(False)
        else:
            self.lineEditTableName.setEnabled(False)
            self.lineEditQuery.setEnabled(True)

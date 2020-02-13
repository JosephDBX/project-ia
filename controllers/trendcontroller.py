from models.icon import Icon
import pandas as pd
import numpy as np
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox, QCheckBox, QDoubleSpinBox, QTableView, QHeaderView

from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from sklearn.externals import joblib

from models.dataframetablemodel import DataFrameTableModel

Ui_TrendWindow, QBaseApp = uic.loadUiType('./views/trendwindow.ui')


class TrendController(QMainWindow, Ui_TrendWindow):
    def __init__(self, parent, data: pd.DataFrame, title='', path=''):
        QMainWindow.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        Ui_TrendWindow.__init__(self)
        self.setupUi(self)

        self.df: pd.DataFrame = data.select_dtypes([np.number])
        self.mlp: MLPRegressor = joblib.load(path)
        self.filterTitle = title
        self.setWindowTitle('Trend Analytics - {}'.format(self.filterTitle))
        self.labelTitle.setText(path)

        # table DF
        self.tableDF.setSelectionBehavior(QTableView.SelectRows)
        self.tableDF.setSelectionMode(QTableView.SingleSelection)
        self.tableDF.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableDF.doubleClicked.connect(self.onTableDF)
        self.updateTableDF(self.df)

        # Filter Columns
        self.comboOutput.addItems(list(self.df.columns))
        self.comboOutput.currentIndexChanged.connect(self.onComboOutput)
        self.comboOutput.setCurrentIndex(-1)

        # widget inputs
        self.layoutInputs = QVBoxLayout()
        self.layoutInputs.setContentsMargins(0, 0, 0, 0)
        self.widgetInputs.setLayout(self.layoutInputs)

        # icons
        self.calculatorIcon = Icon('calculator.svg', '#060').getIcon()

        # Buttons
        self.pushCalculate.setIcon(self.calculatorIcon)
        self.pushCalculate.clicked.connect(self.onCalculate)

    def updateTableDF(self, data: pd.DataFrame):
        if not data.empty:
            self.tableDF.setModel(DataFrameTableModel(data))
        else:
            QMessageBox.warning(self, 'No DataFrame', 'DataFrame Not Found')

    def onTableDF(self):
        indexes = self.tableDF.selectionModel().selectedRows()
        if not indexes:
            QMessageBox.warning(self, 'No Selected Row',
                                'You must select a row')
        for index in sorted(indexes):
            current = self.df.iloc[index.row(), :]
            QMessageBox.warning(self, 'Selected Data', '{}'.format(current))
            self.tableDF.clearSelection()

    def onComboOutput(self, index):
        if index > -1:
            self.pushCalculate.setEnabled(True)
            self.clearLayout(self.layoutInputs)

            self.listCheckBox = list(self.df.drop(
                self.comboOutput.currentText(), 1).columns)
            self.listDoubleSpinBox = list(self.df.drop(
                self.comboOutput.currentText(), 1).columns)
            for i, value in enumerate(self.listCheckBox):
                self.listCheckBox[i] = QCheckBox(value)
                self.listCheckBox[i].stateChanged.connect(self.onStateChanged)
                self.layoutInputs.addWidget(self.listCheckBox[i])
                self.listDoubleSpinBox[i] = QDoubleSpinBox()
                self.listDoubleSpinBox[i].setDecimals(6)
                self.listDoubleSpinBox[i].setMaximum(9999999.999999)
                self.listDoubleSpinBox[i].setEnabled(False)
                self.layoutInputs.addWidget(self.listDoubleSpinBox[i])

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def onStateChanged(self, state):
        for i, value in enumerate(self.listCheckBox):
            if value.checkState():
                self.listDoubleSpinBox[i].setEnabled(True)
            else:
                self.listDoubleSpinBox[i].setEnabled(False)

    def onCalculate(self):
        toPredict = []
        toPredictLabels = []
        for i, value in enumerate(self.listDoubleSpinBox):
            if value.isEnabled():
                toPredict.append(value.value())
                toPredictLabels.append(self.listCheckBox[i].text())
        if len(toPredict) > 0:
            try:
                predic = self.mlp.predict([toPredict])
                predictText = 'For '
                for i, value in enumerate(toPredict):
                    predictText = '{}{}={}, '.format(
                        predictText, toPredictLabels[i], value)
                predictText = '{}the result is "{}={}"'.format(
                    predictText, self.comboOutput.currentText(), predic[0])
                self.labelResult.setText(predictText)
            except:
                QMessageBox.warning(
                    self, 'Mismatch Inputs', 'Input Parameters do not Match the Trained Neural Network')
                self.labelResult.setText('')
        else:
            QMessageBox.warning(self, 'Inputs not Found',
                                'You have to Define the Input Xs')

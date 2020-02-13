from .trendcontroller import TrendController
from .trainingcontroller import TrainingController
from .graphcontroller import GraphController
from .correlationcontroller import CorrelationController
from models.dataframetablemodel import DataFrameTableModel
from models.icon import Icon
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableView, QMessageBox, QHeaderView, QFileDialog

import pandas as pd

Ui_Analytics, QBaseClass = uic.loadUiType('./views/analytics.ui')


class Analytics(QWidget, Ui_Analytics):
    def __init__(self, dataframe: pd.DataFrame, title="FOB"):
        QWidget.__init__(self)
        Ui_Analytics.__init__(self)
        self.setupUi(self)

        self.df = dataframe
        self.dfItem: pd.DataFrame = pd.DataFrame

        # icons
        self.linkIcon = Icon('link.svg', '#0A0').getIcon()
        self.chartBarIcon = Icon('chart-bar.svg', '#080').getIcon()
        self.boxesIcon = Icon('boxes.svg', '#060').getIcon()
        self.projectIcon = Icon('project-diagram.svg', '#006').getIcon()
        self.openIcon = Icon('folder-open.svg', '#008').getIcon()
        self.chartLineIcon = Icon('chart-line.svg', '#A00').getIcon()

        # table DF
        self.labelTitle.setText(title)
        self.tableDF.setSelectionBehavior(QTableView.SelectRows)
        self.tableDF.setSelectionMode(QTableView.SingleSelection)
        self.tableDF.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableDF.doubleClicked.connect(self.onTableDF)
        self.updateTableDF(self.df)

        # table Item
        self.tableItem.setSelectionBehavior(QTableView.SelectRows)
        self.tableItem.setSelectionMode(QTableView.SingleSelection)
        self.tableItem.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableItem.doubleClicked.connect(self.onTableItem)

        # Filter Columns
        self.comboFilterColumn.addItems(list(self.df.columns))
        self.comboFilterColumn.currentIndexChanged.connect(
            self.onComboFilterColumn)
        self.comboFilterColumn.setCurrentIndex(-1)

        # Filter
        self.comboFilter.currentIndexChanged.connect(self.onComboFilter)
        self.comboFilter.setCurrentIndex(-1)

        # Buttons
        self.pushCorrelation.setIcon(self.linkIcon)
        self.pushCorrelation.clicked.connect(self.onCorrelation)

        self.pushHistogram.setIcon(self.chartBarIcon)
        self.pushHistogram.clicked.connect(self.onHistogram)

        self.pushBoxDiagram.setIcon(self.boxesIcon)
        self.pushBoxDiagram.clicked.connect(self.onBoxDiagram)

        self.pushTrainingNN.setIcon(self.projectIcon)
        self.pushTrainingNN.clicked.connect(self.onTrainingNN)

        self.pushLoadTrainedNN.setIcon(self.openIcon)
        self.pushLoadTrainedNN.clicked.connect(self.onLoadTrainedNN)

        self.pushItemCorrelation.setIcon(self.chartLineIcon)
        self.pushItemCorrelation.clicked.connect(self.onItemCorrelation)

        self.checkBoxFilter.stateChanged.connect(self.onStateChanged)
        self.checkBoxFilter.setChecked(True)

    def onStateChanged(self, state):
        if self.checkBoxFilter.checkState():
            self.onDataTableItem()
            self.comboFilterColumn.setEnabled(True)
            self.comboFilter.setEnabled(True)
        else:
            self.onDataTableItem(True)
            self.pushItemCorrelation.setEnabled(False)
            self.comboFilterColumn.setEnabled(False)
            self.comboFilter.setEnabled(False)
            self.comboFilterColumn.setCurrentIndex(-1)
            self.comboFilter.setCurrentIndex(-1)
            self.filterTitle = 'data'

    def updateTableDF(self, data: pd.DataFrame):
        if not data.empty:
            self.tableDF.setModel(DataFrameTableModel(data))
        else:
            QMessageBox.warning(self, 'No DataFrame', 'DataFrame Not Found')

    def updateTableItem(self, data: pd.DataFrame):
        if not data.empty:
            self.tableItem.setModel(DataFrameTableModel(data))
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

    def onTableItem(self):
        indexes = self.tableItem.selectionModel().selectedRows()
        if not indexes:
            QMessageBox.warning(self, 'No Selected Row',
                                'You must select a row')
        for index in sorted(indexes):
            current = self.dfItem.iloc[index.row(), :]
            QMessageBox.warning(self, 'Selected Data', '{}'.format(current))
            self.tableItem.clearSelection()

    def onComboFilterColumn(self, index):
        if index > -1:
            self.comboFilter.clear()
            items = self.df[self.comboFilterColumn.currentText()].unique()
            for i, v in enumerate(items):
                self.comboFilter.addItem('{}'.format(items[i]))
        else:
            self.comboFilter.clear()

    def onComboFilter(self, index):
        if index > -1:
            self.filterTitle = '{}={}'.format(
                self.comboFilterColumn.currentText(), self.comboFilter.currentText())
            self.labelItem.setText(self.filterTitle)
            try:
                aux = float(self.comboFilter.currentText())
            except:
                aux = self.comboFilter.currentText()

            self.dfItem: pd.DataFrame = self.df.where(
                self.df[self.comboFilterColumn.currentText()] == aux).dropna()
            self.updateTableItem(self.dfItem)
            if not self.dfItem.empty:
                self.onDataTableItem(True)
            else:
                self.onDataTableItem()
        else:
            self.dfItem: pd.DataFrame = pd.DataFrame

    def onDataTableItem(self, state=False):
        self.pushCorrelation.setEnabled(state)
        self.pushHistogram.setEnabled(state)
        self.pushBoxDiagram.setEnabled(state)
        self.pushTrainingNN.setEnabled(state)
        self.pushLoadTrainedNN.setEnabled(state)
        self.pushItemCorrelation.setEnabled(state)

    def onCorrelation(self):
        data: pd.DataFrame = self.df if self.dfItem.empty else self.dfItem
        graph = GraphController(
            self, data, 'Columns Correlation - {}'.format(self.filterTitle))
        graph.graphColumnCorrelation()

    def onHistogram(self):
        data: pd.DataFrame = self.df if self.dfItem.empty else self.dfItem
        graph = GraphController(
            self, data, 'Histogram - {}'.format(self.filterTitle))
        graph.graphHistogram()

    def onBoxDiagram(self):
        data: pd.DataFrame = self.df if self.dfItem.empty else self.dfItem
        graph = GraphController(
            self, data, 'Box Diagram - {}'.format(self.filterTitle))
        graph.graphBoxDiagram()

    def onTrainingNN(self):
        data: pd.DataFrame = self.df if self.dfItem.empty else self.dfItem
        training = TrainingController(self, data, self.filterTitle)
        training.show()

    def onLoadTrainedNN(self):
        path = QFileDialog.getOpenFileName(
            self, 'Load Trained Neural Network', '', 'PKL(*.pkl)')
        if path[0] != '':
            data: pd.DataFrame = self.df if self.dfItem.empty else self.dfItem
            trend = TrendController(self, data, self.filterTitle, path[0])
            trend.show()

    def onItemCorrelation(self):
        correlation = CorrelationController(
            self, self.filterTitle, self.comboFilter.currentText(), self.dfItem, self.comboFilterColumn.currentText(), self.df)
        correlation.showMaximized()

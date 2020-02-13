from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from models.dataframetablemodel import DataFrameTableModel
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
from models.icon import Icon
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QTableView, QHeaderView, QMessageBox, QVBoxLayout

Ui_CorrelationWindow, QBaseApp = uic.loadUiType('./views/correlationwindow.ui')


class CorrelationController(QMainWindow, Ui_CorrelationWindow):
    def __init__(self, parent, filterTitle, filterX, dfX: pd.DataFrame, filterY, dfToFilter: pd.DataFrame):
        QMainWindow.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        Ui_CorrelationWindow.__init__(self)
        self.setupUi(self)

        graph = ['regplot']
        self.dfX: pd.DataFrame = dfX
        self.dfY: pd.DataFrame = pd.DataFrame
        self.df: pd.DataFrame = dfToFilter
        self.filter = filterY
        self.filterX = filterX
        columns = self.df.select_dtypes([np.number]).columns

        # icons
        chartIcon = Icon('chart-line.svg', '#A00').getIcon()

        # push graph
        self.pushGraph.setIcon(chartIcon)
        self.pushGraph.clicked.connect(self.onGraph)

        # widget canvas
        self.canvas = FigureCanvasQTAgg(Figure())
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.addWidget(self.canvas)
        self.GraphCanvas.setLayout(vLayout)

        self.addToolBar(NavigationToolbar2QT(self.canvas, self))

        # to graph
        self.comboToGraph.addItems(list(graph))

        # X
        self.labelX.setText('DataFrame X - {}'.format(filterTitle))
        self.tableDFX.setSelectionBehavior(QTableView.SelectRows)
        self.tableDFX.setSelectionMode(QTableView.SingleSelection)
        self.tableDFX.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableDFX.doubleClicked.connect(self.onTableDFX)
        self.updateTableDFX(self.dfX)
        self.comboXColumn.addItems(list(columns))

        # Y
        self.labelY.setText('')
        self.tableDFY.setSelectionBehavior(QTableView.SelectRows)
        self.tableDFY.setSelectionMode(QTableView.SingleSelection)
        self.tableDFY.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableDFY.doubleClicked.connect(self.onTableDFY)
        self.comboYColumn.addItems(list(columns))

        # combo filter
        self.comboFilter.currentIndexChanged.connect(self.onComboFilter)
        items = self.df[self.filter].unique()
        for i, v in enumerate(items):
            self.comboFilter.addItem('{}'.format(items[i]))

    def updateTableDFX(self, data: pd.DataFrame):
        if not data.empty:
            self.tableDFX.setModel(DataFrameTableModel(data))
        else:
            QMessageBox.warning(self, 'No DataFrame', 'DataFrame X Not Found')

    def updateTableDFY(self, data: pd.DataFrame):
        if not data.empty:
            self.tableDFY.setModel(DataFrameTableModel(data))
        else:
            QMessageBox.warning(self, 'No DataFrame', 'DataFrame Y Not Found')

    def onTableDFX(self):
        indexes = self.tableDFX.selectionModel().selectedRows()
        if not indexes:
            QMessageBox.warning(self, 'No Selected Row',
                                'You must select a row')
        for index in sorted(indexes):
            current = self.dfX.iloc[index.row(), :]
            QMessageBox.warning(self, 'Selected Data DF X',
                                '{}'.format(current))
            self.tableDFX.clearSelection()

    def onTableDFY(self):
        indexes = self.tableDFY.selectionModel().selectedRows()
        if not indexes:
            QMessageBox.warning(self, 'No Selected Row',
                                'You must select a row')
        for index in sorted(indexes):
            current = self.dfY.iloc[index.row(), :]
            QMessageBox.warning(self, 'Selected Data DF Y',
                                '{}'.format(current))
            self.tableDFY.clearSelection()

    def onComboFilter(self, index):
        if index > -1:
            self.filterTitle = 'DataFrame Y - {}={}'.format(
                self.filter, self.comboFilter.currentText())
            self.labelY.setText(self.filterTitle)
            try:
                aux = float(self.comboFilter.currentText())
            except:
                aux = self.comboFilter.currentText()

            self.dfY: pd.DataFrame = self.df.where(
                self.df[self.filter] == aux).dropna()
            self.updateTableDFY(self.dfY)
        else:
            self.dfY: pd.DataFrame = pd.DataFrame

    def onGraph(self):
        aux = self.comboToGraph.currentIndex()
        if aux == 0:
            self.graphRegplot()

    def graphRegplot(self):
        data = pd.DataFrame()
        data['X - {}'.format(self.comboXColumn.currentText())
             ] = self.dfX[self.comboXColumn.currentText()].to_numpy()
        data['Y - {}'.format(self.comboYColumn.currentText())
             ] = self.dfY[self.comboYColumn.currentText()].to_numpy()

        slope, intercept, r_value, p_value, std_err = stats.linregress(
            data['X - {}'.format(self.comboXColumn.currentText())], data['Y - {}'.format(self.comboYColumn.currentText())])

        axes = self.getAxes(1, 1, 1)
        if self.checkBoxClear.checkState():
            axes.clear()
            self.checkBoxClear.setCheckState(False)

        axes.set_title('regplot')
        plot = sns.regplot(x='X - {}'.format(self.comboXColumn.currentText()),
                           y='Y - {}'.format(self.comboYColumn.currentText()),
                           data=data, order=1, ax=axes,
                           line_kws={'label': "X={}({})/Y={}({}) - Function(Y={:.2f}+{:.2f}X)".format(self.comboXColumn.currentText(), self.filterX, self.comboYColumn.currentText(), self.comboFilter.currentText(), intercept, slope)})
        # axes.axis('equal')
        axes.grid(True)
        axes.legend(loc=0)

        self.toGraph()

    def getAxes(self, nRows, nColumns, position):
        return self.canvas.figure.add_subplot(nRows, nColumns, position)

    def toGraph(self):
        self.canvas.figure.tight_layout()
        self.canvas.draw()

import seaborn as sns
import pandas as pd
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

Ui_GraphWindow, QBaseApp = uic.loadUiType('./views/graphwindow.ui')


class GraphController(QMainWindow, Ui_GraphWindow):
    def __init__(self, parent, data: pd.DataFrame, title=''):
        QMainWindow.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        Ui_GraphWindow.__init__(self)
        self.setupUi(self)

        self.data: pd.DataFrame = data
        self.setWindowTitle(title)

        self.canvas = FigureCanvasQTAgg(Figure())
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.addWidget(self.canvas)
        self.GraphCanvas.setLayout(vLayout)

        self.addToolBar(NavigationToolbar2QT(self.canvas, self))

    def getAxes(self, nRows, nColumns, position):
        return self.canvas.figure.add_subplot(nRows, nColumns, position)

    def toGraph(self):
        self.canvas.figure.tight_layout()
        self.canvas.draw()
        self.show()

    def graphColumnCorrelation(self):
        axes = self.getAxes(1, 1, 1)
        axes.clear()

        cmap = plt.cm.BuGn
        sns.heatmap(self.data.corr(), linewidths=0.1, vmax=1.0,
                   square=True, cmap=cmap, linecolor='white', annot=True, ax=axes)

        axes.axis('equal')
        self.toGraph()

    def graphHistogram(self):
        axes = self.getAxes(1, 1, 1)
        axes.clear()

        self.data.hist(ax=axes)

        axes.axis('equal')
        self.toGraph()

    def graphBoxDiagram(self):
        axes = self.getAxes(1, 1, 1)
        axes.clear()

        cmap = plt.cm.Set1
        self.data.plot(kind='box', subplots=True, sharex=False, sharey=False, ax=axes, colormap=cmap)

        axes.axis('equal')
        self.toGraph()
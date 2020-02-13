from models.icon import Icon
import seaborn as sb
import pandas as pd
import numpy as np
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox, QCheckBox, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.pyplot import pause

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from sklearn.externals import joblib
from sklearn import decomposition

from math import ceil

Ui_TrainingWindow, QBaseApp = uic.loadUiType('./views/trainingwindow.ui')


class TrainingController(QMainWindow, Ui_TrainingWindow):
    def __init__(self, parent, data: pd.DataFrame, title=''):
        QMainWindow.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint)
        Ui_TrainingWindow.__init__(self)
        self.setupUi(self)

        self.data: pd.DataFrame = data.select_dtypes([np.number])
        self.filterTitle = title
        self.setWindowTitle(
            'Neural Network Training - {}'.format(self.filterTitle))
        self.isStop = False

        # Filter Columns
        self.comboOutput.addItems(list(self.data.columns))
        self.comboOutput.currentIndexChanged.connect(self.onComboOutput)
        self.comboOutput.setCurrentIndex(-1)

        # widget inputs
        self.layoutInputs = QVBoxLayout()
        self.layoutInputs.setContentsMargins(0, 0, 0, 0)
        self.widgetInputs.setLayout(self.layoutInputs)

        # widget canvas
        self.canvas = FigureCanvasQTAgg(Figure())
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.addWidget(self.canvas)
        self.GraphCanvas.setLayout(vLayout)

        self.addToolBar(NavigationToolbar2QT(self.canvas, self))

        # icons
        self.playIcon = Icon('play.svg', '#0A0').getIcon()
        self.stopIcon = Icon('stop.svg', '#A00').getIcon()
        self.saveIcon = Icon('save.svg', '#00A').getIcon()

        # Buttons
        self.pushStart.setIcon(self.playIcon)
        self.pushStart.clicked.connect(self.onStart)

        self.pushStop.setIcon(self.stopIcon)
        self.pushStop.clicked.connect(self.onStop)

        self.pushSave.setIcon(self.saveIcon)
        self.pushSave.clicked.connect(self.onSave)

    def onComboOutput(self, index):
        if index > -1:
            self.pushStart.setEnabled(True)
            self.clearLayout(self.layoutInputs)

            self.listCheckBox = list(self.data.drop(
                self.comboOutput.currentText(), 1).columns)
            for i, value in enumerate(self.listCheckBox):
                self.listCheckBox[i] = QCheckBox(value)
                self.layoutInputs.addWidget(self.listCheckBox[i])

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def onStart(self):
        if self.spinIterations.value() > 0 and self.spinLR.value() > 0 and self.spinAlpha.value() > 0:
            self.Xn = []
            for i, v in enumerate(self.listCheckBox):
                if v.checkState():
                    self.Xn.append(v.text())
            self.yn = self.comboOutput.currentText()

            if len(self.Xn) > 0:
                self.comboOutput.setEnabled(False)
                self.widgetInputs.setEnabled(False)
                self.pushStart.setEnabled(False)
                self.pushSave.setEnabled(False)
                self.pushStop.setEnabled(True)
                self.spinIterations.setEnabled(False)
                self.spinLR.setEnabled(False)
                self.spinAlpha.setEnabled(False)

                nColumns = ceil(len(self.Xn)/2)

                X = self.data.drop(self.yn, 1)
                y = self.data[self.yn]
                X_train, X_test, y_train, y_test = train_test_split(X, y)

                self.mlp = MLPRegressor(solver='adam', alpha=self.spinAlpha.value(
                ), learning_rate_init=self.spinLR.value(), max_iter=self.spinIterations.value())

                i = 1
                self.score_test = 0
                self.score_train = 0
                self.canvas.figure.clf()
                while i <= self.spinIterations.value():
                    self.mlp.partial_fit(X_train, y_train)
                    self.score_test = r2_score(
                        y_test, self.mlp.predict(X_test))
                    self.score_train = self.mlp.score(X_train, y_train)

                    for j, value in enumerate(self.Xn):
                        axes = self.getAxes(2, nColumns, j+1)
                        axes.clear()

                        axes.set_title('Training X={}, y={} - Epoch {}/{}'.format(
                            value, self.comboOutput.currentText(), i, self.spinIterations.value()))
                        axes.plot(
                            self.data[value], y, c='blue', label='Real Data - Test Score={:.2f}'.format(self.score_test))
                        axes.plot(self.data[value], self.mlp._predict(
                            X), 'r--', c='red', label='NN Model - Training Score={:.2f}'.format(self.score_train))
                        axes.grid(True)
                        axes.legend(loc='upper right')

                    self.toGraph()
                    if self.isStop:
                        break
                    i += 1

                if i > self.spinIterations.value():
                    i = self.spinIterations.value()

                self.isStop = False
                self.comboOutput.setEnabled(True)
                self.widgetInputs.setEnabled(True)
                self.pushStart.setEnabled(True)
                self.pushSave.setEnabled(True)
                self.pushStop.setEnabled(False)
                self.spinIterations.setEnabled(True)
                self.spinLR.setEnabled(True)
                self.spinAlpha.setEnabled(True)
                QMessageBox.warning(self, 'Training Complete', 'Test Score={:.2f}, Training Score={:.2f} at {} Iterations'.format(
                    self.score_test, self.score_train, i))
            else:
                QMessageBox.warning(
                    self, 'No Xs inputs for Training', 'You Must Select at Least a X for Input')
        else:
            QMessageBox.warning(self, "Zeros Can't be Selected",
                                'Learning Rate, Alpha and Maximum Iterations must be greater than zero')

    def onStop(self):
        self.isStop = True
        self.pushStart.setEnabled(True)
        self.pushStop.setEnabled(False)
        self.pushSave.setEnabled(True)
        self.comboOutput.setEnabled(True)
        self.widgetInputs.setEnabled(True)

    def onSave(self):
        auxName = '{}'.format(self.Xn[0])
        i = 1
        while i < len(self.Xn):
            auxName = '{},{}'.format(auxName, self.Xn[i])
            i += 1
        path = QFileDialog.getExistingDirectory(
            self, 'Save Trained Neural Network', '')
        if path != '':
            path = '{}/{}-y={}-X={}-Test={:.2f}-Trainig={:.2f}.pkl'.format(
                path, self.filterTitle, self.yn, auxName, self.score_test, self.score_train)
            # save model
            joblib.dump(self.mlp, path)
            QMessageBox.warning(self, 'Trained Neural Network Saved',
                                'Trained Neural Network Saved at "{}"'.format(path))

    def getAxes(self, nRows, nColumns, position):
        return self.canvas.figure.add_subplot(nRows, nColumns, position)

    def toGraph(self):
        self.canvas.figure.tight_layout()
        self.canvas.draw()
        self.canvas.flush_events()
        pause(.000001)

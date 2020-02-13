from PyQt5.QtCore import QAbstractTableModel, Qt

class DataFrameTableModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, QtOrientation, role=Qt.DisplayRole):
        if QtOrientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        if QtOrientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[col]
        return None
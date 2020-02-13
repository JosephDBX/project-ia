from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap, QColor, QIcon

class Icon():
    def __init__(self, filename, color='#FFF'):
        super().__init__()
        self.pixmap = QPixmap('./icons/{}'.format(filename))
        mask = self.pixmap.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
        self.pixmap.fill((QColor(color)))
        self.pixmap.setMask(mask)

    def getIcon(self):
        return QIcon(self.pixmap)
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtGui import QIcon

    from controllers.maincontroller import MainController

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main = MainController()
    main.setWindowIcon(QIcon('./icons/favicon.png'))
    main.showMaximized()
    sys.exit(app.exec_())

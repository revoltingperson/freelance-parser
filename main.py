from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox

from main_widget import MainWidget
from settings import logger

if __name__ == "__main__":
    import sys
    try:
        app = QtWidgets.QApplication(sys.argv)
        widget = MainWidget()
        widget.show()
        app.setStyle('Fusion')
        sys.exit(app.exec())

    except Exception as e:
        QMessageBox.warning(None, 'Ошибка', "Произошла неизвестная ошибка")
        logger.exception(e)



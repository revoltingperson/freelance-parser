from ui_team_element import Ui_Form
from PySide6.QtWidgets import QWidget, QFrame


class TeamElement(QFrame, Ui_Form):
    def __init__(self):
        super(TeamElement, self).__init__()
        self.setupUi(self)




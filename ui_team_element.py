# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'team_elementUzRrRR.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QSizePolicy,
                               QSpacerItem, QVBoxLayout)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(754, 47)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        Form.setFont(font)
        Form.setStyleSheet(u"QWidget#Form{border: 2px solid;}")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        # self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        #
        # self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(True)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.teams = QLabel(Form)
        self.teams.setObjectName(u"teams")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(False)
        self.teams.setFont(font2)

        self.horizontalLayout.addWidget(self.teams)

        self.score = QLabel(Form)
        self.score.setObjectName(u"score")
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.score.setFont(font3)

        self.horizontalLayout.addWidget(self.score)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043c\u0430\u043d\u0434\u044b", None))
        self.teams.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.score.setText(QCoreApplication.translate("Form", u"\u0421\u0447\u0435\u0442", None))
    # retranslateUi


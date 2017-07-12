# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_settingsmanager.ui'
#
# Created: Thu Apr  3 15:51:39 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SettingsManager(object):
    def setupUi(self, SettingsManager):
        SettingsManager.setObjectName(_fromUtf8("SettingsManager"))
        SettingsManager.resize(298, 68)
        self.gridLayout = QtGui.QGridLayout(SettingsManager)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(SettingsManager)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SettingsManager)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.No|QtGui.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SettingsManager)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SettingsManager.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SettingsManager.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsManager)

    def retranslateUi(self, SettingsManager):
        SettingsManager.setWindowTitle(_translate("SettingsManager", "Settings Manager", None))
        self.label.setText(_translate("SettingsManager", "Voulez-vous installer les paramètres SIT ?", None))

import resources_rc

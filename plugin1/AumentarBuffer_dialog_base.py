# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AumentarBuffer_dialog_base.ui'
#
# Created: Mon Apr 03 12:13:32 2017
#      by: PyQt4 UI code generator 4.10.2
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

class Ui_AumentarBufferDialogBase(object):
    def setupUi(self, AumentarBufferDialogBase):
        AumentarBufferDialogBase.setObjectName(_fromUtf8("AumentarBufferDialogBase"))
        AumentarBufferDialogBase.resize(386, 115)
        self.button_box = QtGui.QDialogButtonBox(AumentarBufferDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 70, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.DistancelineEdit = QtGui.QLineEdit(AumentarBufferDialogBase)
        self.DistancelineEdit.setGeometry(QtCore.QRect(282, 20, 91, 20))
        self.DistancelineEdit.setObjectName(_fromUtf8("DistancelineEdit"))
        self.splitter = QtGui.QSplitter(AumentarBufferDialogBase)
        self.splitter.setGeometry(QtCore.QRect(30, 20, 213, 26))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.label = QtGui.QLabel(self.splitter)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.splitter)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(AumentarBufferDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), AumentarBufferDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), AumentarBufferDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(AumentarBufferDialogBase)

    def retranslateUi(self, AumentarBufferDialogBase):
        AumentarBufferDialogBase.setWindowTitle(_translate("AumentarBufferDialogBase", "Aumentar alero de bloque catastral", None))
        self.label.setText(_translate("AumentarBufferDialogBase", "Introuduzca la distancia del alero en metros:", None))
        self.label_2.setText(_translate("AumentarBufferDialogBase", "(el bloque se agrandará)", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    AumentarBufferDialogBase = QtGui.QDialog()
    ui = Ui_AumentarBufferDialogBase()
    ui.setupUi(AumentarBufferDialogBase)
    AumentarBufferDialogBase.show()
    sys.exit(app.exec_())


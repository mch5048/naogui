# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../include/mainwindow.ui'
#
# Created: Mon Feb 29 11:47:16 2016
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1920, 1080)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.btnConfirm = QtGui.QPushButton(self.tab)
        self.btnConfirm.setGeometry(QtCore.QRect(860, 210, 181, 171))
        self.btnConfirm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnConfirm.setText(_fromUtf8(""))
        self.btnConfirm.setObjectName(_fromUtf8("btnConfirm"))
        self.horizontalSlider = QtGui.QSlider(self.tab)
        self.horizontalSlider.setGeometry(QtCore.QRect(630, 500, 641, 51))
        self.horizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setProperty("value", 5)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.horizontalSliderRobot = QtGui.QSlider(self.tab)
        self.horizontalSliderRobot.setEnabled(False)
        self.horizontalSliderRobot.setGeometry(QtCore.QRect(330, 50, 1241, 51))
        self.horizontalSliderRobot.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.horizontalSliderRobot.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.horizontalSliderRobot.setMaximum(30)
        self.horizontalSliderRobot.setSingleStep(1)
        self.horizontalSliderRobot.setProperty("value", 15)
        self.horizontalSliderRobot.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderRobot.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.horizontalSliderRobot.setTickInterval(1)
        self.horizontalSliderRobot.setObjectName(_fromUtf8("horizontalSliderRobot"))
        self.groupBox_4 = QtGui.QGroupBox(self.tab)
        self.groupBox_4.setGeometry(QtCore.QRect(660, 640, 601, 281))
        self.groupBox_4.setTitle(_fromUtf8(""))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(470, 40, 81, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lcdNumberTotal = QtGui.QLCDNumber(self.groupBox_4)
        self.lcdNumberTotal.setGeometry(QtCore.QRect(470, 60, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumberTotal.setFont(font)
        self.lcdNumberTotal.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumberTotal.setAutoFillBackground(False)
        self.lcdNumberTotal.setProperty("intValue", 0)
        self.lcdNumberTotal.setObjectName(_fromUtf8("lcdNumberTotal"))
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lcdNumberRound = QtGui.QLCDNumber(self.groupBox_4)
        self.lcdNumberRound.setGeometry(QtCore.QRect(10, 30, 131, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumberRound.setFont(font)
        self.lcdNumberRound.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumberRound.setAutoFillBackground(False)
        self.lcdNumberRound.setProperty("intValue", 10)
        self.lcdNumberRound.setObjectName(_fromUtf8("lcdNumberRound"))
        self.lcdNumberYourInvestment = QtGui.QLCDNumber(self.groupBox_4)
        self.lcdNumberYourInvestment.setGeometry(QtCore.QRect(170, 30, 131, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumberYourInvestment.setFont(font)
        self.lcdNumberYourInvestment.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumberYourInvestment.setAutoFillBackground(False)
        self.lcdNumberYourInvestment.setProperty("intValue", 0)
        self.lcdNumberYourInvestment.setObjectName(_fromUtf8("lcdNumberYourInvestment"))
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setGeometry(QtCore.QRect(170, 10, 141, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lcdNumberRobotInvestment = QtGui.QLCDNumber(self.groupBox_4)
        self.lcdNumberRobotInvestment.setGeometry(QtCore.QRect(320, 30, 131, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumberRobotInvestment.setFont(font)
        self.lcdNumberRobotInvestment.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumberRobotInvestment.setAutoFillBackground(False)
        self.lcdNumberRobotInvestment.setProperty("intValue", 0)
        self.lcdNumberRobotInvestment.setObjectName(_fromUtf8("lcdNumberRobotInvestment"))
        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setGeometry(QtCore.QRect(320, 10, 141, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.btnStartExperiment = QtGui.QPushButton(self.groupBox_4)
        self.btnStartExperiment.setGeometry(QtCore.QRect(10, 130, 571, 111))
        self.btnStartExperiment.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btnStartExperiment.setObjectName(_fromUtf8("btnStartExperiment"))
        self.groupBox_5 = QtGui.QGroupBox(self.tab)
        self.groupBox_5.setGeometry(QtCore.QRect(1080, 250, 161, 91))
        self.groupBox_5.setTitle(_fromUtf8(""))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.lcdNumberPlayerInvestment = QtGui.QLCDNumber(self.groupBox_5)
        self.lcdNumberPlayerInvestment.setGeometry(QtCore.QRect(10, 30, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.lcdNumberPlayerInvestment.setFont(font)
        self.lcdNumberPlayerInvestment.setObjectName(_fromUtf8("lcdNumberPlayerInvestment"))
        self.label_8 = QtGui.QLabel(self.groupBox_5)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.groupBox = QtGui.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(250, 220, 271, 201))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lineEditNaoIP = QtGui.QLineEdit(self.groupBox)
        self.lineEditNaoIP.setGeometry(QtCore.QRect(10, 50, 151, 27))
        self.lineEditNaoIP.setObjectName(_fromUtf8("lineEditNaoIP"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 151, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnConnectToNao = QtGui.QPushButton(self.groupBox)
        self.btnConnectToNao.setGeometry(QtCore.QRect(10, 90, 251, 91))
        self.btnConnectToNao.setObjectName(_fromUtf8("btnConnectToNao"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(180, 30, 61, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEditNaoPort = QtGui.QLineEdit(self.groupBox)
        self.lineEditNaoPort.setGeometry(QtCore.QRect(180, 50, 81, 27))
        self.lineEditNaoPort.setInputMask(_fromUtf8(""))
        self.lineEditNaoPort.setObjectName(_fromUtf8("lineEditNaoPort"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(250, 90, 291, 121))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 151, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.textEditXML = QtGui.QTextEdit(self.groupBox_2)
        self.textEditXML.setGeometry(QtCore.QRect(0, 50, 211, 51))
        self.textEditXML.setReadOnly(True)
        self.textEditXML.setObjectName(_fromUtf8("textEditXML"))
        self.btnBrowse = QtGui.QPushButton(self.groupBox_2)
        self.btnBrowse.setGeometry(QtCore.QRect(220, 50, 51, 51))
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.groupBox_3 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(580, 90, 391, 331))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.btnWakeUp = QtGui.QPushButton(self.groupBox_3)
        self.btnWakeUp.setEnabled(False)
        self.btnWakeUp.setGeometry(QtCore.QRect(10, 50, 361, 121))
        self.btnWakeUp.setObjectName(_fromUtf8("btnWakeUp"))
        self.btnRest = QtGui.QPushButton(self.groupBox_3)
        self.btnRest.setEnabled(False)
        self.btnRest.setGeometry(QtCore.QRect(10, 190, 361, 121))
        self.btnRest.setObjectName(_fromUtf8("btnRest"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1920, 25))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "---", None))
        self.label_4.setText(_translate("MainWindow", "Total:", None))
        self.label_5.setText(_translate("MainWindow", "Round total:", None))
        self.label_6.setText(_translate("MainWindow", "Your investment:", None))
        self.label_7.setText(_translate("MainWindow", "Robot investment:", None))
        self.btnStartExperiment.setText(_translate("MainWindow", "START", None))
        self.label_8.setText(_translate("MainWindow", "Player investment:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Exp", None))
        self.groupBox.setTitle(_translate("MainWindow", "Connection Box", None))
        self.lineEditNaoIP.setInputMask(_translate("MainWindow", "000.000.000.000", None))
        self.lineEditNaoIP.setText(_translate("MainWindow", "192.168.0.1", None))
        self.label.setText(_translate("MainWindow", "NAO IP Address:", None))
        self.btnConnectToNao.setText(_translate("MainWindow", "Connect", None))
        self.label_3.setText(_translate("MainWindow", "Port:", None))
        self.lineEditNaoPort.setText(_translate("MainWindow", "9559", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "XML file", None))
        self.label_2.setText(_translate("MainWindow", "XML path:", None))
        self.btnBrowse.setText(_translate("MainWindow", "...", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Robt Control", None))
        self.btnWakeUp.setText(_translate("MainWindow", "Init Position", None))
        self.btnRest.setText(_translate("MainWindow", "Rest", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Admin", None))


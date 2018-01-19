# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        ### Create the app window
        MainWindow.setObjectName("MainWindow")

        ### Change the window's size
        MainWindow.resize(1000, 600)

        ### Handle the central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        ### Implement the tabs layout
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-10, -10, 1000, 571))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("QTabBar::tab {\n"
            "    background-color: white;\n"
            "    border-top: 1px solid rgba(0,0,0,0.2);\n"
            "    border-right: 1px solid rgba(0,0,0,0.2);\n"
            "    padding-bottom: 20px;\n"
            "    padding-top: 20px;\n"
            "    color: white;\n"
            "    width : 200px;\n"
            "    height: 50px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected {\n"
            "    background-color: rgba(0,0,0,0.5);"
            "}\n"
            "\n"
            "QTabBar::tab:selected:hover {\n"
            "    background-color: rgba(0,0,0,0.5);"
            "}\n"
            "\n"
            "QTabBar::tab:hover {\n"
            "    background-color:  rgba(0,0,0,0.1);\n"
            "}\n"
            "\n"
            "QTabWidget::tab-bar {\n"
            "    \n"
            "}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

        ### Implement each individual tab
        self.home_tab = QtWidgets.QWidget()
        self.tab = QtWidgets.QWidget()
        self.tabSettings = QtWidgets.QWidget()
        self.tabMonitoring = QtWidgets.QWidget()
        self.home_tab.setObjectName("home_tab")
        self.tab.setObjectName("tab")
        self.tabSettings.setObjectName("tabSettings")
        self.tabMonitoring.setObjectName("tabMonitoring")

        self.tabWidget.addTab(self.home_tab, "")
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.addTab(self.tabMonitoring, "")
        self.tabWidget.addTab(self.tabSettings, "")

        self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHome.png'))
        self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabMonitoring.png'))
        self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabApps.png'))
        self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettings.png'))

        self.tabWidget.tabBar().setTabToolTip(0, "Home")
        self.tabWidget.tabBar().setTabToolTip(1, "Apps")
        self.tabWidget.tabBar().setTabToolTip(2, "Monitoring")
        self.tabWidget.tabBar().setTabToolTip(3, "Settings")

        # self.tabWidget.iconSize(QtCore.QSize(40,40))

        ### Button
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 540, 80, 23))

        ### Menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 813, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        ### Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        ### Central widget
        MainWindow.setCentralWidget(self.centralwidget)

        ### Layout for the home page
        self.groupBoxHome = QtWidgets.QGroupBox(self.home_tab)
        self.groupBoxHome.setGeometry(QtCore.QRect(0, 290, 778, 260))
        self.groupBoxHome.setObjectName("groupBoxHome")

        self.horizontalLayoutHome = QtWidgets.QHBoxLayout(self.groupBoxHome)
        self.horizontalLayoutHome.setObjectName("horizontalLayoutHome")

        ### Text browser
        self.textBrowserHomeInfo = QtWidgets.QTextBrowser(self.groupBoxHome)
        self.textBrowserHomeInfo.setObjectName("textBrowserHomeInfo")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserHomeInfo.sizePolicy().hasHeightForWidth())
        self.textBrowserHomeInfo.setSizePolicy(sizePolicy)
        self.textBrowserHomeInfo.setMaximumSize(QtCore.QSize(250, 16777215))
        self.textBrowserHomeInfo.setText("[ INFORMATIONS ]")
        self.horizontalLayoutHome.addWidget(self.textBrowserHomeInfo)

        ### Buttons for the home page
        self.groupBoxHomeButtons = QtWidgets.QGroupBox(self.groupBoxHome)
        self.groupBoxHomeButtons.setObjectName("groupBoxHomeButtons")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxHomeButtons.sizePolicy().hasHeightForWidth())
        self.groupBoxHomeButtons.setSizePolicy(sizePolicy)
        self.groupBoxHomeButtons.setMaximumSize(QtCore.QSize(250, 16777215))
        self.verticalLayoutHome = QtWidgets.QVBoxLayout(self.groupBoxHomeButtons)
        self.verticalLayoutHome.setObjectName("verticalLayoutHome")

        self.textBrowserSpeedtest = QtWidgets.QTextBrowser(self.groupBoxHome)
        self.textBrowserSpeedtest.setObjectName("textBrowserSpeedtest")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserSpeedtest.sizePolicy().hasHeightForWidth())
        self.textBrowserSpeedtest.setSizePolicy(sizePolicy)
        self.textBrowserSpeedtest.setText(self.readLastSpeedTest())
        self.verticalLayoutHome.addWidget(self.textBrowserSpeedtest)

        self.pushButtonScan = QtWidgets.QPushButton(self.groupBoxHomeButtons)
        self.pushButtonScan.setObjectName("pushButtonScan")
        self.verticalLayoutHome.addWidget(self.pushButtonScan)
        self.pushButtonSpeed = QtWidgets.QPushButton(self.groupBoxHomeButtons)
        self.pushButtonSpeed.setObjectName("pushButtonSpeed")
        self.verticalLayoutHome.addWidget(self.pushButtonSpeed)
        self.horizontalLayoutHome.addWidget(self.groupBoxHomeButtons)

        self.pushButtonSpeed.clicked.connect(self.displaySpeedTest)

        ### Logo for the home page
        self.labelLogo = QtWidgets.QLabel(self.home_tab)
        self.labelLogo.setGeometry(QtCore.QRect(330, 130, 55, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLogo.sizePolicy().hasHeightForWidth())
        self.labelLogo.setSizePolicy(sizePolicy)
        self.labelLogo.setBaseSize(QtCore.QSize(250, 250))
        self.labelLogo.setObjectName("labelLogo")

        ### Ip label
        self.Iplabel = QtWidgets.QLabel(self.home_tab)
        self.Iplabel.setGeometry(QtCore.QRect(600, 10, 185, 20))
        self.Iplabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Iplabel.setObjectName("Iplabel")
        self.Iplabel.setText("Public IP adress: " + External_IP.Get_IP())

        ### Insert items into the application list

        ### Create the application list
        self.list = QtWidgets.QListWidget()

        ### Insert some apps
        # self.createNewAppItem("Test 1");
        # self.createNewAppItem("Test 2");
        # self.createNewAppItem("Test 3");
        self.fillAppList()

        ### Arrange the app list layout
        self.appListLayoutWidget = QtWidgets.QWidget(self.tab)
        self.appListLayoutWidget.setGeometry(QtCore.QRect(20, 60, 411, 481))
        self.appListLayoutWidget.setObjectName("verticalLayoutWidget")
        self.appListLayout = QtWidgets.QVBoxLayout(self.appListLayoutWidget)
        self.appListLayout.setContentsMargins(0, 0, 0, 0)
        self.appListLayout.setObjectName("verticalLayout")
        self.appListLayout.addWidget(self.list)

        ### App search bar
        self.appSearchBar = QtWidgets.QLineEdit(self.tab)
        self.appSearchBar.setGeometry(QtCore.QRect(20, 20, 411, 23))
        self.appSearchBar.setObjectName("appSearchBar")
        self.appSearchBar.textChanged.connect(self.appSearchBarTextChanged)

        #self.window_layout = QtWidgets.QVBoxLayout(self.tab)
        #self.window_layout.addWidget(self.list)
        #self.window_layout.setGeometry(QtCore.QRect(20, 100, 411, 441))
        #self.tab.setLayout(self.window_layout)

        ## Settings tab
        self.openVPNfileDialogButton = QtWidgets.QPushButton()
        self.openVPNfilenameLabel = QtWidgets.QLabel()
        self.openVPNsubmitButton = QtWidgets.QPushButton()

        self.openVPNfileDialogButton.setText("Browse...")
        self.openVPNfilenameLabel.setText("Select VPN certificate: ")
        self.openVPNsubmitButton.setText("Submit")

        ### OpenVPN layout
        self.openVPNlayout = QtWidgets.QVBoxLayout(self.tabSettings)
        self.openVPNlayout.addWidget(self.openVPNfilenameLabel)
        self.openVPNlayout.addWidget(self.openVPNfileDialogButton)
        self.openVPNlayout.addWidget(self.openVPNsubmitButton)

        self.openVPNsubmitButton.setEnabled(False)

        self.openVPNfileDialogButton.clicked.connect(self.selectVPNcertificate)
        self.openVPNsubmitButton.clicked.connect(self.openVPNsubmit)


        ### GUI arrangements
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #self.pushButton_3.clicked.connect(self.addAppClick)

        self.i = 4;


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBoxHome.setTitle(_translate("MainWindow", ""))
        self.groupBoxHomeButtons.setTitle(_translate("MainWindow", ""))
        self.pushButtonScan.setText(_translate("MainWindow", "Scan"))
        self.pushButtonSpeed.setText(_translate("MainWindow", "Speed Test"))

        self.labelLogo.setText(_translate("MainWindow", "Logo"))

        self.pixmap = QtGui.QPixmap(os.getcwd() + 'logo.jpg')
        self.myScaledPixmap = self.pixmap.scaled(self.labelLogo.size(), Qt.KeepAspectRatio)
        self.labelLogo.setPixmap(self.myScaledPixmap)

        self.textBrowserHomeInfo.append("\n\tVitesse: " + "1000000000 km/h");
        self.textBrowserHomeInfo.append("\n\tNombre d'applications actives sur le réseau: "+"1000000000");

        self.appSearchBar.setPlaceholderText(_translate("MainWindow", "Search"))

        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))

    @QtCore.pyqtSlot()
    def addAppClick(self):
        self.createNewAppItem("Test " + str(self.i), {1,2,3})
        self.i+=1

    ### Add a new app item to the application list
    def createNewAppItem(self, processName, PID_list):
        wapp = QtWidgets.QListWidgetItem(self.list)
        wapp.setText(" ")
        wapp_widget = WappWidget()
        wapp_widget.setLabelText(processName)
        wapp_widget.setProcessName(processName)
        wapp_widget.setPIDlist(PID_list)
        wapp.setSizeHint(wapp_widget.sizeHint())
        self.list.addItem(wapp)
        self.list.setItemWidget(wapp, wapp_widget)

    ### Triggers when the app search bar text is changed
    def appSearchBarTextChanged(self):
        print(self.appSearchBar.text())

    def displaySpeedTest(self):
        speedTestResult = SpeedTest.returnSpeedTestResult()

        strST = "Download rate: " + str(float("{0:.2f}".format(speedTestResult["download"] / 1000000))) + "Mb/s\n"
        strST += "Upload rate: " + str(float("{0:.2f}".format(speedTestResult["upload"] / 1000000))) + "Mb/s\n"
        strST += "Ping: " + str(int(speedTestResult["ping"])) + "\n"
        strST += "Server: " + str(speedTestResult["server"]["name"]) + " | " + str(speedTestResult["server"]["country"]) + " | " + str(speedTestResult["server"]["sponsor"]) + "\n"
        strST += str(speedTestResult["timestamp"])

        fh = open("./lastSpeedTest.txt", "w")
        fh.write(strST)
        fh.close()

        self.textBrowserSpeedtest.setText(strST)

    def readLastSpeedTest(self):
        fr = open("./lastSpeedTest.txt", "r")
        strST = fr.read()
        fr.close()
        return strST

    def selectVPNcertificate(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","OpenVPN files (*.ovpn)", options=options)
        self.openVPNfilenameLabel.setText(fileName)
        if(fileName != None):
            self.openVPNsubmitButton.setEnabled(True)

    def openVPNsubmit(self):
        ### TODO : handle openVPN
        print("ok")

    def getAppList(self):
        pidList1 = { 11, 8, 23 }
        pidList2 = { 3 }
        pidList3 = { 98, 278267, 72 }
        pidList4 = { 8337763 }
        listApp = [ { "appname" : "app1", "PID_list" : pidList1 }, { "appname" : "app2", "PID_list" : pidList2 }, { "appname" : "app3", "PID_list" : pidList3 }, { "appname" : "app4", "PID_list" : pidList4 } ]
        return listApp

    def fillAppList(self):
        listApp = self.getAppList()
        for app in listApp:
            self.createNewAppItem(app["appname"], app["PID_list"])


from wapp import WappWidget
import sys
sys.path.append("../Network")
import SpeedTest
import External_IP

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

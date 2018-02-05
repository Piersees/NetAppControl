# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import Qt, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import os
import webbrowser
import threading
import psutil
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
sys.path.append("ui")
from wapp import WappWidget
from gapp import GappWidget
from speedtestwidget import SpeedTestWidget
from VPNstatusWidget import VPNstatusWidget
import time
sys.path.append("../Network")
import External_IP
import ping
import NetworkScan
import openvpn
from Stats import GetPacketStats

class Ui_MainWindow(QtWidgets.QMainWindow):
    bandWidthSig = QtCore.pyqtSignal(int,int)
    pingSig = QtCore.pyqtSignal(str)
    packetsSig = QtCore.pyqtSignal(dict)
    pingLossSig = QtCore.pyqtSignal(str)
    incomingConnectionSig = QtCore.pyqtSignal(dict)
    autoRefreshListSig = QtCore.pyqtSignal(dict)
    deleteGroupSig = QtCore.pyqtSignal(str)
    displayIpSig = QtCore.pyqtSignal(str)
    OpenVpnThread = None
    IP, HOSTNAME, STATUS = range(3)
    nic = None

    appExit = False

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        ### Create the app window
        self.setObjectName("self")

        ### Change the window's size
        self.setFixedSize(985, 560)

        self.setStyleSheet("QInputDialog {background-color: white;} QInputDialog QLabel{color: rgb(41, 107, 116);font-size: 20px; border-bottom: 1px solid rgb(41, 107, 116); }"
        "QInputDialog QLineEdit {"
            "border-top: 0px solid white;"
            "border-left: 0px solid white;"
            "border-right: 0px solid white;"
            "padding-bottom: 5px;"
            "border-bottom: 1px solid #dddddd;"
        "}"
        "QInputDialog QLineEdit:focus{"
            "border-top: 0px solid white;"
            "border-left: 0px solid white;"
            "border-right: 0px solid white;"
            "border-bottom: 2px solid rgb(41, 107, 116);"
        "    padding-bottom: 5px;"
        "}"
        "QInputDialog QLineEdit:selected {"
        "border-top: 0px solid white;"
        "border-left: 0px solid white;"
        "border-right: 0px solid white;"
        "border-bottom: 2px solid rgb(41, 107, 116);"
        "    padding-bottom: 5px;"
        "}"
        "QInputDialog QPushButton{"
        "border-radius: 5px; color: rgb(41, 107, 116); padding: 15px; border: 1px solid rgba(41, 107, 116,1); background-color: rgba(41, 107, 116,0);}"
        "QInputDialog QPushButton:hover{background-color: rgba(41, 107, 116,0.25);}");

        ### Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        ### Set the plots background to white and the axes to black
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ### Handle the central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.thi = 1;
        ### Implement the tabs layout
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-10, -10, 1000, 571))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidgetBar = self.tabWidget.tabBar()
        self.tabWidgetBar.setObjectName("tabWidgetBar")
        self.tabWidget.setStyleSheet("QTabBar#tabWidgetBar::tab {\n"
            "    background-color: white;\n"
            "    border-top: 1px solid rgba(0,0,0,0.2);\n"
            "    border-right: 1px solid rgba(0,0,0,0.2);\n"
            "    padding-bottom: 40px;\n"
            "    padding-top: 20px;\n"
            "    color: white;\n"
            "    width : 200px;\n"
            "    height: 81px;\n"
            "}\n"
            "\n"
            "QTabBar#tabWidgetMonitoringBar::tab {"
            "background-color: rgb(41, 107, 116);"
            "border-left: 1px solid rgba(0,0,0,0.2);"
            "border-bottom: 1px solid rgba(0,0,0,0.2);"
            "padding: 10px;"
            "color: white;"
            "width: 100px;"
            "}"
            "QTabBar#tabWidgetBar::tab:selected, QTabBar#tabWidgetMonitoringBar::tab:hover{\n"
            "    background-color: rgba(41, 107, 116,0.7);"
            "   color: white;"
            "}\n"
            "\n"
            "QTabBar#tabWidgetBar::tab:selected:hover{\n"
            "    background-color: rgba(41, 107, 116, 0.7);"
            "}\n"
            "\n"
            "QTabBar#tabWidgetMonitoringBar::tab:selected, QTabBar#tabWidgetBar::tab:hover, QTabBar#tabWidgetMonitoringBar::tab:selected:hover{\n"
            "    background-color: rgba(41, 107, 116, 0.3);\n"
            "   color: rgb(41, 107, 116);"
            "}\n"
            "\n"
            "QLineEdit {"
                "border-top: 0px solid white;"
                "border-left: 0px solid white;"
                "border-right: 0px solid white;"
                "padding-bottom: 5px;"
                "border-bottom: 1px solid #dddddd;"
            "}"
            "QLineEdit:focus{"
                "border-top: 0px solid white;"
                "border-left: 0px solid white;"
                "border-right: 0px solid white;"
                "border-bottom: 2px solid rgb(41, 107, 116);"
            "    padding-bottom: 5px;"
            "}"
            "QLineEdit:selected {"
            "border-top: 0px solid white;"
            "border-left: 0px solid white;"
            "border-right: 0px solid white;"
            "border-bottom: 2px solid rgb(41, 107, 116);"
            "    padding-bottom: 5px;"
            "}"
            "QPushButton#refreshAppsButton{"
            "width:15px; height:15px;border: 1px solid rgb(41, 107, 116); background-color: rgb(41, 107, 116); border-radius: 14px;"
            "}"
            "QPushButton#refreshAppsButton:hover{"
            "border: 1px solid rgba(41, 107, 116, 0.5); background-color: rgba(41, 107, 116,0.5); border-radius: 14px;"
            "}"
            "QLabel#OpenVPNidFormlabel{"
            "color:rgba(41, 107, 116, 1);"
            "}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

        ### Implement each individual tab
        self.home_tab = QtWidgets.QWidget()
        self.tab = QtWidgets.QWidget()
        self.tabSettings = QtWidgets.QWidget()
        self.tabMonitoring = pg.GraphicsLayoutWidget()
        self.home_tab.setObjectName("home_tab")
        self.tab.setObjectName("tab")
        self.tabSettings.setObjectName("tabSettings")
        self.tabMonitoring.setObjectName("tabMonitoring")


        self.tabWidget.currentChanged.connect(self.onChange)

        self.tabWidget.addTab(self.home_tab, "")
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.addTab(self.tabMonitoring, "")
        self.tabWidget.addTab(self.tabSettings, "")



        ### Implement the tabs layout
        self.tabWidgetMonitoring = QtWidgets.QTabWidget(self.tabMonitoring)
        self.tabWidgetMonitoring.setObjectName("tabWidgetMonitoring")

        self.tabWidgetMonitoringBar = self.tabWidgetMonitoring.tabBar()
        self.tabWidgetMonitoringBar.setObjectName("tabWidgetMonitoringBar")

        self.bwTabMonitoring = pg.GraphicsLayoutWidget()
        self.bwTabConnections = QtWidgets.QWidget()
        self.bwTabSpeedtest = QtWidgets.QWidget()
        self.pkTabMonitoring = pg.GraphicsLayoutWidget()
        self.chTabMonitoring = QtWidgets.QWidget()

        self.bwTabMonitoring.setObjectName("bwTabMonitoring")
        self.bwTabConnections.setObjectName("bwTabConnections")
        self.bwTabSpeedtest.setObjectName("bwTabSpeedtest")
        self.pkTabMonitoring.setObjectName("pkTabMonitoring")
        self.chTabMonitoring.setObjectName("chTabMonitoring")

        self.tabWidgetMonitoring.addTab(self.bwTabMonitoring, "Bandwidth")
        self.tabWidgetMonitoring.addTab(self.bwTabConnections, "Connections")
        self.tabWidgetMonitoring.addTab(self.bwTabSpeedtest, "Speedtest")
        self.tabWidgetMonitoring.addTab(self.pkTabMonitoring, "Packets")
        self.tabWidgetMonitoring.addTab(self.chTabMonitoring, "Channels")


        ## BandWidth graph
        self.BWplot = self.bwTabMonitoring.addPlot(title="Bandwidth over time")
        self.BWplot.setDownsampling(mode='peak')
        #self.BWplot.setClipToView(True)
        self.BWplot.setRange(xRange=[-100, 0])
        self.BWplot.showAxis('bottom', False)
        self.BWplot.addLegend()
        self.dataUL = np.empty(600)
        self.dataDL = np.empty(600)
        self.curveUL = self.BWplot.plot(self.dataUL, fillLevel=-0.25, brush=(200,50,50,100), pen=(255,0,0), name="Upload rate")
        self.curveDL = self.BWplot.plot(self.dataDL, fillLevel=-0.05, brush=(50,50,200,100), pen=(0,0,255), name="Download rate")
        self.BWplot.setLabel('left', "Bandwidth", units='kB')
        self.BWplot.showGrid(x=True, y=True)
        self.ptrBW = 0

        self.BWtextUL = pg.TextItem("test", color=(41, 107, 116), anchor=(1,-0.5))
        self.BWplot.addItem(self.BWtextUL)
        self.BWtextDL = pg.TextItem("test", color=(41, 107, 116), anchor=(1,-1.5))
        self.BWplot.addItem(self.BWtextDL)
        self.BWpercentageVPN = pg.TextItem("test", color=(41, 107, 116), anchor=(1,-2.5))
        self.BWplot.addItem(self.BWpercentageVPN)
        ## Incoming connections tab
        self.incomingConnectionsMainLayout = QVBoxLayout()
        self.bwTabConnections.setLayout(self.incomingConnectionsMainLayout)
        self.incomingConnectionsGroupBox = QGroupBox("Connections on your network")
        self.incomingConnectionsMainLayout.addWidget(self.incomingConnectionsGroupBox)
        self.incomingConnectionsGroupBox.setGeometry(10, 10, self.bwTabConnections.width()-20, self.bwTabConnections.height()-20)
        self.incomingConnectionsList = QTreeView()
        self.incomingConnectionsList.setRootIsDecorated(False)
        self.incomingConnectionsList.setAlternatingRowColors(True)

        self.incomingConnectionsLayout = QHBoxLayout()
        self.incomingConnectionsLayout.addWidget(self.incomingConnectionsList)
        self.incomingConnectionsGroupBox.setLayout(self.incomingConnectionsLayout)

        self.incomingConnectionsModel = self.createConnectionModel()
        self.incomingConnectionsList.setModel(self.incomingConnectionsModel)

        #self.threadIncomingConnections = threading.Thread(target=self.manageConnectionsList)
        #self.threadIncomingConnections.start()

        self.incomingConnectionSig.connect(self.resetConnectionsList)

        ## Speedtest tab
        self.speedtestLayout = QtWidgets.QVBoxLayout()
        self.bwTabSpeedtest.setLayout(self.speedtestLayout)
        self.speedtestWidget = SpeedTestWidget()
        self.speedtestLayout.addWidget(self.speedtestWidget)

        ### Packets bar graph

        self.dpacketsData = {"ALL": 0, "TCP": 0, "UDP": 0, "ARP": 0, "ICMP": 0, "HTTP": 0, "HTTPS": 0, "LLMNR": 0, "DNS": 0, "NBNS": 0, "OTHER": 0}
        self.packetsAxis = [1,2,3,4,5,6,7,8,9,10,11]
        self.pktxdict = {0:' ', 1:'ALL', 2:'TCP', 3:'UDP', 4:'ARP', 5:'ICMP', 6: 'HTTP', 7: 'HTTPS', 8: 'LLMNR', 9: 'DNS', 10: 'NBNS', 11: 'OTHER'}
        self.pktstringaxis = pg.AxisItem(orientation='bottom')
        self.pktstringaxis.setTicks([self.pktxdict.items()])
        self.pkplot = self.pkTabMonitoring.addPlot(title="Packets",axisItems={'bottom': self.pktstringaxis})
        self.packetsData = self.dicToArrayPacketData()
        self.bgALL = pg.BarGraphItem(x=self.packetsAxis ,height=self.packetsData, width=0.3, brush=(41, 107, 116))
        self.pkplot.addItem(self.bgALL)
        self.pkplot.showGrid(x=True, y=True)

        ### Channels pie chart

        self.channelLayout = QtWidgets.QVBoxLayout()
        self.chTabMonitoring.setLayout(self.channelLayout)

        self.chFigure = Figure()
        self.chCanvas = FigureCanvas(self.chFigure)
        self.channelLayout.addWidget(self.chCanvas)

        # self.datapie = wifi_info()
        #
        # for keys, values in self.datapie.items():
        #     print(keys)
        #     print(values)
        self.labelsla = 'Channel 1', 'Channel 2', 'Channel 3'
        self.chSizes = [15, 48, 37]
        self.chExplode = (0 ,0 ,0.1)

        self.chAxis = self.chFigure.add_subplot(111)
        self.chAxis.pie(self.chSizes, explode=self.chExplode, labels=self.labelsla, autopct='%1.1f%%')

        self.chCanvas.draw()


        ### Setting up tab icons
        self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHome.png'))
        self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoringColored.png'))
        self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabAppsColored.png'))
        self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettingsColored.png'))

        self.tabWidget.setIconSize(QSize(60,60))

        self.tabWidget.tabBar().setTabToolTip(0, "Home")
        self.tabWidget.tabBar().setTabToolTip(1, "Apps")
        self.tabWidget.tabBar().setTabToolTip(2, "Monitoring")
        self.tabWidget.tabBar().setTabToolTip(3, "Settings")


        #self.tabWidget.iconSize(QSize(40,40))



        self.bandWidthSig.connect(self.setBandWidthChart)
        self.packetsSig.connect(self.setPacketsChart)

        ### Central widget
        self.setCentralWidget(self.centralwidget)

        ### Layout for the home page
        self.groupBoxHome = QtWidgets.QGroupBox(self.home_tab)
        self.groupBoxHome.setGeometry(QtCore.QRect(-1, 424, 800, 150))
        self.groupBoxHome.setObjectName("groupBoxHome")

        self.horizontalLayoutHome = QtWidgets.QHBoxLayout(self.groupBoxHome)
        self.horizontalLayoutHome.setObjectName("horizontalLayoutHome")

        ### Logo for the home page
        self.labelLogo = QtWidgets.QLabel(self.home_tab)
        self.labelLogo.setGeometry(QtCore.QRect(200, 0, 400, 400))
        pixmapLogo = QtGui.QPixmap('./images/logo.png')
        self.labelLogo.setPixmap(pixmapLogo)
        self.labelLogo.setObjectName("labelLogo")

        ### Network groupbox
        self.NetworkLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayoutHome.addLayout(self.NetworkLayout)

        ### Ip label
        self.Iplabel = QtWidgets.QLabel()
        self.Iplabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Iplabel.setObjectName("Iplabel")
        self.Iplabel.setText("Public IP adress: " + External_IP.Get_IP())
        self.NetworkLayout.addWidget(self.Iplabel)
        self.displayIpSig.connect(self.Iplabel.setText)
        self.threadDisplayIP = threading.Thread(target=self.displayIP)
        self.threadDisplayIP.start()

        ### Ping layout
        self.PingLayout = QtWidgets.QVBoxLayout()
        self.NetworkLayout.addLayout(self.PingLayout)

        ### Ping label
        self.Pinglabel = QtWidgets.QLabel()
        self.Pinglabel.setAlignment(QtCore.Qt.AlignCenter)
        self.Pinglabel.setObjectName("PingLabel")
        self.Pinglabel.setText("Pinging...")
        self.PingLayout.addWidget(self.Pinglabel)

        ### Ping loss label
        self.PingLosslabel = QtWidgets.QLabel()
        self.PingLosslabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PingLosslabel.setObjectName("PingLabel")
        self.PingLosslabel.setText("")
        self.PingLayout.addWidget(self.PingLosslabel)

        self.pingLossSig.connect(self.PingLosslabel.setText)
        self.pingSig.connect(self.Pinglabel.setText)
        self.threadPing = threading.Thread(target=self.pingUpdate)
        self.threadPing.start()

        ### VPN layout
        self.vpnLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayoutHome.addLayout(self.vpnLayout)

        ### VPN status
        self.vpnStatus = VPNstatusWidget()
        self.vpnLayout.addWidget(self.vpnStatus)
        self.vpnStatusThread = threading.Thread(target=self.toggleVPNstatusDisplay)
        self.vpnStatusThread.start()

        ### Stop VPN button
        self.vpnToggleButton1 = QPushButton()
        self.vpnLayout.addWidget(self.vpnToggleButton1)
        self.vpnToggleButton1.clicked.connect(self.toggleVPN)
        self.vpnToggleButton1.setText("Toggle VPN")


        ### About layout
        self.aboutLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayoutHome.addLayout(self.aboutLayout)

        ### About us button
        self.aboutButton = QtWidgets.QPushButton()
        self.aboutButton.setText("About us")
        self.aboutButton.clicked.connect(self.openAbout)
        self.aboutLayout.addWidget(self.aboutButton)

        ### Help button
        self.HelpButton = QtWidgets.QPushButton()
        self.HelpButton.setText("Help")
        self.HelpButton.clicked.connect(self.openHelp)
        self.aboutLayout.addWidget(self.HelpButton)

        ### Create the application list
        self.list = QtWidgets.QListWidget()

        ### Insert items into the application list
        self.fillAppList()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        ### Arrange the app list layout
        self.appListLayoutWidget = QtWidgets.QWidget(self.tab)
        self.appListLayoutWidget.setGeometry(QtCore.QRect(20, 60, 411, 481))
        self.appListLayoutWidget.setObjectName("verticalLayoutWidget")
        self.appListLayout = QtWidgets.QVBoxLayout(self.appListLayoutWidget)
        self.appListLayout.setContentsMargins(0, 0, 0, 0)
        self.appListLayout.setObjectName("verticalLayout")
        self.appListLayout.addWidget(self.list)

        ### Link the selection changed event to a function
        self.list.itemSelectionChanged.connect(self.enableAddToGroupButton)

        ### Create the app groups groupbox
        self.groupBoxAppGroup = QtWidgets.QGroupBox(self.tab)
        self.groupBoxAppGroup.setObjectName("groupBoxAppGroup")
        self.groupBoxAppGroup.setGeometry(QtCore.QRect(450, 60, 320, 481))

        ### Create the app groups groupbox layout
        self.groupMainLayoutWidget = QtWidgets.QVBoxLayout(self.groupBoxAppGroup)
        self.groupMainLayoutWidget.setGeometry(QtCore.QRect(10, 10, 300, 460))
        self.groupMainLayoutWidget.setObjectName("groupMainLayoutWidget")

        ### Create the group list
        self.groupList = QtWidgets.QListWidget()

        ### Create the app group list layout
        self.groupListLayoutWidget = QtWidgets.QWidget()
        self.groupMainLayoutWidget.addWidget(self.groupListLayoutWidget)
        self.groupListLayoutWidget.setGeometry(QtCore.QRect(10, 10, 300, 450))
        self.groupListLayoutWidget.setObjectName("groupListLayoutWidget")
        self.groupListLayout = QtWidgets.QVBoxLayout(self.groupListLayoutWidget)
        self.groupListLayout.setContentsMargins(0, 0, 0, 0)
        self.groupListLayout.setObjectName("groupListLayout")
        self.groupListLayout.addWidget(self.groupList)

        ### Insert groups
        self.addGroups()

        ### Connect the delete event
        self.deleteGroupSig.connect(self.deleteGroup)

        ### Link the selection changed event to a function
        self.groupList.itemSelectionChanged.connect(self.enableAddToGroupButton)

        ### Create the buttons layout
        self.groupAppButtonsLayout = QtWidgets.QHBoxLayout()
        self.groupAppButtonsLayout.setObjectName("groupAppButtonsLayout")
        self.groupMainLayoutWidget.addLayout(self.groupAppButtonsLayout)

        ### Create the add button
        self.buttonGroupAppAdd = QtWidgets.QPushButton()
        self.groupAppButtonsLayout.addWidget(self.buttonGroupAppAdd)
        self.buttonGroupAppAdd.setObjectName("buttonGroupAppAdd")
        self.buttonGroupAppAdd.setText("Add to group")

        ### Create the new group button
        self.buttonGroupAppNew = QtWidgets.QPushButton()
        self.groupAppButtonsLayout.addWidget(self.buttonGroupAppNew)
        self.buttonGroupAppNew.setObjectName("buttonGroupAppNew")
        self.buttonGroupAppNew.setText("New")

        ### Connect the buttons
        self.buttonGroupAppNew.clicked.connect(self.createNewGroup)
        self.buttonGroupAppAdd.clicked.connect(self.addToGroup)
        self.buttonGroupAppAdd.setEnabled(False)


        ### App search bar
        self.appSearchBar = QtWidgets.QLineEdit(self.tab)
        self.appSearchBar.setGeometry(QtCore.QRect(20, 20, 411, 23))
        self.appSearchBar.setObjectName("appSearchBar")
        self.appSearchBar.textChanged.connect(self.appSearchBarTextChanged)

        ### Refresh button
        self.refreshAppsButton = QtWidgets.QPushButton(self.tab)
        self.refreshAppsButton.setGeometry(QtCore.QRect(441, 20, 30, 30))
        self.refreshAppsButton.setObjectName("refreshAppsButton")
        self.refreshAppsButton.setText("")
        self.refreshAppsButton.setIcon(QIcon('./images/refresh.png'))
        self.refreshAppsButton.clicked.connect(self.resetAppList)

        ### Automatically refresh
        self.autoRefreshListSig.connect(self.resetAppListWithDict)
        self.threadAutoRefresh = threading.Thread(target=self.autoRefreshList)
        self.threadAutoRefresh.start()

        ##### Settings tab
        ### Main layout
        self.tabSettingsMainLayout = QtWidgets.QHBoxLayout(self.tabSettings)
        self.tabSettingsMainLayout.setObjectName("tabSettingsMainLayout")
        self.tabSettings.setStyleSheet("")


        ##### Sublayouts
        ### ID layout
        self.openVPNidFormVerticalLayout = QtWidgets.QVBoxLayout()
        self.openVPNidFormVerticalLayout.setObjectName("openVPNidFormVerticalLayout")
        self.tabSettingsMainLayout.addLayout(self.openVPNidFormVerticalLayout)

        ## Title layout label
        self.OpenVPNidFormlabel = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setWeight(0)
        font.setLetterSpacing(QFont.AbsoluteSpacing,2)
        self.OpenVPNidFormlabel.setFont(font)
        self.OpenVPNidFormlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.OpenVPNidFormlabel.setObjectName("OpenVPNidFormlabel")
        self.OpenVPNidFormlabel.setText("Open VPN logins")
        self.OpenVPNidFormlabel.setTextFormat(QtCore.Qt.RichText)
        self.openVPNidFormVerticalLayout.addWidget(self.OpenVPNidFormlabel)


        ## Form layout
        self.OpenVPNidFormLayout = QtWidgets.QFormLayout()
        self.OpenVPNidFormLayout.setObjectName("OpenVPNidFormLayout")
        self.OpenVPNidFormLayout.setContentsMargins(225, -1, 275, 0);
        self.openVPNidFormVerticalLayout.addLayout(self.OpenVPNidFormLayout)

        # Widgets declaration
        self.OpenVPNidLoginLabel = QtWidgets.QLabel()
        self.OpenVPNidLoginInput = QtWidgets.QLineEdit()
        self.OpenVPNidPasswordLabel = QtWidgets.QLabel()
        self.OpenVPNidPasswordInput = QtWidgets.QLineEdit()
        self.OpenVPNidSubmitButton = QtWidgets.QPushButton()

        # Widgets placement
        self.OpenVPNidFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.OpenVPNidLoginLabel)
        self.OpenVPNidFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.OpenVPNidLoginInput)
        self.OpenVPNidFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.OpenVPNidPasswordLabel)
        self.OpenVPNidFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.OpenVPNidPasswordInput)
        self.OpenVPNidFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.OpenVPNidSubmitButton)

        # Wigets naming
        self.OpenVPNidLoginLabel.setText("Login:")
        self.OpenVPNidPasswordLabel.setText("Password:")
        self.OpenVPNidSubmitButton.setText("Submit")

        self.OpenVPNidPasswordInput.setEchoMode(2)

        # Button connecting
        self.OpenVPNidSubmitButton.setEnabled(False)
        self.OpenVPNidSubmitButton.clicked.connect(self.submitOpenVPNid)
        self.OpenVPNidLoginInput.textChanged.connect(self.enableOpenVPNidSubmit)
        self.OpenVPNidPasswordInput.textChanged.connect(self.enableOpenVPNidSubmit)


        self.line = QtWidgets.QFrame();
        self.line.setFrameShape(QtWidgets.QFrame.HLine);
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken);
        self.openVPNidFormVerticalLayout.addWidget(self.line)

        ### Certificate layout
        self.openVPNfileLayout = QtWidgets.QVBoxLayout()
        self.openVPNfileLayout.setObjectName("openVPNfileLayout")
        self.tabSettingsMainLayout.addLayout(self.openVPNfileLayout)

        ## Widgets declaration
        self.openVPNfileDialogButton = QtWidgets.QPushButton()
        self.openVPNfilenameLabel = QtWidgets.QLabel()
        self.openVPNfilenameLabel2 = QtWidgets.QLabel()
        self.openVPNfileDialogButton2 = QtWidgets.QPushButton()
        self.openVPNsubmitButton = QtWidgets.QPushButton()

        ## Widget naming
        self.openVPNfileDialogButton.setText("Browse...")
        self.openVPNfilenameLabel.setText("Select VPN certificate: ")
        self.openVPNfileDialogButton2.setText("Browse...")
        self.openVPNfilenameLabel2.setText("Select second VPN certificate (optional): ")
        self.openVPNsubmitButton.setText("Submit")

        ## Widget placement
        self.openVPNfileLayout = QtWidgets.QFormLayout()
        self.openVPNidFormVerticalLayout.addLayout(self.openVPNfileLayout)
        self.openVPNfileLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.openVPNfilenameLabel)
        self.openVPNfileLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.openVPNfileDialogButton)
        self.openVPNfileLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.openVPNfilenameLabel2)
        self.openVPNfileLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.openVPNfileDialogButton2)
        self.openVPNfileLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.openVPNsubmitButton)
        self.openVPNfileLayout.setContentsMargins(125, -1, 175, 0);


        self.openVPNsubmitButton.setEnabled(False)
        self.openVPNcertificate2Changed = False

        ## Button connections
        self.openVPNfileDialogButton.clicked.connect(self.selectVPNcertificate)
        self.openVPNfileDialogButton2.clicked.connect(self.selectVPNoptionalCertificate)
        self.openVPNsubmitButton.clicked.connect(self.openVPNsubmit)


        ### GUI arrangements
        self.retranslateUi(self)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.autoStartVPN()

    def autoStartVPN(self):
        try:
            fh = open("data/openVPNcertificates.data", "r").read().splitlines()
            certificate = fh[0]
            print(certificate)
            try:
                (self.OpenVpnThread,self.nic) = openvpn.mainVPN(certificate)
                fw = open("data/openVPNcertificates.data", "w")
                fw.write(certificate + "\n")
                if( self.openVPNcertificate2Changed is not False ):
                    certificate2 = self.openVPNfilenameLabel2.text().replace("/",r'\\')
                    fw.write(certificate2 + "\n")
                fw.close()


                for i in range(self.list.count()):
                    wapp = self.list.item(i)
                    self.list.itemWidget(wapp).enableSecurityButton(True)
                    self.list.itemWidget(wapp).setNic(self.nic)


            except(UnboundLocalError):
                msg = QtWidgets.QMessageBox()
                msg.setText("Invalid openVPN certificate")
                msg.exec_()
        except:
            print("no certificate")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "AppVPN"))
        self.bwChartDisplay()
        self.pktChartDisplay()

    @QtCore.pyqtSlot()
    def addAppClick(self):
        for i in range(self.list.count()):
            app_name = self.list.item(i).data(QtCore.Qt.UserRole)

    ### Add a new app item to the application list
    def createNewAppItem(self, processName, PID_list):
        wapp = QtWidgets.QListWidgetItem(self.list)
        wapp.setData(QtCore.Qt.UserRole, processName)
        wapp_widget = WappWidget()
        wapp_widget.setLabelText(processName)
        wapp_widget.setProcessName(processName)
        wapp_widget.setPIDlist(PID_list)
        wapp_widget.setNic(self.nic)
        wapp.setSizeHint(wapp_widget.sizeHint())
        self.list.addItem(wapp)
        self.list.setItemWidget(wapp, wapp_widget)

    ### Triggers when the app search bar text is changed
    def appSearchBarTextChanged(self):
        if(self.appSearchBar.text() == ""):
            for i in range(self.list.count()):
                self.list.item(i).setHidden(False)
        else:
            for i in range(self.list.count()):
                app = self.list.item(i)
                if self.appSearchBar.text().lower() in self.list.itemWidget(app).getLabelText().lower():
                    app.setHidden(False)
                else:
                    app.setHidden(True)

    def bwChartDisplay(self):
        self.threadBW = threading.Thread(target=self.bwChartGetValues)
        self.threadBW.daemon = True
        self.threadBW.start()
    def pktChartDisplay(self):
        self.threadPkt = threading.Thread(target=self.pktChartGetValues)
        self.threadPkt.daemon = True
        self.threadPkt.start()
    def bwChartGetValues(self):
        self.i = 0
        iostat = psutil.net_io_counters(pernic=False, nowrap=True)

        while(self.appExit is not True):
            self.i = 1+self.i
            presc_UL=iostat[0]
            presc_DL=iostat[1]
            iostat = psutil.net_io_counters(pernic=False, nowrap=True)
            upload_rate = (iostat[0] - presc_UL)/1000
            download_rate = (iostat[1] - presc_DL)/1000
            arrayResult = [upload_rate, download_rate]
            up = arrayResult[0]
            down = arrayResult[1]
            self.bandWidthSig.emit(up, down)
            time.sleep(1)
    def pktChartGetValues(self):
        while(self.appExit is not True):
            currentPacketResults = GetPacketStats(self.nic)
            self.packetsSig.emit(currentPacketResults)

    def setBandWidthChart(self, up, down):
        if self.ptrBW == 600:
            self.dataUL[:-1] = self.dataUL[1:]
            self.dataDL[:-1] = self.dataDL[1:]
            self.ptrBW = 599
        self.dataUL[self.ptrBW] = up
        self.dataDL[self.ptrBW] = down

        self.BWtextUL.setText('Current UL speed: %0.1f kB/s' % up)
        self.BWtextDL.setText('Current DL speed: %0.1f kB/s' % down)
        self.BWpercentageVPN.setText('Bandwidth used by VPN: %0.1f %%' % down)

        self.ptrBW += 1
        self.curveUL.setData(self.dataUL[:self.ptrBW])
        self.curveUL.setPos(-self.ptrBW, 0)
        self.curveDL.setData(self.dataDL[:self.ptrBW])
        self.curveDL.setPos(-self.ptrBW, 0)
        #dataUL[:-1] = dataUL[1:] #shift data in the array to the left
        #dataUL[-1] = upload
        #curveUL.setData(dataUL)
        #dataDL[:-1] = dataDL[1:] #shift data in the array to the left
        #dataDL[-1] = download
        #curveDL.setData(dataDL)

    def setPacketsChart(self, packets):
        self.dpacketsData["ALL"] = self.dpacketsData["ALL"] + packets["ALL"]
        self.dpacketsData["TCP"] = self.dpacketsData["TCP"] + packets["TCP"]
        self.dpacketsData["UDP"] = self.dpacketsData["UDP"] + packets["UDP"]
        self.dpacketsData["ARP"] = self.dpacketsData["ARP"] + packets["ARP"]
        self.dpacketsData["ICMP"] = self.dpacketsData["ICMP"] + packets["ICMP"]
        self.dpacketsData["HTTP"] = self.dpacketsData["HTTP"] + packets["HTTP"]
        self.dpacketsData["HTTPS"] = self.dpacketsData["HTTPS"] + packets["HTTPS"]
        self.dpacketsData["LLMNR"] = self.dpacketsData["LLMNR"] + packets["LLMNR"]
        self.dpacketsData["DNS"] = self.dpacketsData["DNS"] + packets["DNS"]
        self.dpacketsData["NBNS"] = self.dpacketsData["NBNS"] + packets["NBNS"]
        self.dpacketsData["OTHER"] = self.dpacketsData["OTHER"] + packets["OTHER"]

        self.packetsData = self.dicToArrayPacketData()
        self.bgALL.setOpts(y=self.packetsData, brush=(41, 107, 116))
        # self.bgTCP.setOpts(y=self.packetsData["TCP"])
        # self.bgUDP.setOpts(y=self.packetsData["UDP"])
        # self.bgARP.setOpts(y=self.packetsData["ARP"])
        # self.bgICMP.setOpts(y=self.packetsData["ICMP"])
        # self.bgHTTP.setOpts(y=self.packetsData["HTTP"])
        # self.bgHTTPS.setOpts(y=self.packetsData["HTTPS"])
        # self.bgLLMNR.setOpts(y=self.packetsData["LLMNR"])
        # self.bgDNS.setOpts(y=self.packetsData["DNS"])
        # self.bgNBNS.setOpts(y=self.packetsData["NBNS"])
        # self.bgOTHER.setOpts(y=self.packetsData["OTHER"])

    def dicToArrayPacketData(self):
        dic = []
        for key in self.dpacketsData:
            dic.append(self.dpacketsData[key])
        return dic

    def selectVPNcertificate(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Select VPN certificate:", "","OpenVPN files (*.ovpn)", options=options)

        if(fileName != None):
            self.openVPNfilenameLabel.setText(fileName)
            self.openVPNsubmitButton.setEnabled(True)

    def selectVPNoptionalCertificate(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Select second VPN certficate:", "","OpenVPN files (*.ovpn)", options=options)

        if(fileName != None):
            self.openVPNfilenameLabel2.setText(fileName)
            self.openVPNcertificate2Changed = True

    def openVPNsubmit(self):
        certificate = self.openVPNfilenameLabel.text().replace("/",r'\\')

        try:
            (self.OpenVpnThread,self.nic) = openvpn.mainVPN(certificate)

            fw = open("data/openVPNcertificates.data", "w")
            fw.write(certificate + "\n")
            if( self.openVPNcertificate2Changed is not False ):
                certificate2 = self.openVPNfilenameLabel2.text().replace("/",r'\\')
                fw.write(certificate2 + "\n")
            fw.close()

            msg = QtWidgets.QMessageBox()
            msg.setText("openVPN certificate registered")
            msg.exec_()


            for i in range(self.list.count()):
                wapp = self.list.item(i)
                self.list.itemWidget(wapp).enableSecurityButton(True)
                self.list.itemWidget(wapp).setNic(self.nic)


        except(UnboundLocalError):
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid openVPN certificate")
            msg.exec_()



    def getAppListWithInternet(self):
        dic = {}
        for proc in psutil.process_iter():
            try :
                process = psutil.Process(proc.pid)
                pname = process.name()
                if proc.connections():
                    if pname not in dic:
                        dic[pname] = [proc.pid]
                    else:
                        dic[pname].append(proc.pid)
            except ( psutil.NoSuchProcess ):
                pass
        return dic

    def fillAppList(self):
        self.listApp = self.getAppListWithInternet()
        for app in self.listApp:
            if ( self.appInWappList(self.listApp, app) is False ):
                self.createNewAppItem(app, self.listApp[app])

    def fillAppListWithDict(self, listApp):
        for app in listApp:
            if ( self.appInWappList(listApp, app) is False ):
                self.createNewAppItem(app, listApp[app])

    def compareWapp(self, wapp, apps, app):
        if(wapp.getProcessName() != app):
            return False
        else:
            if (wapp.getPIDlist() != apps[app]):
                return False
            return True

    def appInWappList(self, apps, app):
        for i in range(self.list.count()):
            wapp = self.list.item(i)
            if( self.compareWapp(self.list.itemWidget(wapp), apps, app) is True ):
                return True
        return False

    def clearList(self):
        apps = self.getAppListWithInternet()
        itemsToRemove = []
        for i in range(self.list.count()):
            wapp = self.list.item(i)
            toDelete = True
            for app in apps:
                if(self.compareWapp(self.list.itemWidget(wapp), apps, app) is True):
                    toDelete = False
            if(toDelete is True):
                itemsToRemove.append(self.list.item(i))
        for item in itemsToRemove:
            self.list.takeItem(self.list.row(item))

    def clearListWithList(self, apps):
        itemsToRemove = []
        for i in range(self.list.count()):
            wapp = self.list.item(i)
            toDelete = True
            for app in apps:
                if(self.compareWapp(self.list.itemWidget(wapp), apps, app) is True):
                    toDelete = False
            if(toDelete is True):
                itemsToRemove.append(self.list.item(i))
        for item in itemsToRemove:
            self.list.takeItem(self.list.row(item))


    def resetAppList(self):
        self.secureForeverSecuredApps()
        # self.clearList()
        # self.fillAppList()
        # self.appSearchBarTextChanged()

    def resetAppListWithDict(self, listApp):
        self.clearListWithList(listApp)
        self.fillAppListWithDict(listApp)
        self.appSearchBarTextChanged()

    def autoRefreshList(self):
        time.sleep(8)
        while(self.appExit is False):
            self.autoRefreshListSig.emit(self.getAppListWithInternet())
            self.secureForeverSecuredApps()
            time.sleep(5)


    def submitOpenVPNid(self):
        fh = open("data/openVPNid.data", "w")
        fh.write(self.OpenVPNidLoginInput.text() + "\n" + self.OpenVPNidPasswordInput.text())
        fh.close()
        msg = QtWidgets.QMessageBox()
        msg.setText("Logins saved")
        msg.exec_()

    def checkIfValidOpenVPNLogins(self):
        if(self.OpenVPNidLoginInput.text() != "" and self.OpenVPNidPasswordInput.text() != ""):
            return True
        else:
            return False

    def enableOpenVPNidSubmit(self):
        if(self.checkIfValidOpenVPNLogins() == True):
            self.OpenVPNidSubmitButton.setEnabled(True)

        else:
            self.OpenVPNidSubmitButton.setEnabled(False)



    def pingUpdate(self):
        packetsSent = 0
        packetsReceived = 0

        while(self.appExit is not True):
            pingResult = ping.getPing()

            if ( pingResult != "lost" and pingResult != None and pingResult != "error"):
                self.pingSig.emit("Ping: " + str(pingResult) + " ms")
                packetsSent += 1
                packetsReceived += 1
            else:
                self.pingSig.emit("Ping: lost")
                packetsSent += 1

            packetLossRatio = 100 - (100*(packetsReceived / packetsSent))
            packetLossRatio = "%.2f" % packetLossRatio
            self.pingLossSig.emit("Loss ratio: " + str(packetLossRatio) + "%")

            time.sleep(1)


    def onChange(self,i): #changed!
        if i == 0:
            self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHome.png'))
            self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoringColored.png'))
            self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabAppsColored.png'))
            self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettingsColored.png'))
        elif i == 2:
            self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoring.png'))
            self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHomeColored.png'))
            self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabAppsColored.png'))
            self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettingsColored.png'))
        elif i == 1:
            self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabApps.png'))
            self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHomeColored.png'))
            self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoringColored.png'))
            self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettingsColored.png'))
        elif i == 3:
            self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettings.png'))
            self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHomeColored.png'))
            self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoringColored.png'))
            self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabAppsColored.png'))

    def createNewGroupWidget(self, name):
        gapp = QtWidgets.QListWidgetItem(self.groupList)
        gapp_widget = GappWidget()
        gapp_widget.setAppList(self.listApp)
        gapp_widget.setName(name)
        gapp_widget.setSignal(self.deleteGroupSig)
        gapp_widget.fillGroup()
        gapp.setSizeHint(gapp_widget.sizeHint())
        self.groupList.addItem(gapp)
        self.groupList.setItemWidget(gapp, gapp_widget)

    def addGroups(self):
        fr = open('data/groups.data', 'r')
        names = []

        for name in fr.readlines():
            self.createNewGroupWidget(name.split("\n")[0])


    def createNewGroup(self):
        fr = open('data/groups.data', 'r')
        groups = fr.readlines()
        fr.close()

        groupName, okPressed = QtWidgets.QInputDialog.getText(self, "New group","New group name:", QtWidgets.QLineEdit.Normal, "")

        alreadyExists = False
        if okPressed and groupName != '':
            for group in groups:
                if (groupName == group.split("\n")[0]):
                    alreadyExists = True

            if alreadyExists is False:
                fw = open('data/groups.data', "a")
                fw.write(groupName + "\n")
                self.createNewGroupWidget(groupName)
                fw.close()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setText("Group already exists")
                msg.exec_()

    def addToGroup(self):
        processes = []
        data_list = []

        for process in self.list.selectedItems():
            processes.append(self.list.itemWidget(process).getLabelText())

        selectedGroup = self.groupList.itemWidget( self.groupList.selectedItems()[0] )
        name = selectedGroup.getName()

        fw = open('data/appGroups.data', 'a')
        fr = open('data/appGroups.data', 'r')
        existingProcesses = fr.readlines()
        fr.close()

        for process in processes:
            alreadyExists = False
            for existingProcess in existingProcesses:
                line = existingProcess.split('|')
                if name in line[0]:
                    if process in line[1]:
                        alreadyExists = True
            if alreadyExists is False:
                data_list.append(name + "|" + process + "\n")
        fw.writelines(data_list)
        fw.close()

        selectedGroup.fillGroup()

    def enableAddToGroupButton(self):
        if(self.list.selectedItems() and self.groupList.selectedItems()):
            self.buttonGroupAppAdd.setEnabled(True)
        else:
            self.buttonGroupAppAdd.setEnabled(False)

    def deleteGroup(self, groupName):
        fg = open('data/groups.data' , 'r')
        group_list = fg.readlines()
        fg.close()
        fg = open('data/appGroups.data', 'r')
        groupApps_list = fg.readlines()
        fg.close()

        insertGroups = []
        insertGroupApps = []

        for group in group_list:
            if ( groupName != group.split("\n")[0] ):
                insertGroups.append(group)
        for groupApp in groupApps_list:
            if ( groupName != groupApp.split("|")[0] ):
                insertGroupApps.append(groupApp)

        fw = open('data/groups.data' , 'w')
        fw.writelines(insertGroups)
        fw.close()
        fw = open('data/appGroups.data', 'w')
        fw.writelines(insertGroupApps)
        fw.close()

        for i in range(self.groupList.count()):
            gapp = self.groupList.item(i)
            if(self.groupList.itemWidget(gapp).getName() == groupName):
                indexToDelete = i

        self.groupList.takeItem(indexToDelete)

    def createConnectionModel(self):
        model = QStandardItemModel(0, 3, self)
        model.setHeaderData(self.IP, Qt.Horizontal, "IP address")
        model.setHeaderData(self.HOSTNAME, Qt.Horizontal, "Hostname")
        model.setHeaderData(self.STATUS, Qt.Horizontal, "Status")
        return model

    def addConnection(self,model, ip, hostname, status):
        self.incomingConnectionsModel.insertRow(0)
        self.incomingConnectionsModel.setData(self.incomingConnectionsModel.index(0, self.IP), ip)
        self.incomingConnectionsModel.setData(self.incomingConnectionsModel.index(0, self.HOSTNAME), hostname)
        self.incomingConnectionsModel.setData(self.incomingConnectionsModel.index(0, self.STATUS), status)

    def addAllConnections(self, incomingConnections):
        for incomingConnection in incomingConnections:
            self.addConnection(self.incomingConnectionsModel, incomingConnection, incomingConnections[incomingConnection]['Hostname'], incomingConnections[incomingConnection]['Status'])

    def deleteAllConnections(self):
        rangeModel = range(self.incomingConnectionsModel.rowCount())
        for i in rangeModel:
            self.incomingConnectionsModel.removeRow(self.incomingConnectionsList.indexAt(QtCore.QPoint(i,0)).row())

    def resetConnectionsList(self, incomingConnections):
        self.deleteAllConnections()
        self.addAllConnections(incomingConnections)

    def manageConnectionsList(self):
        while(self.appExit is False):
            time.sleep(3)
            try :
                self.incomingConnectionSig.emit(NetworkScan.GetHostLan())
            except (TypeError):
                pass

    def getActionsList(self):
        fr = open('data/appsActions.data', 'r')
        actions = fr.readlines()
        fr.close()
        list = []

        for action in actions:
            action = action.rstrip()
            try:
                line = action.split(',')
                list.append({'processName':line[0], 'actionType':line[1], 'durationType':line[2], 'durationTime':line[3]})
            except:
                pass

        return list

    def getGroups(self):
        fr = open('data/appGroups.data', 'r')
        groups = fr.readlines()
        fr.close()
        dic = {}

        for group in groups:
            group = group.rstrip()
            try:
                line = group.split('|')
                if(line[0] not in dic):
                    dic[line[0]] = [line[1]]
                else:
                    dic[line[0]].append(line[1])
            except:
                pass

        return dic

    def secureForeverSecuredApps(self):
        actions = self.getActionsList()
        appList=[]
        # keep a list of running processes
        for i in range(self.list.count()):
            wapp = self.list.item(i)
            app = self.list.itemWidget(wapp)
            appList.append(app)

        groups = []
        for i in range(self.groupList.count()):
            gapp = self.groupList.item(i)
            group = self.groupList.itemWidget(gapp)
            groups.append(group)

        for action in actions:
            if ( (action['actionType'] == "security") and (int(action['durationType']) == 2) ):
                for gapp in groups:
                    try:
                        if(gapp.getName() == action['processName'] and gapp.getSecured() is False):
                            wapps = []
                            for i in range(self.list.count()):
                                wapp = self.list.item(i)
                                app = self.list.itemWidget(wapp)
                                if(app.getProcessName() in gapp.returnGroupNameList()):
                                    wapps.append(app)
                            gapp.groupManageVPN(action['durationType'], action['durationTime'], wapps)
                    except(AttributeError):
                        pass


            if ( (action['actionType'] == "security") and (int(action['durationType']) == 2) ):
                for app in appList:
                    try:
                        if(app.getProcessName() == action['processName'] and app.getSecured() is False):
                            app.manageVPN(action['durationType'], action['durationTime'])
                    except(AttributeError):
                        pass
            if ( (action['actionType'] == "security") and (int(action['durationType']) == 1) ):
                for app in appList:
                    try:
                        if(app.getProcessName() == action['processName'] and app.getSecured() is False):
                            if(self.inTime(action["durationTime"])):
                                app.manageVPN(action['durationType'], action['durationTime'])
                            else:
                                #TO DO: remove from list
                                pass

                    except(AttributeError):
                        pass

    def displayIP(self):
        while(self.appExit is False):
            time.sleep(5)
            self.displayIpSig.emit("Public IP address: " + External_IP.Get_IP())

    def inTime(self, durationTime):
        if time.time() > float(durationTime):
            return False
        else:
            return True


    def stopVPN(self):
        try:
            self.OpenVpnThread.do_run = False
            self.OpenVpnThread.join()
            # Stop the apps' injection
            for i in range(self.list.count()):
                wapp = self.list.item(i)
                self.list.itemWidget(wapp).clean()
        except:
            pass

    def toggleVPNstatusDisplay(self):
        while(self.appExit is False):
            print(self.OpenVpnThread)
            if (self.vpnStatus.getStatus() is False and self.OpenVpnThread != None):
                self.vpnStatus.setActive()
                ### Secure the needed apps in the list
                self.secureForeverSecuredApps()
            if (self.vpnStatus.getStatus() is True and self.OpenVpnThread == None):
                print("Out")
                self.vpnStatus.setInactive()
            time.sleep(1)

    def toggleVPN(self):
        if (self.vpnStatus.getStatus() is False and self.OpenVpnThread != None):
            self.stopVPN()
        if (self.vpnStatus.getStatus() is True and self.OpenVpnThread == None):
            self.autoStartVPN()

    def openAbout(self):
        webbrowser.open('https://github.com/Piersees/NetAppControl')

    def openHelp(self):
        webbrowser.open('https://github.com/Piersees/NetAppControl/blob/master/README.md')

    def closeEvent(self, event):
        if(True):
            self.stopVPN()
            for i in range(self.list.count()):
                wapp = self.list.item(i)
                self.list.itemWidget(wapp).clean()

            self.appExit = True
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

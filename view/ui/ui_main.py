# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QTabWidget, QTextEdit,
    QTreeView, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

from widgets import (CustomTreeView, FileDropWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 719)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setEnabled(True)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"QWidget{\n"
"	color: #333;\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #333;\n"
"	background-color: #f8f8f2;\n"
"	border: 1px solid #CCC;\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(121, 179, 255);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {\n"
"	background-color: #f5f5fa;\n"
"	border: 1px solid #CCC;\n"
"	color: #44475a;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {\n"
"	background-color: #ffffff;\n"
"	border-right: 1px solid #c0c0c0;\n"
"}\n"
"#topLogo {\n"
"	background-color: #ffffff;\n"
"	background-image: url("
                        ":/resources/images/media/gino_logo.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; color: #2f93e1; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: #2f93e1; }\n"
"\n"
"/* MENUS */\n"
"#topMenu {\n"
"	padding-right: 1px;\n"
"}\n"
"#topMenu .QPushButton {\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 18px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: #383838;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: #f2f6ff;\n"
"}\n"
"#topMenu .QPushButton:pressed {\n"
"	background-color: #2f93e1;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: "
                        "44px;\n"
"	color: #4d4d4d;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: #2f93e1;\n"
"}\n"
"#bottomMenu .QPushButton:pressed {\n"
"	background-color: #2f93e1;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 0px solid #ffffff;\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 15px solid transparent;\n"
"	background-color: #ffffff;\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: #f2f6ff;\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: #f2f6ff;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {\n"
"	background-color: #f2f6ff;\n"
"	border-right: 1px solid rgb(224, 224, 224);\n"
"	color: #2f93e1;\n"
"}\n"
"#extraTopBg{\n"
"	background"
                        "-color: #f2f6ff;\n"
"	border-right: 1px solid rgb(224, 224, 224);\n"
"	border-left: 1px solid rgb(224, 224, 224);\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/resources/images/icons/icon_settings_black.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(88, 88, 88); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(161, 196, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(161, 196, 249); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid #2f93e1;\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 18px solid transparent;\n"
""
                        "	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: #2f93e1;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: #ffffff;\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {\n"
"	background-color: rgb(161, 196, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{\n"
"	background-color: #ffffff;\n"
"}\n"
"#contentMain{\n"
"	border-top: 3px solid #2f93e1;\n"
"}\n"
"\n"
"#pagesContainer {\n"
"	background-color: #ffffff;\n"
"}\n"
"#pagesContainer .QFrame {\n"
"	border: none;\n"
"}\n"
"\n"
"#titleRightInfo{\n"
"	color: #0f2c52;\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons QPushButton:hover { background-color: #f2f6ff; border-style: solid; border-radius: 4px; }\n"
"#rightButtons QPushButton:pressed { background-colo"
                        "r: #2f93e1; border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBoxBg {\n"
"	background-color: #ffffff;\n"
"}\n"
"\n"
"#extraRightBoxTopBar QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraRightBoxTopBar QPushButton:hover { background-color: #f2f6ff; border-style: solid; border-radius: 4px; }\n"
"#extraRightBoxTopBar QPushButton:pressed { background-color: #2f93e1; border-style: solid; border-radius: 4px; }\n"
"\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: #beceff }\n"
"#bottomBar QLabel { font-size: 11px; color: #525252; padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: #333333;\n"
""
                        "}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: #2f93e1;\n"
"	color: #f2f6ff;\n"
"}\n"
"#contentSettings .QPushButton:pressed {\n"
"	background-color: #46afff;\n"
"	color: #f2f6ff;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"	border: 3px solid #5e5e5e;\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"	background: #f5f7ff;\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"	border: 3px solid #2f93e1\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"	background: 3px solid #2f93e1;\n"
"	border: 3px solid #2f93e1;\n"
"	background-image: url(:/resources/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"	border: 3px solid #5e5e5e;\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"	background: #f5f7ff;\n"
"}\n"
""
                        "QRadioButton::indicator:hover {\n"
"	border: 3px solid rgb(119, 136, 187);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"	background: 2px solid #2d6d9e;\n"
"	border: 3px solid #2f93e1;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: #ffffff;\n"
"	border-radius: 2px;\n"
"	border: 1px solid #505050;\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"	color: #424242;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 1px solid #2f93e1;\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;\n"
"	background-image: url(:/resources/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"	color: #505050;\n"
"	background-color: #ffffff;\n"
"	padding: 10px;\n"
"	selection-background-"
                        "color: #2f93e1;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"	border-radius: 5px;\n"
"	height: 10px;\n"
"	margin: 0px;\n"
"	background-color: #ffffff;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"	background-color: #2f93e1;\n"
"	border: none;\n"
"	height: 10px;\n"
"	width: 10px;\n"
"	margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"	background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"	background-color: #2f93e1\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"	border-radius: 5px;\n"
"	width: 10px;\n"
"	margin: 0px;\n"
"	background-color: #ffffff;\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: #ffffff;\n"
"}\n"
"QSlider::handle:vertical {\n"
"	background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"	height: 10px;\n"
"	width: 10px;\n"
"	margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:"
                        "vertical:hover {\n"
"	background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"	background-color: #2f93e1;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"#pagesContainer QCommandLinkButton {\n"
"	color: #2f93e1;\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	border: 2px solid #2f93e1;\n"
"	color: #2f93e1\n"
"}\n"
"#pagesContainer QCommandLinkButton:hover {\n"
"	color: #2f93e1;\n"
"	background-color: #ffffff;\n"
"}\n"
"#pagesContainer QCommandLinkButton:pressed {\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: #586796;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"/* #pagesContainer QPushButton { */\n"
"/* 	border: 2px solid #2f93e1; */\n"
"/* 	border-radius: 5px; */\n"
"/* 	background-color: #2f93e1; */\n"
"/* 	color: #f8f8f2; */\n"
"/* } */\n"
"/* #pagesContainer QPushButton:hover { */\n"
""
                        "/* 	background-color: #7082b6; */\n"
"/* 	border: 2px solid #7082b6; */\n"
"/* } */\n"
"\n"
"#pagesContainer QPushButton\n"
"{\n"
"	border: 2px solid #2f93e1;\n"
"	border-radius: 5px;\n"
"	background-color: #2f93e1;\n"
"    color: #f8f8f2;\n"
"	padding: 5px 10px;\n"
"}\n"
"\n"
"#pagesContainer QPushButton:hover\n"
"{\n"
"	background-color: #7082b6;\n"
"	border: 2px solid #7082b6;\n"
"}\n"
"\n"
"#pagesContainer QPushButton:pressed\n"
"{\n"
"	border: 2px solid #2f93e1;\n"
"}\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Custome */\n"
"\n"
"#fileScanDropContainer\n"
"{\n"
"	border: 2px dashed rgb(220, 220, 220);\n"
"	border-radius: 5px;\n"
"}\n"
"")
        self.verticalLayout_21 = QVBoxLayout(self.styleSheet)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.Shape.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Shadow.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.Shape.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.Shape.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Shadow.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.Shape.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Shadow.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        self.titleLeftApp.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftDescription.setFont(font1)
        self.titleLeftDescription.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.topMenu)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.Shape.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Shadow.Plain)
        self.toggleBox.setLineWidth(-1)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.verticalLayout_4.setContentsMargins(0, 2, 0, 0)

        self.verticalLayout_8.addWidget(self.toggleBox)

        self.nav_btn_home = QPushButton(self.topMenu)
        self.nav_btn_home.setObjectName(u"nav_btn_home")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_btn_home.sizePolicy().hasHeightForWidth())
        self.nav_btn_home.setSizePolicy(sizePolicy)
        self.nav_btn_home.setMinimumSize(QSize(0, 45))
        self.nav_btn_home.setFont(font)
        self.nav_btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.nav_btn_home.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.nav_btn_home.setStyleSheet(u"background-image: url(:/heroicons/Home.svg);")
        self.nav_btn_home.setCheckable(False)
        self.nav_btn_home.setChecked(False)

        self.verticalLayout_8.addWidget(self.nav_btn_home)

        self.nav_btn_fileScan = QPushButton(self.topMenu)
        self.nav_btn_fileScan.setObjectName(u"nav_btn_fileScan")
        sizePolicy.setHeightForWidth(self.nav_btn_fileScan.sizePolicy().hasHeightForWidth())
        self.nav_btn_fileScan.setSizePolicy(sizePolicy)
        self.nav_btn_fileScan.setMinimumSize(QSize(0, 45))
        self.nav_btn_fileScan.setFont(font)
        self.nav_btn_fileScan.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.nav_btn_fileScan.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.nav_btn_fileScan.setStyleSheet(u"background-image: url(:/heroicons/DocumentMagnifyingGlass.svg);")

        self.verticalLayout_8.addWidget(self.nav_btn_fileScan)

        self.nav_btn_urlScan = QPushButton(self.topMenu)
        self.nav_btn_urlScan.setObjectName(u"nav_btn_urlScan")
        self.nav_btn_urlScan.setMinimumSize(QSize(0, 45))
        self.nav_btn_urlScan.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.nav_btn_urlScan.setStyleSheet(u"background-image: url(:/heroicons/GlobeAlt.svg);")

        self.verticalLayout_8.addWidget(self.nav_btn_urlScan)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignmentFlag.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/resources/images/icons/icon_settings_black.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)


        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignmentFlag.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.Shape.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Shadow.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.Shape.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.Shape.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Shadow.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/resources/images/icons/cil-x-black.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.extraCloseColumnBtn.setIcon(icon)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.Shape.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_more = QPushButton(self.extraTopMenu)
        self.btn_more.setObjectName(u"btn_more")
        sizePolicy.setHeightForWidth(self.btn_more.sizePolicy().hasHeightForWidth())
        self.btn_more.setSizePolicy(sizePolicy)
        self.btn_more.setMinimumSize(QSize(0, 45))
        self.btn_more.setFont(font)
        self.btn_more.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_more.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_more.setStyleSheet(u"background-image: url(:/resources/images/icons/cil-save-black.png);")

        self.verticalLayout_11.addWidget(self.btn_more)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignmentFlag.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.Shape.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.Shape.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.Shape.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Shadow.Plain)
        self.contentTopBg.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.Shape.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Shadow.Plain)
        self.leftBox.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.leftBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(50, 50))
        self.toggleButton.setMaximumSize(QSize(45, 16777215))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/resources/images/icons/icon_menu_black.png);")

        self.horizontalLayout_3.addWidget(self.toggleButton)

        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.Shape.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/resources/images/icons/icon_settings_black.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settingsTopBtn.setIcon(icon1)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/resources/images/icons/icon_minimize_black.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font2)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/resources/images/icons/icon_maximize_black.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/resources/images/icons/icon_close_black.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeAppBtn.setIcon(icon4)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentMain = QFrame(self.contentBox)
        self.contentMain.setObjectName(u"contentMain")
        self.contentMain.setFrameShape(QFrame.Shape.NoFrame)
        self.contentMain.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentMain)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QStackedWidget(self.contentMain)
        self.content.setObjectName(u"content")
        self.content.setMinimumSize(QSize(300, 0))
        self.content.setFrameShape(QFrame.Shape.NoFrame)
        self.content.setFrameShadow(QFrame.Shadow.Raised)
        self.contentPage2 = QWidget()
        self.contentPage2.setObjectName(u"contentPage2")
        self.contentPage2.setStyleSheet(u"background: rgba(64,64,64,64)")
        self.horizontalLayout_21 = QHBoxLayout(self.contentPage2)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.extraRightBoxBackdrop = QWidget(self.contentPage2)
        self.extraRightBoxBackdrop.setObjectName(u"extraRightBoxBackdrop")
        self.horizontalLayout_16 = QHBoxLayout(self.extraRightBoxBackdrop)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_12)


        self.horizontalLayout_21.addWidget(self.extraRightBoxBackdrop)

        self.extraRightBoxBg = QWidget(self.contentPage2)
        self.extraRightBoxBg.setObjectName(u"extraRightBoxBg")
        self.extraRightBoxBg.setMaximumSize(QSize(0, 16777215))
        self.extraRightBoxBg.setStyleSheet(u"background:white")
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBoxBg)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.extraRightBoxTopBar = QFrame(self.extraRightBoxBg)
        self.extraRightBoxTopBar.setObjectName(u"extraRightBoxTopBar")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.extraRightBoxTopBar.sizePolicy().hasHeightForWidth())
        self.extraRightBoxTopBar.setSizePolicy(sizePolicy3)
        self.extraRightBoxTopBar.setMinimumSize(QSize(400, 0))
        self.horizontalLayout_18 = QHBoxLayout(self.extraRightBoxTopBar)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_extraRightBoxTitle = QLabel(self.extraRightBoxTopBar)
        self.label_extraRightBoxTitle.setObjectName(u"label_extraRightBoxTitle")

        self.horizontalLayout_18.addWidget(self.label_extraRightBoxTitle)

        self.btn_extraRightBoxClose = QPushButton(self.extraRightBoxTopBar)
        self.btn_extraRightBoxClose.setObjectName(u"btn_extraRightBoxClose")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.btn_extraRightBoxClose.sizePolicy().hasHeightForWidth())
        self.btn_extraRightBoxClose.setSizePolicy(sizePolicy4)
        self.btn_extraRightBoxClose.setMinimumSize(QSize(16, 16))
        self.btn_extraRightBoxClose.setMaximumSize(QSize(16, 16))
        self.btn_extraRightBoxClose.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_extraRightBoxClose.setIcon(icon4)
        self.btn_extraRightBoxClose.setIconSize(QSize(20, 20))

        self.horizontalLayout_18.addWidget(self.btn_extraRightBoxClose)

        self.horizontalLayout_18.setStretch(0, 1)

        self.verticalLayout_7.addWidget(self.extraRightBoxTopBar)

        self.extraRightBox = QWidget(self.extraRightBoxBg)
        self.extraRightBox.setObjectName(u"extraRightBox")

        self.verticalLayout_7.addWidget(self.extraRightBox)

        self.verticalLayout_7.setStretch(1, 1)

        self.horizontalLayout_21.addWidget(self.extraRightBoxBg)

        self.content.addWidget(self.contentPage2)
        self.contentPage1 = QWidget()
        self.contentPage1.setObjectName(u"contentPage1")
        self.horizontalLayout_4 = QHBoxLayout(self.contentPage1)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.contentPage1)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.verticalLayout_28 = QVBoxLayout(self.home)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.groupBox_6 = QGroupBox(self.home)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.horizontalLayout_23 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.groupBox_7 = QGroupBox(self.groupBox_6)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.verticalLayout_30 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox_7)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_filesScanned = QLabel(self.groupBox_7)
        self.label_filesScanned.setObjectName(u"label_filesScanned")
        self.label_filesScanned.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_filesScanned)

        self.label_4 = QLabel(self.groupBox_7)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.label_5 = QLabel(self.groupBox_7)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_5)

        self.label_8 = QLabel(self.groupBox_7)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_8)

        self.label_threatsDetected = QLabel(self.groupBox_7)
        self.label_threatsDetected.setObjectName(u"label_threatsDetected")
        self.label_threatsDetected.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.label_threatsDetected)


        self.verticalLayout_30.addLayout(self.formLayout)


        self.horizontalLayout_23.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.groupBox_6)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.tabWidget = QTabWidget(self.groupBox_8)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_14 = QHBoxLayout(self.tab)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.tbl_mostDetectedVirus = QTreeView(self.tab)
        self.tbl_mostDetectedVirus.setObjectName(u"tbl_mostDetectedVirus")
        self.tbl_mostDetectedVirus.setAlternatingRowColors(True)

        self.horizontalLayout_14.addWidget(self.tbl_mostDetectedVirus)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_14 = QVBoxLayout(self.tab_2)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.tbl_recentlyDetectedVirus = QTreeView(self.tab_2)
        self.tbl_recentlyDetectedVirus.setObjectName(u"tbl_recentlyDetectedVirus")
        self.tbl_recentlyDetectedVirus.setAlternatingRowColors(True)

        self.verticalLayout_14.addWidget(self.tbl_recentlyDetectedVirus)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_7.addWidget(self.tabWidget)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer)

        self.label_2 = QLabel(self.groupBox_8)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_13.addWidget(self.label_2)

        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.op_TopThreatsfilterAll = QRadioButton(self.groupBox_8)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.op_TopThreatsfilterAll)
        self.op_TopThreatsfilterAll.setObjectName(u"op_TopThreatsfilterAll")
        self.op_TopThreatsfilterAll.setChecked(True)

        self.verticalLayout_18.addWidget(self.op_TopThreatsfilterAll)

        self.op_TopThreatsfilterFiles = QRadioButton(self.groupBox_8)
        self.buttonGroup.addButton(self.op_TopThreatsfilterFiles)
        self.op_TopThreatsfilterFiles.setObjectName(u"op_TopThreatsfilterFiles")

        self.verticalLayout_18.addWidget(self.op_TopThreatsfilterFiles)

        self.op_TopThreatsfilterURLs = QRadioButton(self.groupBox_8)
        self.buttonGroup.addButton(self.op_TopThreatsfilterURLs)
        self.op_TopThreatsfilterURLs.setObjectName(u"op_TopThreatsfilterURLs")

        self.verticalLayout_18.addWidget(self.op_TopThreatsfilterURLs)


        self.verticalLayout_13.addLayout(self.verticalLayout_18)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_2)


        self.horizontalLayout_7.addLayout(self.verticalLayout_13)


        self.horizontalLayout_23.addWidget(self.groupBox_8)

        self.horizontalLayout_23.setStretch(0, 1)
        self.horizontalLayout_23.setStretch(1, 2)

        self.verticalLayout_28.addWidget(self.groupBox_6)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.groupBox_5 = QGroupBox(self.home)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_29 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.tbl_fileScanResults = QTreeView(self.groupBox_5)
        self.tbl_fileScanResults.setObjectName(u"tbl_fileScanResults")
        self.tbl_fileScanResults.setAlternatingRowColors(True)

        self.verticalLayout_29.addWidget(self.tbl_fileScanResults)


        self.horizontalLayout_24.addWidget(self.groupBox_5)

        self.groupBox_9 = QGroupBox(self.home)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_31 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.tbl_latestURLScanResults = QTreeView(self.groupBox_9)
        self.tbl_latestURLScanResults.setObjectName(u"tbl_latestURLScanResults")
        self.tbl_latestURLScanResults.setAlternatingRowColors(True)

        self.verticalLayout_31.addWidget(self.tbl_latestURLScanResults)


        self.horizontalLayout_24.addWidget(self.groupBox_9)


        self.verticalLayout_28.addLayout(self.horizontalLayout_24)

        self.stackedWidget.addWidget(self.home)
        self.page_fileScan2 = QWidget()
        self.page_fileScan2.setObjectName(u"page_fileScan2")
        self.verticalLayout_27 = QVBoxLayout(self.page_fileScan2)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.groupBox_4 = QGroupBox(self.page_fileScan2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_26 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.fileScanDropContainer = QWidget(self.groupBox_4)
        self.fileScanDropContainer.setObjectName(u"fileScanDropContainer")
        self._2 = QVBoxLayout(self.fileScanDropContainer)
        self._2.setObjectName(u"_2")
        self._2.setContentsMargins(9, 9, 9, 9)
        self.fileScanDrop = FileDropWidget(self.fileScanDropContainer)
        self.fileScanDrop.setObjectName(u"fileScanDrop")
        self.fileScanDrop.setMinimumSize(QSize(0, 100))
        self.fileScanDrop.setAcceptDrops(True)
        self.horizontalLayout_15 = QHBoxLayout(self.fileScanDrop)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.btn_fileSelect = QPushButton(self.fileScanDrop)
        self.btn_fileSelect.setObjectName(u"btn_fileSelect")
        sizePolicy4.setHeightForWidth(self.btn_fileSelect.sizePolicy().hasHeightForWidth())
        self.btn_fileSelect.setSizePolicy(sizePolicy4)
        icon5 = QIcon()
        icon5.addFile(u":/resources/images/icons/file_plus_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_fileSelect.setIcon(icon5)

        self.horizontalLayout_15.addWidget(self.btn_fileSelect)


        self._2.addWidget(self.fileScanDrop)


        self.verticalLayout_26.addWidget(self.fileScanDropContainer)

        self.tbl_fileScanList = CustomTreeView(self.groupBox_4)
        self.tbl_fileScanList.setObjectName(u"tbl_fileScanList")
        self.tbl_fileScanList.setAlternatingRowColors(True)
        self.tbl_fileScanList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.verticalLayout_26.addWidget(self.tbl_fileScanList)


        self.verticalLayout_27.addWidget(self.groupBox_4)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setSpacing(20)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_16)

        self.btn_startFileScan = QPushButton(self.page_fileScan2)
        self.btn_startFileScan.setObjectName(u"btn_startFileScan")
        sizePolicy4.setHeightForWidth(self.btn_startFileScan.sizePolicy().hasHeightForWidth())
        self.btn_startFileScan.setSizePolicy(sizePolicy4)
        self.btn_startFileScan.setMinimumSize(QSize(100, 0))
        icon6 = QIcon()
        icon6.addFile(u":/resources/images/icons/play_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_startFileScan.setIcon(icon6)

        self.horizontalLayout_22.addWidget(self.btn_startFileScan)

        self.btn_stopFileScan = QPushButton(self.page_fileScan2)
        self.btn_stopFileScan.setObjectName(u"btn_stopFileScan")
        sizePolicy4.setHeightForWidth(self.btn_stopFileScan.sizePolicy().hasHeightForWidth())
        self.btn_stopFileScan.setSizePolicy(sizePolicy4)
        self.btn_stopFileScan.setMinimumSize(QSize(100, 0))
        icon7 = QIcon()
        icon7.addFile(u":/resources/images/icons/rectangle_white.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_stopFileScan.setIcon(icon7)

        self.horizontalLayout_22.addWidget(self.btn_stopFileScan)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_17)


        self.verticalLayout_27.addLayout(self.horizontalLayout_22)

        self.stackedWidget.addWidget(self.page_fileScan2)
        self.page_urlScan = QWidget()
        self.page_urlScan.setObjectName(u"page_urlScan")
        self.verticalLayout_16 = QVBoxLayout(self.page_urlScan)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.groupBox_2 = QGroupBox(self.page_urlScan)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.input_url = QLineEdit(self.groupBox_2)
        self.input_url.setObjectName(u"input_url")

        self.horizontalLayout_9.addWidget(self.input_url)

        self.btn_urlScan = QPushButton(self.groupBox_2)
        self.btn_urlScan.setObjectName(u"btn_urlScan")
        self.btn_urlScan.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.btn_urlScan)


        self.verticalLayout_16.addWidget(self.groupBox_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBox = QGroupBox(self.page_urlScan)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.tbl_urlDetails = QTreeWidget(self.groupBox)
        self.tbl_urlDetails.setObjectName(u"tbl_urlDetails")
        self.tbl_urlDetails.setAlternatingRowColors(True)

        self.verticalLayout_17.addWidget(self.tbl_urlDetails)


        self.horizontalLayout_6.addWidget(self.groupBox)

        self.groupBox_urlScanResult = QGroupBox(self.page_urlScan)
        self.groupBox_urlScanResult.setObjectName(u"groupBox_urlScanResult")
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_urlScanResult)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_6 = QLabel(self.groupBox_urlScanResult)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_10.addWidget(self.label_6)

        self.label_urlScanStatus = QLabel(self.groupBox_urlScanResult)
        self.label_urlScanStatus.setObjectName(u"label_urlScanStatus")

        self.horizontalLayout_10.addWidget(self.label_urlScanStatus)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)

        self.label_7 = QLabel(self.groupBox_urlScanResult)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_7)

        self.label_urlScanDetection = QLabel(self.groupBox_urlScanResult)
        self.label_urlScanDetection.setObjectName(u"label_urlScanDetection")

        self.horizontalLayout_10.addWidget(self.label_urlScanDetection)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)


        self.verticalLayout_23.addLayout(self.horizontalLayout_10)

        self.tbl_urlScanResult = QTreeWidget(self.groupBox_urlScanResult)
        self.tbl_urlScanResult.setObjectName(u"tbl_urlScanResult")
        self.tbl_urlScanResult.setAlternatingRowColors(True)

        self.verticalLayout_23.addWidget(self.tbl_urlScanResult)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_7)

        self.label_3 = QLabel(self.groupBox_urlScanResult)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_11.addWidget(self.label_3)

        self.label_urlScanElapsedTime = QLabel(self.groupBox_urlScanResult)
        self.label_urlScanElapsedTime.setObjectName(u"label_urlScanElapsedTime")

        self.horizontalLayout_11.addWidget(self.label_urlScanElapsedTime)


        self.verticalLayout_23.addLayout(self.horizontalLayout_11)


        self.horizontalLayout_6.addWidget(self.groupBox_urlScanResult)


        self.verticalLayout_16.addLayout(self.horizontalLayout_6)

        self.stackedWidget.addWidget(self.page_urlScan)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.content.addWidget(self.contentPage1)

        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentMain)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setBold(False)
        font3.setItalic(False)
        self.creditsLabel.setFont(font3)
        self.creditsLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentMain)


        self.appLayout.addWidget(self.contentBox)


        self.verticalLayout_21.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.content.setCurrentIndex(1)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"Genius Software", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"Invoice App", None))
        self.nav_btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.nav_btn_fileScan.setText(QCoreApplication.translate("MainWindow", u"File Scan", None))
        self.nav_btn_urlScan.setText(QCoreApplication.translate("MainWindow", u"URL Scan", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"Left Box", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.btn_more.setText(QCoreApplication.translate("MainWindow", u"More", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#0055ff;\">GUI With PySide</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#454544;\">An interface created using Python and PySide (support for PyQt), and with colors based on the Dracula theme created "
                        "by Zeno Rocha.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#454544;\">MIT License</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#0055ff;\">Convert UI</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#483d37;\">pyside6-uic main.ui -o ui_main.py</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#0055ff;\">Convert QRC</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0"
                        "px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#483d37;\">pyside6-rcc resources.qrc -o resources_rc.py</span></p></body></html>", None))
        self.toggleButton.setText("")
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"Scan-X // Malware Scanning and Analysis Tool", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.label_extraRightBoxTitle.setText("")
#if QT_CONFIG(tooltip)
        self.btn_extraRightBoxClose.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.btn_extraRightBoxClose.setText("")
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Analysis Stats", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Summary", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Files scanned:", None))
        self.label_filesScanned.setText(QCoreApplication.translate("MainWindow", u"999", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"URLs scanned:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"999", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Threats detected:", None))
        self.label_threatsDetected.setText(QCoreApplication.translate("MainWindow", u"999,999", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Top Threats", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Most detected", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Recently detected", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Filter By:", None))
        self.op_TopThreatsfilterAll.setText(QCoreApplication.translate("MainWindow", u"All", None))
        self.op_TopThreatsfilterFiles.setText(QCoreApplication.translate("MainWindow", u"Files", None))
        self.op_TopThreatsfilterURLs.setText(QCoreApplication.translate("MainWindow", u"URLs", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Latest File Scan Results", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Latest URL Scan Results", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Scan files", None))
        self.btn_fileSelect.setText(QCoreApplication.translate("MainWindow", u"Select file...", None))
        self.btn_startFileScan.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btn_stopFileScan.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"URL Scan", None))
        self.input_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"https://", None))
        self.btn_urlScan.setText(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"URL Details", None))
        ___qtreewidgetitem = self.tbl_urlDetails.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Value", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Property", None));
        self.groupBox_urlScanResult.setTitle(QCoreApplication.translate("MainWindow", u"Analysis Results", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
        self.label_urlScanStatus.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Detection:", None))
        self.label_urlScanDetection.setText("")
        ___qtreewidgetitem1 = self.tbl_urlScanResult.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow", u"Result", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Vendor", None));
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Elapsed time:", None))
        self.label_urlScanElapsedTime.setText("")
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"Developed by Pang Hoi Him (220327019)", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"Scan-X version 1.0.0", None))
    # retranslateUi


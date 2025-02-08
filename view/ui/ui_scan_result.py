# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'scan_result.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QSizePolicy, QSpacerItem, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)
import resources_rc

class Ui_ScanResult(object):
    def setupUi(self, ScanResult):
        if not ScanResult.objectName():
            ScanResult.setObjectName(u"ScanResult")
        ScanResult.resize(400, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(ScanResult.sizePolicy().hasHeightForWidth())
        ScanResult.setSizePolicy(sizePolicy)
        ScanResult.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout_2 = QVBoxLayout(ScanResult)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 0, 10, 10)
        self.groupBox_details = QGroupBox(ScanResult)
        self.groupBox_details.setObjectName(u"groupBox_details")
        self.verticalLayout_21 = QVBoxLayout(self.groupBox_details)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.tbl_details = QTreeWidget(self.groupBox_details)
        self.tbl_details.setObjectName(u"tbl_details")
        self.tbl_details.setMaximumSize(QSize(16777215, 150))
        self.tbl_details.setAlternatingRowColors(True)

        self.verticalLayout_21.addWidget(self.tbl_details)


        self.verticalLayout.addWidget(self.groupBox_details)

        self.groupBox_scanResult = QGroupBox(ScanResult)
        self.groupBox_scanResult.setObjectName(u"groupBox_scanResult")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_scanResult.sizePolicy().hasHeightForWidth())
        self.groupBox_scanResult.setSizePolicy(sizePolicy1)
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_scanResult)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.groupBox_scanResult)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.label_status = QLabel(self.groupBox_scanResult)
        self.label_status.setObjectName(u"label_status")

        self.horizontalLayout_7.addWidget(self.label_status)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.label_4 = QLabel(self.groupBox_scanResult)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label_4.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_4)

        self.label_detection = QLabel(self.groupBox_scanResult)
        self.label_detection.setObjectName(u"label_detection")

        self.horizontalLayout_7.addWidget(self.label_detection)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)


        self.verticalLayout_22.addLayout(self.horizontalLayout_7)

        self.tbl_analysisResults = QTreeWidget(self.groupBox_scanResult)
        self.tbl_analysisResults.setObjectName(u"tbl_analysisResults")
        self.tbl_analysisResults.setAlternatingRowColors(True)

        self.verticalLayout_22.addWidget(self.tbl_analysisResults)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)

        self.label = QLabel(self.groupBox_scanResult)
        self.label.setObjectName(u"label")

        self.horizontalLayout_8.addWidget(self.label)

        self.label_elapsedTime = QLabel(self.groupBox_scanResult)
        self.label_elapsedTime.setObjectName(u"label_elapsedTime")

        self.horizontalLayout_8.addWidget(self.label_elapsedTime)


        self.verticalLayout_22.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addWidget(self.groupBox_scanResult)

        self.verticalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2.setStretch(0, 1)

        self.retranslateUi(ScanResult)

        QMetaObject.connectSlotsByName(ScanResult)
    # setupUi

    def retranslateUi(self, ScanResult):
        ScanResult.setWindowTitle(QCoreApplication.translate("ScanResult", u"Form", None))
        self.groupBox_details.setTitle(QCoreApplication.translate("ScanResult", u"Details", None))
        ___qtreewidgetitem = self.tbl_details.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("ScanResult", u"Value", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("ScanResult", u"Property", None));
        self.groupBox_scanResult.setTitle(QCoreApplication.translate("ScanResult", u"Analysis Results", None))
        self.label_5.setText(QCoreApplication.translate("ScanResult", u"Status:", None))
        self.label_status.setText("")
        self.label_4.setText(QCoreApplication.translate("ScanResult", u"Detection:", None))
        self.label_detection.setText("")
        ___qtreewidgetitem1 = self.tbl_analysisResults.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("ScanResult", u"Result", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("ScanResult", u"Engine", None));
        self.label.setText(QCoreApplication.translate("ScanResult", u"Elapsed time:", None))
        self.label_elapsedTime.setText("")
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_details.ui'
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

class Ui_FileDetails(object):
    def setupUi(self, FileDetails):
        if not FileDetails.objectName():
            FileDetails.setObjectName(u"FileDetails")
        FileDetails.resize(400, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(FileDetails.sizePolicy().hasHeightForWidth())
        FileDetails.setSizePolicy(sizePolicy)
        FileDetails.setMaximumSize(QSize(400, 16777215))
        self.verticalLayout_2 = QVBoxLayout(FileDetails)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 0, 10, 10)
        self.groupBox_fileInfo = QGroupBox(FileDetails)
        self.groupBox_fileInfo.setObjectName(u"groupBox_fileInfo")
        self.verticalLayout_21 = QVBoxLayout(self.groupBox_fileInfo)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.tbl_fileInfo = QTreeWidget(self.groupBox_fileInfo)
        self.tbl_fileInfo.setObjectName(u"tbl_fileInfo")

        self.verticalLayout_21.addWidget(self.tbl_fileInfo)


        self.verticalLayout.addWidget(self.groupBox_fileInfo)

        self.groupBox_fileScanResult = QGroupBox(FileDetails)
        self.groupBox_fileScanResult.setObjectName(u"groupBox_fileScanResult")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_fileScanResult.sizePolicy().hasHeightForWidth())
        self.groupBox_fileScanResult.setSizePolicy(sizePolicy1)
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_fileScanResult)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.groupBox_fileScanResult)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.label_fileScanStatus = QLabel(self.groupBox_fileScanResult)
        self.label_fileScanStatus.setObjectName(u"label_fileScanStatus")

        self.horizontalLayout_7.addWidget(self.label_fileScanStatus)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.label_4 = QLabel(self.groupBox_fileScanResult)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label_4.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_4)

        self.label_fileScanDetection = QLabel(self.groupBox_fileScanResult)
        self.label_fileScanDetection.setObjectName(u"label_fileScanDetection")

        self.horizontalLayout_7.addWidget(self.label_fileScanDetection)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)


        self.verticalLayout_22.addLayout(self.horizontalLayout_7)

        self.tbl_fileScanResult = QTreeWidget(self.groupBox_fileScanResult)
        self.tbl_fileScanResult.setObjectName(u"tbl_fileScanResult")
        self.tbl_fileScanResult.setAlternatingRowColors(True)

        self.verticalLayout_22.addWidget(self.tbl_fileScanResult)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)

        self.label = QLabel(self.groupBox_fileScanResult)
        self.label.setObjectName(u"label")

        self.horizontalLayout_8.addWidget(self.label)

        self.label_fileScanElapsedTime = QLabel(self.groupBox_fileScanResult)
        self.label_fileScanElapsedTime.setObjectName(u"label_fileScanElapsedTime")

        self.horizontalLayout_8.addWidget(self.label_fileScanElapsedTime)


        self.verticalLayout_22.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addWidget(self.groupBox_fileScanResult)

        self.verticalLayout.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2.setStretch(0, 1)

        self.retranslateUi(FileDetails)

        QMetaObject.connectSlotsByName(FileDetails)
    # setupUi

    def retranslateUi(self, FileDetails):
        FileDetails.setWindowTitle(QCoreApplication.translate("FileDetails", u"Form", None))
        self.groupBox_fileInfo.setTitle(QCoreApplication.translate("FileDetails", u"File Details", None))
        ___qtreewidgetitem = self.tbl_fileInfo.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("FileDetails", u"Value", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("FileDetails", u"Property", None));
        self.groupBox_fileScanResult.setTitle(QCoreApplication.translate("FileDetails", u"Analysis Results", None))
        self.label_5.setText(QCoreApplication.translate("FileDetails", u"Status:", None))
        self.label_fileScanStatus.setText("")
        self.label_4.setText(QCoreApplication.translate("FileDetails", u"Detection:", None))
        self.label_fileScanDetection.setText("")
        ___qtreewidgetitem1 = self.tbl_fileScanResult.headerItem()
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("FileDetails", u"Result", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("FileDetails", u"Engine", None));
        self.label.setText(QCoreApplication.translate("FileDetails", u"Elapsed time:", None))
        self.label_fileScanElapsedTime.setText("")
    # retranslateUi


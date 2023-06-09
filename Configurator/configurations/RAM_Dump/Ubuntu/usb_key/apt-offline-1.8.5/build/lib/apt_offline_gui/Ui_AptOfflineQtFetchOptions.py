# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AptOfflineQtFetchOptions.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_downloadOptionsDialog(object):
    def setupUi(self, downloadOptionsDialog):
        downloadOptionsDialog.setObjectName("downloadOptionsDialog")
        downloadOptionsDialog.resize(443, 304)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(downloadOptionsDialog.sizePolicy().hasHeightForWidth())
        downloadOptionsDialog.setSizePolicy(sizePolicy)
        downloadOptionsDialog.setMinimumSize(QtCore.QSize(443, 304))
        downloadOptionsDialog.setMaximumSize(QtCore.QSize(443, 304))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/configure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        downloadOptionsDialog.setWindowIcon(icon)
        downloadOptionsDialog.setSizeGripEnabled(False)
        downloadOptionsDialog.setModal(True)
        self.lblThreads = QtWidgets.QLabel(downloadOptionsDialog)
        self.lblThreads.setGeometry(QtCore.QRect(255, 10, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblThreads.setFont(font)
        self.lblThreads.setObjectName("lblThreads")
        self.spinThreads = QtWidgets.QSpinBox(downloadOptionsDialog)
        self.spinThreads.setGeometry(QtCore.QRect(338, 9, 90, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinThreads.sizePolicy().hasHeightForWidth())
        self.spinThreads.setSizePolicy(sizePolicy)
        self.spinThreads.setMinimum(1)
        self.spinThreads.setMaximum(10)
        self.spinThreads.setObjectName("spinThreads")
        self.downloadOptionDialogOkButton = QtWidgets.QPushButton(downloadOptionsDialog)
        self.downloadOptionDialogOkButton.setGeometry(QtCore.QRect(350, 260, 81, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/dialog-ok-apply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.downloadOptionDialogOkButton.setIcon(icon1)
        self.downloadOptionDialogOkButton.setObjectName("downloadOptionDialogOkButton")
        self.lblSocketTimeo = QtWidgets.QLabel(downloadOptionsDialog)
        self.lblSocketTimeo.setGeometry(QtCore.QRect(10, 8, 110, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblSocketTimeo.setFont(font)
        self.lblSocketTimeo.setObjectName("lblSocketTimeo")
        self.spinTimeout = QtWidgets.QSpinBox(downloadOptionsDialog)
        self.spinTimeout.setGeometry(QtCore.QRect(119, 7, 100, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinTimeout.sizePolicy().hasHeightForWidth())
        self.spinTimeout.setSizePolicy(sizePolicy)
        self.spinTimeout.setMinimum(10)
        self.spinTimeout.setMaximum(100)
        self.spinTimeout.setProperty("value", 30)
        self.spinTimeout.setObjectName("spinTimeout")
        self.cacheDirLineEdit = QtWidgets.QLineEdit(downloadOptionsDialog)
        self.cacheDirLineEdit.setGeometry(QtCore.QRect(120, 60, 221, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cacheDirLineEdit.sizePolicy().hasHeightForWidth())
        self.cacheDirLineEdit.setSizePolicy(sizePolicy)
        self.cacheDirLineEdit.setObjectName("cacheDirLineEdit")
        self.cacheDirBrowseButton = QtWidgets.QPushButton(downloadOptionsDialog)
        self.cacheDirBrowseButton.setGeometry(QtCore.QRect(350, 60, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cacheDirBrowseButton.sizePolicy().hasHeightForWidth())
        self.cacheDirBrowseButton.setSizePolicy(sizePolicy)
        self.cacheDirBrowseButton.setObjectName("cacheDirBrowseButton")
        self.lblCacheDir = QtWidgets.QLabel(downloadOptionsDialog)
        self.lblCacheDir.setGeometry(QtCore.QRect(10, 60, 91, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCacheDir.sizePolicy().hasHeightForWidth())
        self.lblCacheDir.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblCacheDir.setFont(font)
        self.lblCacheDir.setObjectName("lblCacheDir")
        self.disableChecksumCheckBox = QtWidgets.QCheckBox(downloadOptionsDialog)
        self.disableChecksumCheckBox.setGeometry(QtCore.QRect(10, 120, 151, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.disableChecksumCheckBox.sizePolicy().hasHeightForWidth())
        self.disableChecksumCheckBox.setSizePolicy(sizePolicy)
        self.disableChecksumCheckBox.setObjectName("disableChecksumCheckBox")
        self.fetchBugReportsCheckBox = QtWidgets.QCheckBox(downloadOptionsDialog)
        self.fetchBugReportsCheckBox.setGeometry(QtCore.QRect(180, 120, 151, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fetchBugReportsCheckBox.sizePolicy().hasHeightForWidth())
        self.fetchBugReportsCheckBox.setSizePolicy(sizePolicy)
        self.fetchBugReportsCheckBox.setObjectName("fetchBugReportsCheckBox")
        self.proxyGroupBox = QtWidgets.QGroupBox(downloadOptionsDialog)
        self.proxyGroupBox.setGeometry(QtCore.QRect(9, 169, 421, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxyGroupBox.sizePolicy().hasHeightForWidth())
        self.proxyGroupBox.setSizePolicy(sizePolicy)
        self.proxyGroupBox.setStyleSheet("")
        self.proxyGroupBox.setTitle("")
        self.proxyGroupBox.setFlat(True)
        self.proxyGroupBox.setObjectName("proxyGroupBox")
        self.proxyHostLineEdit = QtWidgets.QLineEdit(self.proxyGroupBox)
        self.proxyHostLineEdit.setEnabled(False)
        self.proxyHostLineEdit.setGeometry(QtCore.QRect(25, 39, 238, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxyHostLineEdit.sizePolicy().hasHeightForWidth())
        self.proxyHostLineEdit.setSizePolicy(sizePolicy)
        self.proxyHostLineEdit.setObjectName("proxyHostLineEdit")
        self.proxyPortLineEdit = QtWidgets.QLineEdit(self.proxyGroupBox)
        self.proxyPortLineEdit.setEnabled(False)
        self.proxyPortLineEdit.setGeometry(QtCore.QRect(280, 39, 61, 31))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.proxyPortLineEdit.sizePolicy().hasHeightForWidth())
        self.proxyPortLineEdit.setSizePolicy(sizePolicy)
        self.proxyPortLineEdit.setText("")
        self.proxyPortLineEdit.setObjectName("proxyPortLineEdit")
        self.useProxyCheckBox = QtWidgets.QCheckBox(self.proxyGroupBox)
        self.useProxyCheckBox.setGeometry(QtCore.QRect(0, 0, 89, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.useProxyCheckBox.sizePolicy().hasHeightForWidth())
        self.useProxyCheckBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.useProxyCheckBox.setFont(font)
        self.useProxyCheckBox.setObjectName("useProxyCheckBox")
        self.lblProxyPort = QtWidgets.QLabel(downloadOptionsDialog)
        self.lblProxyPort.setGeometry(QtCore.QRect(290, 186, 138, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblProxyPort.setFont(font)
        self.lblProxyPort.setObjectName("lblProxyPort")
        self.lblProxyHost = QtWidgets.QLabel(downloadOptionsDialog)
        self.lblProxyHost.setGeometry(QtCore.QRect(35, 186, 138, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblProxyHost.setFont(font)
        self.lblProxyHost.setObjectName("lblProxyHost")

        self.retranslateUi(downloadOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(downloadOptionsDialog)
        downloadOptionsDialog.setTabOrder(self.spinTimeout, self.spinThreads)
        downloadOptionsDialog.setTabOrder(self.spinThreads, self.cacheDirLineEdit)
        downloadOptionsDialog.setTabOrder(self.cacheDirLineEdit, self.cacheDirBrowseButton)
        downloadOptionsDialog.setTabOrder(self.cacheDirBrowseButton, self.disableChecksumCheckBox)
        downloadOptionsDialog.setTabOrder(self.disableChecksumCheckBox, self.fetchBugReportsCheckBox)
        downloadOptionsDialog.setTabOrder(self.fetchBugReportsCheckBox, self.useProxyCheckBox)
        downloadOptionsDialog.setTabOrder(self.useProxyCheckBox, self.proxyHostLineEdit)
        downloadOptionsDialog.setTabOrder(self.proxyHostLineEdit, self.proxyPortLineEdit)
        downloadOptionsDialog.setTabOrder(self.proxyPortLineEdit, self.downloadOptionDialogOkButton)

    def retranslateUi(self, downloadOptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        downloadOptionsDialog.setWindowTitle(_translate("downloadOptionsDialog", "Advanced options for download"))
        self.lblThreads.setToolTip(_translate("downloadOptionsDialog", "Number of parallel connections"))
        self.lblThreads.setText(_translate("downloadOptionsDialog", "Use threads"))
        self.spinThreads.setToolTip(_translate("downloadOptionsDialog", "Number of parallel connections"))
        self.downloadOptionDialogOkButton.setText(_translate("downloadOptionsDialog", "Ok"))
        self.lblSocketTimeo.setToolTip(_translate("downloadOptionsDialog", "Network timeout in seconds"))
        self.lblSocketTimeo.setText(_translate("downloadOptionsDialog", "Network Timeout"))
        self.spinTimeout.setToolTip(_translate("downloadOptionsDialog", "Network timeout in seconds"))
        self.cacheDirLineEdit.setToolTip(_translate("downloadOptionsDialog", "Cache folder to search for"))
        self.cacheDirBrowseButton.setText(_translate("downloadOptionsDialog", "Browse"))
        self.lblCacheDir.setToolTip(_translate("downloadOptionsDialog", "Cache folder to search for"))
        self.lblCacheDir.setText(_translate("downloadOptionsDialog", "Cache Directory"))
        self.disableChecksumCheckBox.setToolTip(_translate("downloadOptionsDialog", "Disables checksum verification of downloaded items. Enable only if you know what you are doing"))
        self.disableChecksumCheckBox.setText(_translate("downloadOptionsDialog", "Disable Checksum"))
        self.fetchBugReportsCheckBox.setToolTip(_translate("downloadOptionsDialog", "Fetch Bug Reports"))
        self.fetchBugReportsCheckBox.setText(_translate("downloadOptionsDialog", "Fetch Bug Reports"))
        self.proxyHostLineEdit.setToolTip(_translate("downloadOptionsDialog", "Proxy Server Host/IP Address"))
        self.proxyPortLineEdit.setToolTip(_translate("downloadOptionsDialog", "Proxy Server Port Address"))
        self.useProxyCheckBox.setToolTip(_translate("downloadOptionsDialog", "Check if using a Proxy server"))
        self.useProxyCheckBox.setText(_translate("downloadOptionsDialog", "Proxy"))
        self.lblProxyPort.setToolTip(_translate("downloadOptionsDialog", "Cache folder to search for"))
        self.lblProxyPort.setText(_translate("downloadOptionsDialog", "Port"))
        self.lblProxyHost.setToolTip(_translate("downloadOptionsDialog", "Cache folder to search for"))
        self.lblProxyHost.setText(_translate("downloadOptionsDialog", "Host"))
from . import resources_rc

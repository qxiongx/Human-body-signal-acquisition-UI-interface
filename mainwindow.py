# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(834, 644)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_1 = QtWidgets.QGridLayout()
        self.gridLayout_1.setObjectName("gridLayout_1")
        self.pushButton_connect = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pushButton_connect.setFont(font)
        self.pushButton_connect.setObjectName("pushButton_connect")
        self.gridLayout_1.addWidget(self.pushButton_connect, 0, 0, 1, 1)
        self.pushButton_wave = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pushButton_wave.setFont(font)
        self.pushButton_wave.setObjectName("pushButton_wave")
        self.gridLayout_1.addWidget(self.pushButton_wave, 1, 0, 1, 1)
        self.pushButton_collect = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pushButton_collect.setFont(font)
        self.pushButton_collect.setObjectName("pushButton_collect")
        self.gridLayout_1.addWidget(self.pushButton_collect, 2, 0, 1, 1)
        self.pushButton_predict = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pushButton_predict.setFont(font)
        self.pushButton_predict.setObjectName("pushButton_predict")
        self.gridLayout_1.addWidget(self.pushButton_predict, 3, 0, 1, 1)
        self.pushButton_experiment = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pushButton_experiment.setFont(font)
        self.pushButton_experiment.setObjectName("pushButton_experiment")
        self.gridLayout_1.addWidget(self.pushButton_experiment, 4, 0, 1, 1)
        self.pushButton_explain = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pushButton_explain.setFont(font)
        self.pushButton_explain.setObjectName("pushButton_explain")
        self.gridLayout_1.addWidget(self.pushButton_explain, 5, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_1, 1, 0, 1, 1)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 40))
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label = QtWidgets.QLabel(self.widget_3)
        self.label.setMinimumSize(QtCore.QSize(0, 40))
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_3, 0, 1, 1, 1)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_connect = QtWidgets.QWidget()
        self.page_connect.setObjectName("page_connect")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_connect)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.widget = QtWidgets.QWidget(self.page_connect)
        self.widget.setObjectName("widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_state = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_state.setFont(font)
        self.label_state.setObjectName("label_state")
        self.gridLayout_4.addWidget(self.label_state, 2, 0, 1, 1)
        self.pushButton_cel_device = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pushButton_cel_device.setFont(font)
        self.pushButton_cel_device.setObjectName("pushButton_cel_device")
        self.gridLayout_4.addWidget(self.pushButton_cel_device, 2, 2, 1, 1)
        self.label_address = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_address.setFont(font)
        self.label_address.setObjectName("label_address")
        self.gridLayout_4.addWidget(self.label_address, 0, 0, 1, 1)
        self.label_battery = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_battery.setFont(font)
        self.label_battery.setObjectName("label_battery")
        self.gridLayout_4.addWidget(self.label_battery, 3, 0, 1, 1)
        self.pushButton_con_device = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.pushButton_con_device.setFont(font)
        self.pushButton_con_device.setObjectName("pushButton_con_device")
        self.gridLayout_4.addWidget(self.pushButton_con_device, 0, 2, 1, 1)
        self.label_port = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.label_port.setFont(font)
        self.label_port.setObjectName("label_port")
        self.gridLayout_4.addWidget(self.label_port, 1, 0, 1, 1)
        self.lineEdit_state = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_state.setObjectName("lineEdit_state")
        self.gridLayout_4.addWidget(self.lineEdit_state, 2, 1, 1, 1)
        self.lineEdit_adress = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_adress.setObjectName("lineEdit_adress")
        self.gridLayout_4.addWidget(self.lineEdit_adress, 0, 1, 1, 1)
        self.lineEdit_port = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.gridLayout_4.addWidget(self.lineEdit_port, 1, 1, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_device1 = QtWidgets.QLabel(self.widget_2)
        self.label_device1.setObjectName("label_device1")
        self.gridLayout_7.addWidget(self.label_device1, 0, 0, 1, 1)
        self.widget_5 = QtWidgets.QWidget(self.widget_2)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_7.addWidget(self.widget_5, 0, 1, 1, 1)
        self.label_device2 = QtWidgets.QLabel(self.widget_2)
        self.label_device2.setObjectName("label_device2")
        self.gridLayout_7.addWidget(self.label_device2, 1, 0, 1, 1)
        self.widget_6 = QtWidgets.QWidget(self.widget_2)
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_7.addWidget(self.widget_6, 1, 1, 1, 1)
        self.label_device3 = QtWidgets.QLabel(self.widget_2)
        self.label_device3.setObjectName("label_device3")
        self.gridLayout_7.addWidget(self.label_device3, 2, 0, 1, 1)
        self.widget_7 = QtWidgets.QWidget(self.widget_2)
        self.widget_7.setObjectName("widget_7")
        self.gridLayout_7.addWidget(self.widget_7, 2, 1, 1, 1)
        self.gridLayout_4.addWidget(self.widget_2, 3, 1, 1, 1)
        self.gridLayout_3.addWidget(self.widget, 2, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_connect)
        self.page_wave = QtWidgets.QWidget()
        self.page_wave.setObjectName("page_wave")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page_wave)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.widget_8 = QtWidgets.QWidget(self.page_wave)
        self.widget_8.setObjectName("widget_8")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget_8)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.comboBox = QtWidgets.QComboBox(self.widget_8)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_8.addWidget(self.comboBox, 0, 0, 1, 1)
        self.pushButton_int_display = QtWidgets.QPushButton(self.widget_8)
        self.pushButton_int_display.setObjectName("pushButton_int_display")
        self.gridLayout_8.addWidget(self.pushButton_int_display, 2, 0, 1, 1)
        self.pushButton_display = QtWidgets.QPushButton(self.widget_8)
        self.pushButton_display.setObjectName("pushButton_display")
        self.gridLayout_8.addWidget(self.pushButton_display, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout_5.addWidget(self.widget_8, 0, 1, 1, 1)
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.page_wave)
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.page_device1 = QtWidgets.QWidget()
        self.page_device1.setObjectName("page_device1")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.page_device1)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.widget_bend2 = QtWidgets.QWidget(self.page_device1)
        self.widget_bend2.setObjectName("widget_bend2")
        self.gridLayout_9.addWidget(self.widget_bend2, 0, 1, 1, 1)
        self.widget_bend3 = QtWidgets.QWidget(self.page_device1)
        self.widget_bend3.setObjectName("widget_bend3")
        self.gridLayout_9.addWidget(self.widget_bend3, 0, 2, 1, 1)
        self.widget_bend4 = QtWidgets.QWidget(self.page_device1)
        self.widget_bend4.setObjectName("widget_bend4")
        self.gridLayout_9.addWidget(self.widget_bend4, 1, 0, 1, 1)
        self.widget_bend5 = QtWidgets.QWidget(self.page_device1)
        self.widget_bend5.setObjectName("widget_bend5")
        self.gridLayout_9.addWidget(self.widget_bend5, 1, 1, 1, 1)
        self.widget_stress1 = QtWidgets.QWidget(self.page_device1)
        self.widget_stress1.setObjectName("widget_stress1")
        self.gridLayout_9.addWidget(self.widget_stress1, 1, 2, 1, 1)
        self.widget_stress2 = QtWidgets.QWidget(self.page_device1)
        self.widget_stress2.setObjectName("widget_stress2")
        self.gridLayout_9.addWidget(self.widget_stress2, 2, 0, 1, 1)
        self.widget_stress3 = QtWidgets.QWidget(self.page_device1)
        self.widget_stress3.setObjectName("widget_stress3")
        self.gridLayout_9.addWidget(self.widget_stress3, 2, 1, 1, 1)
        self.widget_imu1 = QtWidgets.QWidget(self.page_device1)
        self.widget_imu1.setObjectName("widget_imu1")
        self.gridLayout_9.addWidget(self.widget_imu1, 2, 2, 1, 1)
        self.widget_imu2 = QtWidgets.QWidget(self.page_device1)
        self.widget_imu2.setObjectName("widget_imu2")
        self.gridLayout_9.addWidget(self.widget_imu2, 3, 0, 1, 1)
        self.widget_imu3 = QtWidgets.QWidget(self.page_device1)
        self.widget_imu3.setObjectName("widget_imu3")
        self.gridLayout_9.addWidget(self.widget_imu3, 3, 1, 1, 1)
        self.widget_bend1 = QtWidgets.QWidget(self.page_device1)
        self.widget_bend1.setObjectName("widget_bend1")
        self.gridLayout_9.addWidget(self.widget_bend1, 0, 0, 1, 1)
        self.stackedWidget_2.addWidget(self.page_device1)
        self.page_device2 = QtWidgets.QWidget()
        self.page_device2.setObjectName("page_device2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_device2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_EMG1 = QtWidgets.QWidget(self.page_device2)
        self.widget_EMG1.setObjectName("widget_EMG1")
        self.verticalLayout.addWidget(self.widget_EMG1)
        self.widget_EMG2 = QtWidgets.QWidget(self.page_device2)
        self.widget_EMG2.setObjectName("widget_EMG2")
        self.verticalLayout.addWidget(self.widget_EMG2)
        self.widget_EMG3 = QtWidgets.QWidget(self.page_device2)
        self.widget_EMG3.setObjectName("widget_EMG3")
        self.verticalLayout.addWidget(self.widget_EMG3)
        self.widget_EMG4 = QtWidgets.QWidget(self.page_device2)
        self.widget_EMG4.setObjectName("widget_EMG4")
        self.verticalLayout.addWidget(self.widget_EMG4)
        self.stackedWidget_2.addWidget(self.page_device2)
        self.page_device3 = QtWidgets.QWidget()
        self.page_device3.setObjectName("page_device3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_device3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_EOG1 = QtWidgets.QWidget(self.page_device3)
        self.widget_EOG1.setObjectName("widget_EOG1")
        self.verticalLayout_2.addWidget(self.widget_EOG1)
        self.widget_EOG2 = QtWidgets.QWidget(self.page_device3)
        self.widget_EOG2.setObjectName("widget_EOG2")
        self.verticalLayout_2.addWidget(self.widget_EOG2)
        self.widget_allIMU = QtWidgets.QWidget(self.page_device3)
        self.widget_allIMU.setObjectName("widget_allIMU")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_allIMU)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_IMU1 = QtWidgets.QWidget(self.widget_allIMU)
        self.widget_IMU1.setObjectName("widget_IMU1")
        self.horizontalLayout.addWidget(self.widget_IMU1)
        self.widget_IMU2 = QtWidgets.QWidget(self.widget_allIMU)
        self.widget_IMU2.setObjectName("widget_IMU2")
        self.horizontalLayout.addWidget(self.widget_IMU2)
        self.widget_IMU3 = QtWidgets.QWidget(self.widget_allIMU)
        self.widget_IMU3.setObjectName("widget_IMU3")
        self.horizontalLayout.addWidget(self.widget_IMU3)
        self.verticalLayout_2.addWidget(self.widget_allIMU)
        self.stackedWidget_2.addWidget(self.page_device3)
        self.gridLayout_5.addWidget(self.stackedWidget_2, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_wave)
        self.page_collect = QtWidgets.QWidget()
        self.page_collect.setObjectName("page_collect")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_collect)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.widget_4 = QtWidgets.QWidget(self.page_collect)
        self.widget_4.setMaximumSize(QtCore.QSize(375, 16777215))
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_title1 = QtWidgets.QLabel(self.widget_4)
        self.label_title1.setMaximumSize(QtCore.QSize(16777215, 60))
        self.label_title1.setObjectName("label_title1")
        self.gridLayout_10.addWidget(self.label_title1, 0, 0, 1, 2)
        self.lineEdit_input = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_input.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_input.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_input.setFont(font)
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.gridLayout_10.addWidget(self.lineEdit_input, 1, 0, 1, 2)
        self.pushButton_make_label = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_make_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton_make_label.setObjectName("pushButton_make_label")
        self.gridLayout_10.addWidget(self.pushButton_make_label, 2, 0, 1, 1)
        self.pushButton_clear_label = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_clear_label.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton_clear_label.setObjectName("pushButton_clear_label")
        self.gridLayout_10.addWidget(self.pushButton_clear_label, 2, 1, 1, 1)
        self.pushButton_begin_col = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_begin_col.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton_begin_col.setObjectName("pushButton_begin_col")
        self.gridLayout_10.addWidget(self.pushButton_begin_col, 3, 0, 1, 2)
        self.pushButton_stop_col = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_stop_col.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton_stop_col.setObjectName("pushButton_stop_col")
        self.gridLayout_10.addWidget(self.pushButton_stop_col, 4, 0, 1, 2)
        self.pushButton_look_col = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_look_col.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton_look_col.setObjectName("pushButton_look_col")
        self.gridLayout_10.addWidget(self.pushButton_look_col, 5, 0, 1, 2)
        self.lineEdit_display1 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_display1.setMaximumSize(QtCore.QSize(16777215, 90))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_display1.setFont(font)
        self.lineEdit_display1.setObjectName("lineEdit_display1")
        self.gridLayout_10.addWidget(self.lineEdit_display1, 6, 0, 1, 2)
        self.gridLayout_2.addWidget(self.widget_4, 0, 0, 1, 1)
        self.widget_dump1 = QtWidgets.QWidget(self.page_collect)
        self.widget_dump1.setMaximumSize(QtCore.QSize(20, 1000))
        self.widget_dump1.setObjectName("widget_dump1")
        self.gridLayout_2.addWidget(self.widget_dump1, 0, 1, 1, 1)
        self.widget_9 = QtWidgets.QWidget(self.page_collect)
        self.widget_9.setMaximumSize(QtCore.QSize(375, 16777215))
        self.widget_9.setObjectName("widget_9")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.widget_9)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.widget_device2 = QtWidgets.QWidget(self.widget_9)
        self.widget_device2.setObjectName("widget_device2")
        self.gridLayout_11.addWidget(self.widget_device2, 2, 0, 1, 1)
        self.widget_device1 = QtWidgets.QWidget(self.widget_9)
        self.widget_device1.setObjectName("widget_device1")
        self.gridLayout_11.addWidget(self.widget_device1, 1, 0, 1, 1)
        self.widget_device3_2 = QtWidgets.QWidget(self.widget_9)
        self.widget_device3_2.setObjectName("widget_device3_2")
        self.gridLayout_11.addWidget(self.widget_device3_2, 4, 0, 1, 1)
        self.widget_device3_1 = QtWidgets.QWidget(self.widget_9)
        self.widget_device3_1.setObjectName("widget_device3_1")
        self.gridLayout_11.addWidget(self.widget_device3_1, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget_9)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_2.setObjectName("label_2")
        self.gridLayout_11.addWidget(self.label_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_9, 0, 3, 1, 1)
        self.stackedWidget.addWidget(self.page_collect)
        self.page_predict = QtWidgets.QWidget()
        self.page_predict.setObjectName("page_predict")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.page_predict)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_11 = QtWidgets.QWidget(self.page_predict)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_10 = QtWidgets.QWidget(self.widget_11)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_13 = QtWidgets.QWidget(self.widget_10)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_13)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_16 = QtWidgets.QWidget(self.widget_13)
        self.widget_16.setObjectName("widget_16")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_16)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_input_model = QtWidgets.QPushButton(self.widget_16)
        self.pushButton_input_model.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pushButton_input_model.setIconSize(QtCore.QSize(20, 50))
        self.pushButton_input_model.setObjectName("pushButton_input_model")
        self.horizontalLayout_4.addWidget(self.pushButton_input_model)
        self.pushButton_clear_model = QtWidgets.QPushButton(self.widget_16)
        self.pushButton_clear_model.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pushButton_clear_model.setObjectName("pushButton_clear_model")
        self.horizontalLayout_4.addWidget(self.pushButton_clear_model)
        self.verticalLayout_4.addWidget(self.widget_16)
        self.widget_15 = QtWidgets.QWidget(self.widget_13)
        self.widget_15.setObjectName("widget_15")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_15)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_15)
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 260))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_6.addWidget(self.lineEdit)
        self.verticalLayout_4.addWidget(self.widget_15)
        self.verticalLayout_3.addWidget(self.widget_13)
        self.widget_14 = QtWidgets.QWidget(self.widget_10)
        self.widget_14.setObjectName("widget_14")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_14)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_begin_pre = QtWidgets.QPushButton(self.widget_14)
        self.pushButton_begin_pre.setMaximumSize(QtCore.QSize(16777215, 35))
        self.pushButton_begin_pre.setObjectName("pushButton_begin_pre")
        self.verticalLayout_7.addWidget(self.pushButton_begin_pre)
        self.pushButton_final_pre = QtWidgets.QPushButton(self.widget_14)
        self.pushButton_final_pre.setMaximumSize(QtCore.QSize(16777215, 35))
        self.pushButton_final_pre.setObjectName("pushButton_final_pre")
        self.verticalLayout_7.addWidget(self.pushButton_final_pre)
        self.verticalLayout_3.addWidget(self.widget_14)
        self.horizontalLayout_3.addWidget(self.widget_10)
        self.widget_12 = QtWidgets.QWidget(self.widget_11)
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_12)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_17 = QtWidgets.QWidget(self.widget_12)
        self.widget_17.setObjectName("widget_17")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_17)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_4 = QtWidgets.QLabel(self.widget_17)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4)
        self.widget_18 = QtWidgets.QWidget(self.widget_17)
        self.widget_18.setObjectName("widget_18")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_18)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_device1 = QtWidgets.QPushButton(self.widget_18)
        self.pushButton_device1.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pushButton_device1.setObjectName("pushButton_device1")
        self.horizontalLayout_5.addWidget(self.pushButton_device1)
        self.pushButton_device2 = QtWidgets.QPushButton(self.widget_18)
        self.pushButton_device2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pushButton_device2.setObjectName("pushButton_device2")
        self.horizontalLayout_5.addWidget(self.pushButton_device2)
        self.pushButton_device3 = QtWidgets.QPushButton(self.widget_18)
        self.pushButton_device3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.pushButton_device3.setObjectName("pushButton_device3")
        self.horizontalLayout_5.addWidget(self.pushButton_device3)
        self.verticalLayout_8.addWidget(self.widget_18)
        self.widget_19 = QtWidgets.QWidget(self.widget_17)
        self.widget_19.setObjectName("widget_19")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_19)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_select_de = QtWidgets.QPushButton(self.widget_19)
        self.pushButton_select_de.setMaximumSize(QtCore.QSize(16777215, 35))
        self.pushButton_select_de.setObjectName("pushButton_select_de")
        self.horizontalLayout_6.addWidget(self.pushButton_select_de)
        self.pushButton_remove_de = QtWidgets.QPushButton(self.widget_19)
        self.pushButton_remove_de.setMaximumSize(QtCore.QSize(16777215, 39))
        self.pushButton_remove_de.setObjectName("pushButton_remove_de")
        self.horizontalLayout_6.addWidget(self.pushButton_remove_de)
        self.verticalLayout_8.addWidget(self.widget_19)
        self.lineEdit_device = QtWidgets.QLineEdit(self.widget_17)
        self.lineEdit_device.setMaximumSize(QtCore.QSize(16777215, 80))
        self.lineEdit_device.setObjectName("lineEdit_device")
        self.verticalLayout_8.addWidget(self.lineEdit_device)
        self.verticalLayout_5.addWidget(self.widget_17)
        self.label_3 = QtWidgets.QLabel(self.widget_12)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.lineEdit_result = QtWidgets.QLineEdit(self.widget_12)
        self.lineEdit_result.setMaximumSize(QtCore.QSize(16777215, 600))
        self.lineEdit_result.setObjectName("lineEdit_result")
        self.verticalLayout_5.addWidget(self.lineEdit_result)
        self.horizontalLayout_3.addWidget(self.widget_12)
        self.horizontalLayout_2.addWidget(self.widget_11)
        self.stackedWidget.addWidget(self.page_predict)
        self.page_experiment = QtWidgets.QWidget()
        self.page_experiment.setObjectName("page_experiment")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.page_experiment)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.widget_20 = QtWidgets.QWidget(self.page_experiment)
        self.widget_20.setObjectName("widget_20")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_20)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widget_21 = QtWidgets.QWidget(self.widget_20)
        self.widget_21.setObjectName("widget_21")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_21)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget_23 = QtWidgets.QWidget(self.widget_21)
        self.widget_23.setObjectName("widget_23")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_23)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.pushButton_input1 = QtWidgets.QPushButton(self.widget_23)
        self.pushButton_input1.setObjectName("pushButton_input1")
        self.verticalLayout_11.addWidget(self.pushButton_input1)
        self.pushButton_output1 = QtWidgets.QPushButton(self.widget_23)
        self.pushButton_output1.setObjectName("pushButton_output1")
        self.verticalLayout_11.addWidget(self.pushButton_output1)
        self.pushButton_begin1 = QtWidgets.QPushButton(self.widget_23)
        self.pushButton_begin1.setObjectName("pushButton_begin1")
        self.verticalLayout_11.addWidget(self.pushButton_begin1)
        self.pushButton_end1 = QtWidgets.QPushButton(self.widget_23)
        self.pushButton_end1.setObjectName("pushButton_end1")
        self.verticalLayout_11.addWidget(self.pushButton_end1)
        self.verticalLayout_10.addWidget(self.widget_23)
        self.widget_24 = QtWidgets.QWidget(self.widget_21)
        self.widget_24.setObjectName("widget_24")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.widget_24)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.textEdit = QtWidgets.QTextEdit(self.widget_24)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_13.addWidget(self.textEdit)
        self.verticalLayout_10.addWidget(self.widget_24)
        self.horizontalLayout_7.addWidget(self.widget_21)
        self.widget_22 = QtWidgets.QWidget(self.widget_20)
        self.widget_22.setObjectName("widget_22")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.widget_22)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_5 = QtWidgets.QLabel(self.widget_22)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_12.addWidget(self.label_5)
        self.textEdit_result1 = QtWidgets.QTextEdit(self.widget_22)
        self.textEdit_result1.setObjectName("textEdit_result1")
        self.verticalLayout_12.addWidget(self.textEdit_result1)
        self.pushButton_control = QtWidgets.QPushButton(self.widget_22)
        self.pushButton_control.setObjectName("pushButton_control")
        self.verticalLayout_12.addWidget(self.pushButton_control)
        self.pushButton_dis_control = QtWidgets.QPushButton(self.widget_22)
        self.pushButton_dis_control.setObjectName("pushButton_dis_control")
        self.verticalLayout_12.addWidget(self.pushButton_dis_control)
        self.widget_25 = QtWidgets.QWidget(self.widget_22)
        self.widget_25.setObjectName("widget_25")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_25)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(self.widget_25)
        self.label_6.setMinimumSize(QtCore.QSize(140, 0))
        self.label_6.setMaximumSize(QtCore.QSize(140, 16777215))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.lineEdit_control_ip = QtWidgets.QLineEdit(self.widget_25)
        self.lineEdit_control_ip.setObjectName("lineEdit_control_ip")
        self.horizontalLayout_8.addWidget(self.lineEdit_control_ip)
        self.verticalLayout_12.addWidget(self.widget_25)
        self.widget_26 = QtWidgets.QWidget(self.widget_22)
        self.widget_26.setObjectName("widget_26")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_26)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.widget_26)
        self.label_7.setMinimumSize(QtCore.QSize(140, 0))
        self.label_7.setMaximumSize(QtCore.QSize(140, 16777215))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.lineEdit_control_port = QtWidgets.QLineEdit(self.widget_26)
        self.lineEdit_control_port.setObjectName("lineEdit_control_port")
        self.horizontalLayout_9.addWidget(self.lineEdit_control_port)
        self.verticalLayout_12.addWidget(self.widget_26)
        self.textEdit_result2 = QtWidgets.QTextEdit(self.widget_22)
        self.textEdit_result2.setObjectName("textEdit_result2")
        self.verticalLayout_12.addWidget(self.textEdit_result2)
        self.horizontalLayout_7.addWidget(self.widget_22)
        self.verticalLayout_9.addWidget(self.widget_20)
        self.stackedWidget.addWidget(self.page_experiment)
        self.page_explain = QtWidgets.QWidget()
        self.page_explain.setObjectName("page_explain")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.page_explain)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.textEdit_3 = QtWidgets.QTextEdit(self.page_explain)
        self.textEdit_3.setObjectName("textEdit_3")
        self.verticalLayout_14.addWidget(self.textEdit_3)
        self.stackedWidget.addWidget(self.page_explain)
        self.gridLayout.addWidget(self.stackedWidget, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 834, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        self.stackedWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_connect.setText(_translate("MainWindow", "设备连接"))
        self.pushButton_wave.setText(_translate("MainWindow", "波形显示"))
        self.pushButton_collect.setText(_translate("MainWindow", "数据采集"))
        self.pushButton_predict.setText(_translate("MainWindow", "模型预测"))
        self.pushButton_experiment.setText(_translate("MainWindow", "实验测试"))
        self.pushButton_explain.setText(_translate("MainWindow", "使用说明"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:700;\">人体信号采集软件系统</span></p></body></html>"))
        self.label_state.setText(_translate("MainWindow", "连接状态："))
        self.pushButton_cel_device.setText(_translate("MainWindow", "取消连接"))
        self.label_address.setText(_translate("MainWindow", "TCP地址："))
        self.label_battery.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700; color:#000000;\">设</span><span style=\" font-size:14pt; font-weight:700; color:#ff0000;\"><br/></span><span style=\" font-size:14pt; font-weight:700; color:#000000;\">备</span><span style=\" font-size:14pt; font-weight:700; color:#ff0000;\"><br/></span><span style=\" font-size:14pt; font-weight:700; color:#000000;\">电</span><span style=\" font-size:14pt; font-weight:700; color:#ff0000;\"><br/></span><span style=\" font-size:14pt; font-weight:700; color:#000000;\">量</span><span style=\" font-size:14pt; font-weight:700; color:#ff0000;\"><br/></span></p></body></html>"))
        self.pushButton_con_device.setText(_translate("MainWindow", "连接设备"))
        self.label_port.setText(_translate("MainWindow", "TCP端口号："))
        self.label_device1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">数据手套</span></p></body></html>"))
        self.label_device2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">肌电手环</span></p></body></html>"))
        self.label_device3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">眼电及头动采集板卡</span></p></body></html>"))
        self.comboBox.setItemText(0, _translate("MainWindow", "数据手套"))
        self.comboBox.setItemText(1, _translate("MainWindow", "肌电手环"))
        self.comboBox.setItemText(2, _translate("MainWindow", "眼电及头动采集板卡"))
        self.pushButton_int_display.setText(_translate("MainWindow", "结束显示"))
        self.pushButton_display.setText(_translate("MainWindow", "开始显示"))
        self.label_title1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:700;\">请在下方文本框内<br/>输入姿态标签</span></p></body></html>"))
        self.pushButton_make_label.setText(_translate("MainWindow", "确定标签"))
        self.pushButton_clear_label.setText(_translate("MainWindow", "清除标签"))
        self.pushButton_begin_col.setText(_translate("MainWindow", "开始录入"))
        self.pushButton_stop_col.setText(_translate("MainWindow", "停止录入"))
        self.pushButton_look_col.setText(_translate("MainWindow", "记录查询"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:700;\">如下为实际数据接收情况</span></p></body></html>"))
        self.pushButton_input_model.setText(_translate("MainWindow", "载入模型"))
        self.pushButton_clear_model.setText(_translate("MainWindow", "清除模型"))
        self.pushButton_begin_pre.setText(_translate("MainWindow", "开始预测"))
        self.pushButton_final_pre.setText(_translate("MainWindow", "结束预测"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">输入设备选择</span></p></body></html>"))
        self.pushButton_device1.setText(_translate("MainWindow", "数据手套"))
        self.pushButton_device2.setText(_translate("MainWindow", "肌电手环"))
        self.pushButton_device3.setText(_translate("MainWindow", "眼电头动采集卡"))
        self.pushButton_select_de.setText(_translate("MainWindow", "选择"))
        self.pushButton_remove_de.setText(_translate("MainWindow", "移除"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">动作识别结果</span></p></body></html>"))
        self.pushButton_input1.setText(_translate("MainWindow", "载入模型"))
        self.pushButton_output1.setText(_translate("MainWindow", "删除模型"))
        self.pushButton_begin1.setText(_translate("MainWindow", "开始预测"))
        self.pushButton_end1.setText(_translate("MainWindow", "结束预测"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:700;\">预测结果</span></p></body></html>"))
        self.pushButton_control.setText(_translate("MainWindow", "连接无人车"))
        self.pushButton_dis_control.setText(_translate("MainWindow", "关闭所有节点"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">无人车ip</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">无人车端口</span></p></body></html>"))

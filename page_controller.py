"""
页面控制器模块

此模块负责管理应用程序的页面切换逻辑。通过PageController类实现以下功能：
- 初始化页面显示
- 设置页面切换按钮的信号连接
- 处理各个页面之间的切换
- 管理设备选择和对应页面显示
- 管理数据标签的设置和清除

类:
    PageController: 负责处理所有页面切换相关的逻辑
"""
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from mainwindow import Ui_MainWindow
from data_storage import DataStorage  # 添加这行导入
import logging

class PageController:
    def __init__(self, main_window: QMainWindow):
        self.ui = main_window.ui
        self.wave_controllers = main_window.wave_controllers
        self.connect_controller = main_window.connect_controller
        self.setup_wave_display_controls()
        self.data_storage = getattr(main_window, 'data_storage', None)
        if self.data_storage is None:
            self.data_storage = DataStorage()
            main_window.data_storage = self.data_storage  # 保存到主窗口以便共享
        
        # 配置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 初始化设置
        self.setup_device_selector()
        self.setup_page_connections()
        self.setup_label_connections()
        self.set_initial_page()

    def setup_wave_display_controls(self):
        """设置波形显示控制按钮的连接"""
        try:
            # 控制所有波形显示
            self.ui.pushButton_display.clicked.connect(self.start_all_displays)
            self.ui.pushButton_int_display.clicked.connect(self.stop_all_displays)
        except Exception as e:
            print(f"设置波形显示控制失败: {e}")

    def start_all_displays(self):
        """开始所有波形显示"""
        try:
            # 先启动数据接收
            if hasattr(self.connect_controller, 'start_data_receiving'):
                self.connect_controller.start_data_receiving()
            
            # 然后启动所有波形显示
            for controller in self.wave_controllers:
                if hasattr(controller, 'start_display'):
                    controller.start_display()
                    
        except Exception as e:
            print(f"启动所有波形显示失败: {e}")

    def stop_all_displays(self):
        """停止所有波形显示"""
        try:
            # 先停止数据接收
            if hasattr(self.connect_controller, 'stop_data_receiving'):
                self.connect_controller.stop_data_receiving()
            
            # 然后停止所有波形显示
            for controller in self.wave_controllers:
                if hasattr(controller, 'stop_display'):
                    controller.stop_display()
                    
        except Exception as e:
            print(f"停止所有波形显示失败: {e}")
    
    def setup_device_selector(self):
        """设置设备选择下拉框"""
        try:
            # 清空现有选项
            self.ui.comboBox.clear()
            
            # 添加设备选项
            devices = ['数据手套', '肌电手环', '眼电及头动采集板卡']
            self.ui.comboBox.addItems(devices)
            
            # 连接信号
            self.ui.comboBox.currentIndexChanged.connect(self.on_device_changed)
            
            self.logger.info("设备选择器初始化完成")
        except Exception as e:
            self.logger.error(f"设备选择器初始化失败: {e}")

    def setup_label_connections(self):
        """设置标签按钮的连接"""
        try:
            self.ui.pushButton_make_label.clicked.connect(self.set_data_label)
            self.ui.pushButton_clear_label.clicked.connect(self.clear_data_label)
            self.logger.info("标签按钮连接设置完成")
        except Exception as e:
            self.logger.error(f"标签按钮连接设置失败: {e}")

    def set_data_label(self):
        """设置数据标签"""
        try:
            label = self.ui.lineEdit_input.text().strip()
            if not label:
                QMessageBox.warning(None, "警告", "请输入标签")
                return
                
            success, message = self.data_storage.set_label(label)
            if success:
                self.logger.info(f"标签设置成功: {label}")
                self.update_status_display()
                QMessageBox.information(None, "成功", message)
            else:
                QMessageBox.warning(None, "警告", message)
                self.ui.lineEdit_input.clear()  # 清空输入框
                self.ui.lineEdit_input.setFocus()  # 重新获得焦点
                
        except Exception as e:
            self.logger.error(f"设置标签失败: {e}")
            QMessageBox.critical(None, "错误", f"设置标签失败: {str(e)}")

    def clear_data_label(self):
        """清除数据标签"""
        try:
            message = self.data_storage.clear_label()
            self.ui.lineEdit_input.clear()
            self.logger.info("标签已清除")
            self.update_status_display()
            QMessageBox.information(None, "成功", message)
        except Exception as e:
            self.logger.error(f"清除标签失败: {e}")
            QMessageBox.critical(None, "错误", f"清除标签失败: {str(e)}")

    def update_status_display(self):
        """更新状态显示"""
        try:
            if hasattr(self.ui, 'label_status'):
                self.ui.label_status.setText(self.data_storage.get_storage_status())
        except Exception as e:
            self.logger.error(f"更新状态显示失败: {e}")
    
    def set_initial_page(self):
        """设置初始页面"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_connect)
        if hasattr(self.ui, 'stackedWidget_2'):
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_device1)
    
    def setup_page_connections(self):
        """设置页面切换按钮的连接"""
        # 主导航按钮连接
        self.ui.pushButton_connect.clicked.connect(self.show_connect_page)
        self.ui.pushButton_wave.clicked.connect(self.show_wave_page)
        self.ui.pushButton_collect.clicked.connect(self.show_collect_page)
        self.ui.pushButton_predict.clicked.connect(self.show_predict_page)
        self.ui.pushButton_experiment.clicked.connect(self.show_learn_page)
        self.ui.pushButton_explain.clicked.connect(self.show_explain_page)
        self.ui.pushButton_look_col.clicked.connect(self.show_collection_records)
    
    def on_device_changed(self, index):
        """处理设备选择变更"""
        try:
            if not hasattr(self.ui, 'stackedWidget_2'):
                self.logger.error("找不到波形页面的堆叠窗口部件")
                return
                
            # 根据选择切换到对应页面
            page_mapping = {
                0: self.ui.page_device1,  # 数据手套
                1: self.ui.page_device2,  # 肌电手环
                2: self.ui.page_device3   # 眼电及头动采集板卡
            }
            
            if index in page_mapping:
                self.ui.stackedWidget_2.setCurrentWidget(page_mapping[index])
                self.logger.info(f"切换到设备页面: {self.ui.comboBox.currentText()}")
            else:
                self.logger.error(f"无效的设备索引: {index}")
                
        except Exception as e:
            self.logger.error(f"切换设备页面失败: {e}")
    
    def show_connect_page(self):
        """显示连接页面"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_connect)
        self.logger.info("切换到连接页面")
    
    def show_wave_page(self):
        """切换到波形显示页面"""
        try:
            # 切换到波形页面
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_wave)
            
            # 根据当前选择的设备切换子页面
            if hasattr(self.ui, 'stackedWidget_2'):
                current_device = self.ui.comboBox.currentIndex()
                self.on_device_changed(current_device)
            else:
                self.logger.error("找不到波形页面的堆叠窗口部件")
                
            self.logger.info("切换到波形显示页面")
        except Exception as e:
            self.logger.error(f"切换到波形显示页面失败: {e}")
    
    def show_collect_page(self):
        """显示采集页面"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_collect)
        self.logger.info("切换到采集页面")
    
    def show_predict_page(self):
        """显示预测页面"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_predict)
        self.logger.info("切换到预测页面")
    
    def show_learn_page(self):
        """显示学习页面"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_experiment)
        self.logger.info("切换到学习页面")
    
    def show_explain_page(self):
        """显示说明页面"""
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_explain)
        self.logger.info("切换到说明页面")
        
    def cleanup(self):
        """清理页面控制器资源"""
        try:
            self.logger.info("正在清理页面控制器资源...")
            
            # 断开所有信号连接
            if hasattr(self.ui, 'pushButton_connect'):
                self.ui.pushButton_connect.clicked.disconnect()
            if hasattr(self.ui, 'pushButton_wave'):
                self.ui.pushButton_wave.clicked.disconnect()
            if hasattr(self.ui, 'pushButton_collect'):
                self.ui.pushButton_collect.clicked.disconnect()
            if hasattr(self.ui, 'pushButton_predict'):
                self.ui.pushButton_predict.clicked.disconnect()
            if hasattr(self.ui, 'pushButton_exp'):
                self.ui.pushButton_exp.clicked.disconnect()
            if hasattr(self.ui, 'pushButton_explain'):
                self.ui.pushButton_explain.clicked.disconnect()
            
            # 断开标签按钮的信号连接
            if hasattr(self.ui, 'pushButton_make_label'):
                self.ui.pushButton_make_label.clicked.disconnect()
            if hasattr(self.ui, 'pushButton_clear_label'):
                self.ui.pushButton_clear_label.clicked.disconnect()
            
            # 断开设备选择器的信号连接
            if hasattr(self.ui, 'comboBox'):
                self.ui.comboBox.currentIndexChanged.disconnect()
                
            self.logger.info("页面控制器资源清理完成")
            
        except Exception as e:
            self.logger.error(f"页面控制器清理时出错: {e}")
    
    def show_collection_records(self):
        """显示采集数据记录"""
        print("Debug: 正在打开数据记录窗口")  # 添加调试信息
        self.data_storage.show_collection_records()
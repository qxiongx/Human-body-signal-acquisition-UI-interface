from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
import os
import joblib


class PredictPageController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui
        self.model = None
        self.selected_devices = []  # 存储选中的设备
        self.device_buttons = {}  # 存储设备按钮状态
        self.setup_connections()
        self.setup_device_controls()

    def setup_device_controls(self):
        """初始化设备控制按钮"""
        try:
            # 初始化设备按钮状态字典
            self.device_buttons = {
                '数据手套': {'button': self.ui.pushButton_device1, 'selected': False},
                '肌电手环': {'button': self.ui.pushButton_device2, 'selected': False},
                '头部采集卡': {'button': self.ui.pushButton_device3, 'selected': False}
            }

            # 连接设备按钮
            for device_name, info in self.device_buttons.items():
                info['button'].clicked.connect(
                    lambda checked, btn=info['button']: self.toggle_device(btn)
                )

            # 连接确认选择按钮
            self.ui.pushButton_select_de.clicked.connect(self.confirm_device_selection)

        except Exception as e:
            print(f"设置设备控制按钮失败: {e}")

    def toggle_device(self, button):
        """切换设备选择状态"""
        try:
            for device_name, info in self.device_buttons.items():
                if info['button'] == button:
                    # 切换选中状态
                    info['selected'] = not info['selected']
                    # 更新按钮样式
                    if info['selected']:
                        # 设置深灰色样式
                        button.setStyleSheet("background-color: #666666; color: white;")
                    else:
                        # 恢复默认样式
                        button.setStyleSheet("")
                    break
        except Exception as e:
            print(f"切换设备状态失败: {e}")

    def confirm_device_selection(self):
        """确认设备选择并显示"""
        try:
            # 清空之前的选择
            self.selected_devices.clear()
            
            # 收集选中的设备
            for device_name, info in self.device_buttons.items():
                if info['selected']:
                    self.selected_devices.append(device_name)
            
            # 在lineEdit中显示选中的设备
            if hasattr(self.ui, 'lineEdit_device'):
                if self.selected_devices:
                    devices_text = ", ".join(self.selected_devices)
                    self.ui.lineEdit_device.setText(f"已选择: {devices_text}")
                else:
                    self.ui.lineEdit_device.setText("未选择任何设备")
                    
            print(f"当前选中的设备: {self.selected_devices}")
            
        except Exception as e:
            print(f"确认设备选择失败: {e}")
            if hasattr(self.ui, 'lineEdit_device'):
                self.ui.lineEdit_device.setText("设备选择失败")


    def setup_connections(self):
        """设置按钮连接"""
        try:
            self.ui.pushButton_input_model.clicked.connect(self.select_model)
            # 添加清除模型按钮的连接
            self.ui.pushButton_clear_model.clicked.connect(self.clear_model)
            self.ui.pushButton_remove_de.clicked.connect(self.remove_device_selection)
        except Exception as e:
            print(f"设置预测页面按钮连接失败: {e}")
    
    def remove_device_selection(self):
        """移除所有设备选择状态"""
        try:
            # 清空选中的设备列表
            self.selected_devices.clear()
            
            # 重置所有设备按钮状态
            for device_info in self.device_buttons.values():
                device_info['selected'] = False
                device_info['button'].setStyleSheet("")  # 恢复默认样式
            
            # 清空设备选择显示
            if hasattr(self.ui, 'lineEdit_device'):
                self.ui.lineEdit_device.setText("已清除所有设备选择")
                
            print("已清除所有设备选择")
            
        except Exception as e:
            print(f"清除设备选择失败: {e}")
            if hasattr(self.ui, 'lineEdit_device'):
                self.ui.lineEdit_device.setText("清除设备选择失败")

    def clear_model(self):
        """清除已加载的模型"""
        try:
            self.model = None
            if hasattr(self.ui, 'lineEdit'):
                self.ui.lineEdit.setText("已清除模型")
            print("模型已清除")
        except Exception as e:
            print(f"清除模型失败: {e}")
            if hasattr(self.ui, 'lineEdit'):
                self.ui.lineEdit.setText("模型清除失败")

    def select_model(self):
        """选择并加载模型文件"""
        try:
            # 获取当前目录下的models文件夹路径
            models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
            
            # 确保models目录存在
            if not os.path.exists(models_dir):
                os.makedirs(models_dir)
            
            # 打开文件选择对话框
            file_name, _ = QFileDialog.getOpenFileName(
                self.main_window,
                "选择模型文件",
                models_dir,
                "模型文件 (*.pkl);;所有文件 (*.*)"
            )
            
            if file_name:
                try:
                    # 加载选中的模型
                    self.model = joblib.load(file_name)
                    # 只获取文件名，不包含路径
                    model_name = os.path.basename(file_name)
                    print(f"模型加载成功: {model_name}")
                    
                    # 在lineEdit中只显示模型名称
                    if hasattr(self.ui, 'lineEdit'):
                        self.ui.lineEdit.setText(model_name)
                    
                except Exception as e:
                    print(f"模型加载失败: {e}")
                    if hasattr(self.ui, 'lineEdit'):
                        self.ui.lineEdit.setText("模型加载失败")
                    
        except Exception as e:
            print(f"选择模型文件失败: {e}")
            if hasattr(self.ui, 'lineEdit'):
                self.ui.lineEdit.setText("模型选择失败")
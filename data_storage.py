import os
import time
import threading
import queue
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QTimer
from data_record_window import DataRecordWindow

class DataStorage:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataStorage, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    def __init__(self):
        if not self._initialized:
            self.data_queues = {
                'glove': queue.Queue(),
                'emg': queue.Queue(),
                'eog': queue.Queue(), 
                'imu': queue.Queue()
            }
            self.is_storing = False
            self.storage_thread = None
            self.base_path = "collected_data"
            self.current_session = None
            self.files = {}
            self.current_label = ""
            self.record_window = None
            self._initialized = True
            
            self.total_samples = {
                'glove': 0,
                'emg': 0,
                'eog': 0,
                'imu': 0
            }
            
            self.animation_chars = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
            self.animation_index = 0
            self.storage_status = "等待开始录入..."
            self._initialized = True
    

    def set_label(self, label):
        """设置数据标签"""
        if not label:
            self.storage_status = "标签不能为空"
            print(f"Debug: 标签为空")
            return False, "标签不能为空"
        
        # 检查是否为整数
        try:
            label_value = int(label.strip())
            self.current_label = str(label_value)  # 转换回字符串保存
            self.storage_status = f"标签已设置: {self.current_label}"
            print(f"Debug: 标签已设置为: '{self.current_label}'")
            return True, f"标签'{self.current_label}'设置成功"
        except ValueError:
            self.storage_status = "标签必须是数字类型"
            print(f"Debug: 标签格式错误: {label}")
            return False, "标签必须是数字类型，请重新输入"

    def clear_label(self):
        """清除数据标签"""
        old_label = self.current_label
        self.current_label = ""
        self.storage_status = "标签已清除"
        return f"标签'{old_label}'已清除"

    def _format_status(self, show_animation=False):
        """格式化状态信息"""
        if show_animation:
            animation_char = self.animation_chars[self.animation_index]
            self.animation_index = (self.animation_index + 1) % len(self.animation_chars)
            return f"正在录入数据 {animation_char}"
        return self.storage_status

    def start_storage(self):
        """开始数据存储"""
        if self.is_storing:
            print("Debug: 已经在存储中")
            return
                
        print(f"Debug: DataStorage 实例 ID: {id(self)}")
        print(f"Debug: 当前标签值: '{self.current_label}'")
        if not self.current_label:
            self.storage_status = "请点击'确认标签'按钮确认标签后再开始录入数据"
            print("Debug: 标签为空，无法开始存储")
            return
        
        # 创建自动关闭的消息框
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("开始录入")
        msg.setText(f"开始录入数据\n当前标签: {self.current_label}")
        
        # 创建定时器
        timer = QTimer()
        timer.timeout.connect(msg.close)
        timer.start(3000)  # 3000毫秒 = 3秒
        
        # 显示消息框
        msg.exec_()
        print("Debug: 开始创建存储会话，使用标签：", self.current_label)
            
        # 查找可用的目录名
        base_label_dir = f"label_{self.current_label}"
        label_dir = base_label_dir
        counter = 1
        
        while os.path.exists(os.path.join(self.base_path, label_dir)):
            label_dir = f"{base_label_dir}_{counter}"
            counter += 1
        
        # 创建标签目录
        label_path = os.path.join(self.base_path, label_dir)
        os.makedirs(label_path, exist_ok=True)
        print(f"Debug: 创建数据存储目录: {label_path}")

        headers = {
            'glove': "timestamp,bend1,bend2,bend3,bend4,bend5,stress1,stress2,stress3,imu1,imu2,imu3,label",
            'emg': "timestamp,emg1,emg2,emg3,emg4,label",
            'eog': "timestamp,eog1,eog2,label",
            'imu': "timestamp,imu_head1,imu_head2,imu_head3,label"
        }
        self.files = {}
        for data_type, header in headers.items():
            file_path = os.path.join(label_path, f"{data_type}_data.csv")
            self.files[data_type] = open(file_path, "w")
            self.files[data_type].write(f"{header}\n")

        self.reset_counters()
        self.is_storing = True
        self.storage_thread = threading.Thread(target=self._storage_loop)
        self.storage_thread.daemon = True
        self.storage_thread.start()
        self.storage_status = self._format_status(show_animation=True)

    def stop_storage(self):
        """停止数据存储"""
        if not self.is_storing:
            return
                
        self.is_storing = False
        if self.storage_thread:
            self.storage_thread.join()
            
        # 准备显示的数据信息
        session_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_info = f"数据采集会话结束\n时间：{session_time}\n\n"
        data_info += "采集数据统计：\n" + "-" * 30 + "\n"
        
        # 计算总采样数
        total_count = sum(self.total_samples.values())
        
        for data_type, count in self.total_samples.items():
            type_names = {
                'glove': '数据手套数据',
                'emg': 'EMG信号数据',
                'eog': 'EOG信号数据',
                'imu': '头动测量数据'
            }
            data_info += f"{type_names[data_type]:<15}: {count:>8} 采样\n"
        
        data_info += "-" * 30 + "\n"
        data_info += f"总采样数：{total_count:>13} 采样\n"
        data_info += f"数据标签：{self.current_label:>13}\n"
        data_info += f"存储路径：{os.path.abspath(self.base_path)}\n"
        
        # 创建消息框
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("数据采集完成")
        msg.setText(data_info)
        
        # 创建定时器自动关闭
        timer = QTimer()
        timer.timeout.connect(msg.close)
        timer.start(10000)  # 10秒后自动关闭
        
        # 显示消息框
        msg.exec_()
        
        self.storage_status = "数据采集已完成"
        
        # 关闭所有文件
        for file in self.files.values():
            file.close()
        self.files.clear()

    def _storage_loop(self):
        """存储循环"""
        while self.is_storing:
            try:
                total_processed = 0
                
                for data_type in ['glove', 'emg', 'eog', 'imu']:
                    while not self.data_queues[data_type].empty():
                        timestamp, data = self.data_queues[data_type].get_nowait()
                        data_str = ",".join(f"{float(x):.6f}" for x in data)
                        self.files[data_type].write(f"{int(timestamp)},{data_str},{self.current_label}\n")
                        self.files[data_type].flush()
                        self.total_samples[data_type] += 1
                        total_processed += 1

                if total_processed > 0:
                    self.storage_status = self._format_status(show_animation=True)

                time.sleep(0.1)

            except Exception as e:
                self.storage_status = "数据存储错误".center(50)
                print(f"数据存储错误: {str(e)}")

    def get_storage_status(self):
        """获取存储状态信息"""
        return self.storage_status

    def reset_counters(self):
        """重置计数器"""
        self.total_samples = {k: 0 for k in self.total_samples}
        self.storage_status = "准备开始新的录入..."

    def store_data(self, data_type, data):
        """通用数据存储方法"""
        if self.is_storing:
            try:
                float_data = [float(x) for x in data]
                timestamp = time.time()
                self.data_queues[data_type].put((timestamp, float_data))
            except (ValueError, TypeError) as e:
                print(f"{data_type}数据类型转换错误: {e}")

    def show_collection_records(self):
        """显示所有采集数据记录"""
        try:
            print("Debug: 开始显示数据记录")
            if not os.path.exists(self.base_path):
                print(f"Debug: 数据目录不存在: {self.base_path}")
                os.makedirs(self.base_path)
                QMessageBox.warning(None, "提示", "暂无采集数据记录")
                return
                
            self.record_window = DataRecordWindow()  # 使用类成员变量
            self.record_window.load_data(self.base_path)
            self.record_window.setAttribute(Qt.WA_DeleteOnClose)
            self.record_window.show()
            print("Debug: 数据记录窗口已创建并显示")
            
        except Exception as e:
            print(f"Debug: 显示数据记录出错: {str(e)}")
            QMessageBox.critical(None, "错误", f"查看数据记录时出错：{str(e)}")

    def store_glove_data(self, data): self.store_data('glove', data)
    def store_emg_data(self, data): self.store_data('emg', data)
    def store_eog_data(self, data): self.store_data('eog', data)
    def store_imu_data(self, data): self.store_data('imu', data)
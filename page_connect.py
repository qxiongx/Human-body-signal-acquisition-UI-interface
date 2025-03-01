"""
连接页面控制模块

此模块负责处理设备连接页面的功能，包括：
- TCP连接管理
- 数据接收和解析
- 电量显示更新
"""

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from battery_widget import BatteryWidget
import socket
import threading
import select
import queue
from concurrent.futures import ThreadPoolExecutor
import logging
from threading import Lock, Event
from data_storage import DataStorage
import paramiko 

# 配置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

class ConnectPageController:
    def __init__(self, main_window: QMainWindow):
        self.ui = main_window.ui
        self.main_window = main_window
        self.client_socket = None
        self.socket_lock = Lock()
        self.is_connected = False
        self.is_running = True
        self.data_collection_started = False  # 添加数据采集状态标志

        self.ssh_client = None
        self.ip = None
        self.data_collection_enabled = False
        
        
        # 初始化日志记录器
        self.logger = logging.getLogger(__name__)
        
        self.stop_event = Event()
        self.data_queue = queue.Queue(maxsize=1000)
        
        # 创建线程池
        self.thread_pool = ThreadPoolExecutor(max_workers=2)
        
        # 创建两个独立的定时器
        self.process_timer = QTimer(self.main_window)  # 数据处理定时器
        self.process_timer.timeout.connect(self.process_data)
        self.process_timer.setInterval(10)
        self.process_timer.start()
        
        self.display_timer = QTimer(self.main_window)  # 波形显示定时器
        self.display_timer.timeout.connect(self.update_display)
        self.display_timer.setInterval(10)
        self.display_enabled = False  # 控制波形显示的标志
        self.ui.lineEdit_display1.setAlignment(Qt.AlignCenter)
        # 添加状态更新定时器
        self.status_update_timer = QTimer(self.main_window)
        self.status_update_timer.timeout.connect(self.update_storage_status)
        self.status_update_timer.setInterval(1000)  # 每秒更新一次


        self.data_storage = DataStorage()
    
        # 添加按钮连接
        self.ui.pushButton_begin_col.clicked.connect(self.start_data_collection)
        self.ui.pushButton_stop_col.clicked.connect(self.stop_data_collection)

        # 初始化组件
        self.setup_battery_widgets()
        self.setup_default_values()
        self.setup_connections()
        
        logging.info("初始化完成")

    def setup_battery_widgets(self):
        """初始化电池显示组件"""
        self.batteries = {}
        for widget_name, widget in [
            ("battery1", self.ui.widget_5),
            ("battery2", self.ui.widget_6),
            ("battery3", self.ui.widget_7)
        ]:
            battery = BatteryWidget(widget)
            layout = widget.layout() or QVBoxLayout(widget)
            layout.addWidget(battery)
            self.batteries[widget_name] = battery

    def setup_default_values(self):
        """设置默认值"""
        # IP地址设置
        self.ui.lineEdit_adress.setText("192.168.4.1")
        self.ui.lineEdit_adress.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_adress.setStyleSheet("font-weight: bold;")
        
        # 端口设置
        self.ui.lineEdit_port.setText("8080")
        self.ui.lineEdit_port.setAlignment(Qt.AlignCenter)
        self.ui.lineEdit_port.setStyleSheet("font-weight: bold;")
        
        # 状态显示设置
        self.ui.lineEdit_state.setAlignment(Qt.AlignCenter)
        self.update_status("未连接", "red")
        
        # 按钮文本设置
        self.ui.pushButton_con_device.setText("连接设备")
        self.ui.pushButton_cel_device.setText("断开连接")

    def setup_connections(self):
        """设置信号连接"""
        self.ui.pushButton_con_device.clicked.connect(self.connect_device)
        self.ui.pushButton_cel_device.clicked.connect(self.disconnect_device)

    def connect_device(self):
        """连接设备支持TCP和SSH"""
        if self.is_connected:
            self.update_status("设备已连接", "green")
            return
            
        try:
            ip = self.ui.lineEdit_adress.text()
            
            # 尝试SSH连接
            try:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(
                    hostname=ip,
                    port=22,
                    username="nvidia",
                    password="nvidia",
                    timeout=5
                )
                self.ip = ip
                logging.info(f"SSH连接成功：{ip}")
            except Exception as e:
                logging.error(f"SSH连接失败: {e}")
                self.ssh_client = None
            
            # 继续TCP连接
            port = int(self.ui.lineEdit_port.text())
            self.thread_pool.submit(self._connect_thread, ip, port)
            
        except ValueError:
            self.update_status("端口号格式错误", "red")


    def _connect_thread(self, ip: str, port: int):
        """连接线程"""
        try:
            with self.socket_lock:
                if self.client_socket:
                    self.client_socket.close()
                    self.client_socket = None
                
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(5)
                self.client_socket.connect((ip, port))
                self.client_socket.setblocking(False)
            
            self.is_connected = True
            self.stop_event.clear()
            self.update_status(f"已连接到 {ip}:{port}", "green")
            logging.info(f"成功连接到 {ip}:{port}")
            
            # 启动数据接收
            self.thread_pool.submit(self._receive_data)
            
        except Exception as e:
            logging.error(f"连接失败: {e}")
            self.update_status(f"连接失败: {str(e)}", "red")
            self.disconnect_device()

    def _receive_data(self):
        """数据接收处理"""
        buffer = bytearray()
        while self.is_connected and not self.stop_event.is_set():
            try:
                with self.socket_lock:
                    if not self.client_socket:
                        break
                    
                    readable, _, _ = select.select([self.client_socket], [], [], 0.1)
                    
                    if readable:
                        data = self.client_socket.recv(8192)
                        if not data:
                            self.disconnect_device()
                            break
                        
                        print(f"接收原始数据: {data}")  # 打印原始数据
                        buffer.extend(data)
                        
                        # 处理完整数据行
                        while b'\n' in buffer:
                            line, buffer = buffer.split(b'\n', 1)
                            try:
                                decoded_line = line.decode('utf-8').strip()
                                print(f"解析数据行: {decoded_line}")  # 打印解析后的数据
                                if decoded_line:
                                    self.data_queue.put(decoded_line)
                            except UnicodeDecodeError:
                                logging.warning("数据解码错误")
                            
            except socket.error as e:
                if e.errno not in (socket.EAGAIN, socket.EWOULDBLOCK):
                    logging.error(f"接收数据错误: {e}")
                    self.disconnect_device()
                    break
            except Exception as e:
                logging.error(f"接收数据错误: {e}")
                self.disconnect_device()
                break

    def process_data(self):
        """处理数据队列中的数据"""
        try:
            while not self.data_queue.empty():
                line = self.data_queue.get_nowait()
                self._parse_data_line(line)
        except queue.Empty:
            pass
        except Exception as e:
            logging.error(f"数据处理错误: {e}")


    def update_display(self):
        """更新波形显示"""
        if not self.display_enabled:
            return
        # 波形显示的更新逻辑移到这里
        pass

    def _parse_data_line(self, line):
        """解析数据行"""
        try:
            if line.startswith('D1:'):
                parts = line.split(':')[1].strip().split(',')
                if len(parts) >= 12:
                    try:
                        wave_data = [float(x) for x in parts[:11]]
                        # 数据存储和波形显示分开处理
                        if self.data_collection_started:
                            self.data_storage.store_glove_data(wave_data)
                        if self.display_enabled and hasattr(self.main_window, 'wave1_controller'):
                            self.main_window.wave1_controller.update_plots(wave_data)
                    except ValueError as e:
                        print(f"波形数据转换错误: {e}")
                        
                    # 处理电量数据
                    try:
                        value = float(parts[11].strip())
                        self.batteries["battery1"].battery_level = value
                    except ValueError as e:
                        print(f"电量数据转换错误: {e}")
            
                
            elif line.startswith('D2:'):
                parts = line.split(':')[1].strip().split(',')
                if len(parts) >= 4:
                    try:
                        emg_data = [float(x) for x in parts[:4]]
                        if self.data_collection_started:
                            self.data_storage.store_emg_data(emg_data)
                        if self.display_enabled and hasattr(self.main_window, 'wave2_controller'):
                            self.main_window.wave2_controller.update_plots(emg_data)
                    except ValueError as e:
                        print(f"EMG数据转换错误: {e}")

            elif line.startswith('B2:'):
                value = float(line.split('B2:')[1].split(',')[0].strip())
                print(f"设备2电量值: {value}")
                self.batteries["battery2"].battery_level = value


            elif line.startswith('D3:'):
                parts = line.split(':')[1].strip().split(',')
                if len(parts) >= 2:
                    try:
                        eog_data = [float(x) for x in parts[:2]]
                        if self.data_collection_started:
                            self.data_storage.store_eog_data(eog_data)
                        if self.display_enabled and hasattr(self.main_window, 'wave3_controller'):
                            self.main_window.wave3_controller.update_plots(eog_data)
                    except ValueError as e:
                        self.logger.error(f"EOG数据转换错误: {e}")

            elif line.startswith('I3:'):
                parts = line.split(':')[1].strip().split(',')
                if len(parts) >= 3:
                    try:
                        imu_data = [float(x) for x in parts[:3]]
                        if self.data_collection_started:
                            self.data_storage.store_imu_data(imu_data)
                        if self.display_enabled and hasattr(self.main_window, 'wave4_controller'):
                            self.main_window.wave4_controller.update_plots(imu_data)
                    except ValueError as e:
                        self.logger.error(f"IMU数据转换错误: {e}")

                
            elif line.startswith('B3:'):
                value = float(line.split('B3:')[1].strip())
                print(f"设备3电量值: {value}")
                self.batteries["battery3"].battery_level = value
            
                
        except (ValueError, IndexError) as e:
            logging.warning(f"数据解析错误: {line} - {e}")

    def disconnect_device(self):
        """断开设备连接"""
        if not self.is_connected:
            self.update_status("设备未连接", "red")
            return
        
        self.stop_event.set()  # 设置停止标志
    

        if self.ssh_client:
            try:
                self.ssh_client.close()
                self.ssh_client = None
            except Exception as e:
                logging.error(f"关闭SSH连接时出错: {e}")
        
        self.is_connected = False
        self.ip = None
        
        with self.socket_lock:
            if self.client_socket:
                try:
                    self.client_socket.close()
                except Exception as e:
                    logging.error(f"关闭连接时出错: {e}")
                finally:
                    self.client_socket = None
        
        self.is_connected = False
        self.data_queue.queue.clear()
        self.update_status("已断开连接", "red")
        logging.info("已断开连接")


    def update_status(self, message, color):
        """更新状态显示"""
        self.ui.lineEdit_state.setText(message)
        self.ui.lineEdit_state.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def stop_data_receiving(self):
        """停止波形显示"""
        try:
            self.display_enabled = False
            self.display_timer.stop()
            self.logger.info("波形显示已停止")
        except Exception as e:
            self.logger.error(f"停止波形显示失败: {e}")

    def start_data_receiving(self):
        """开始波形显示"""
        try:
            self.display_enabled = True
            self.display_timer.start()
            self.logger.info("波形显示已开始")
        except Exception as e:
            self.logger.error(f"启动波形显示失败: {e}")


    def cleanup(self):
        """清理资源"""
        if not self.is_running:
            return
            
        print("开始清理资源...")
        try:
            self.is_running = False
            self.stop_event.set()
            
            # 停止所有定时器
            for timer in [self.process_timer, self.display_timer]:
                if timer is not None:
                    try:
                        timer.stop()
                        timer.deleteLater()
                    except:
                        pass
            
            self.process_timer = None
            self.display_timer = None
            

            if self.ssh_client:
                try:
                    self.ssh_client.close()
                    self.ssh_client = None
                except:
                    pass
            
            # 停止定时器
            if self.process_timer is not None:
                try:
                    self.process_timer.stop()
                    self.process_timer.deleteLater()  # 正确删除Qt定时器
                except:
                    pass
                self.process_timer = None
            
            # 断开连接
            try:
                self.disconnect_device()
            except:
                pass
                
            # 关闭线程池
            if self.thread_pool:
                try:
                    self.thread_pool.shutdown(wait=False)
                except:
                    pass
                self.thread_pool = None
            
            # 清空数据队列
            try:
                while not self.data_queue.empty():
                    self.data_queue.get_nowait()
            except:
                pass
                
            print("资源清理完成")
            
        except Exception as e:
            print(f"清理资源时出错: {e}")
        
        finally:
            self.is_running = False
    
    def start_data_collection(self):
        """开始数据采集"""
        try:
            self.data_storage.start_storage()
            self.data_collection_started = True
            self.status_update_timer.start()
        except Exception as e:
            print(f"启动数据采集失败: {e}")

    def stop_data_collection(self):
        """停止数据采集"""
        try:
            self.data_storage.stop_storage()
            self.data_collection_started = False
        except Exception as e:
            print(f"停止数据采集失败: {e}")

    def update_storage_status(self):
        """更新存储状态显示"""
        if hasattr(self, 'data_storage'):
            status = self.data_storage.get_storage_status()
            self.ui.lineEdit_display1.setText(status)



    def __del__(self):
        """析构函数"""
        if hasattr(self, 'is_running') and self.is_running:
            print("正在执行清理...")
            self.cleanup()
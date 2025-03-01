"""
实验页面控制器模块
包含手势识别和机器人控制相关功能

主要类:
- PredictThread: 预测线程类
- RealTimePredictor: 实时预测器类 
- ExperimentPageController: 实验页面主控制器
- SSHConnectThread: SSH连接线程
- CommandExecuteThread: 命令执行线程
"""

# 标准库导入
import os
import numpy as np
import logging
import queue
import time
from collections import deque
from threading import Thread

# 第三方库导入
from scipy.signal import butter, filtfilt
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QTextCursor
import paramiko
import joblib

class PredictThread(QThread):
    """预测线程类,用于异步处理预测"""
    prediction_signal = pyqtSignal(tuple)

    def __init__(self, predictor):
        super().__init__()
        self.predictor = predictor

    def run(self):
        self.predictor.start(self.handle_prediction)

    def handle_prediction(self, result):
        self.prediction_signal.emit(result)


class SSHConnectThread(QThread):
    """SSH连接线程类"""
    connected_signal = pyqtSignal(bool, str, object)

    def __init__(self, ip, username, password):
        super().__init__()
        self.ip = ip
        self.username = username
        self.password = password

    def run(self):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(
                hostname=self.ip,
                port=22,
                username=self.username,
                password=self.password,
                timeout=10
            )
            self.connected_signal.emit(True, "SSH连接成功", ssh_client)
        except Exception as e:
            self.connected_signal.emit(False, str(e), None)



class CommandExecuteThread(QThread):
    """命令执行线程类"""
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, ssh_client):
        super().__init__()
        self.ssh_client = ssh_client
        self.terminals = []
        self.is_running = True

    def run(self):
        try:
            # 创建终端
            for i in range(3):
                channel = self.ssh_client.invoke_shell()
                self.terminals.append(channel)
                self.progress_signal.emit(f"创建终端 {i+1}")

            # 终端1命令
            self.progress_signal.emit("\n====== 终端1：编译和启动roscore ======\n")
            commands1 = [
                "cd ~/tianbot_ws",
                "catkin_make",
                "source ~/tianbot_ws/devel/setup.bash",
                "roscore\n"
            ]
            self.execute_terminal_commands(0, commands1)
            self.msleep(10000)  # 等待

            # 终端2命令
            self.progress_signal.emit("\n====== 终端2：启动底盘 ======\n")
            commands2 = [
                "source ~/tianbot_ws/devel/setup.bash",
                "roslaunch tianbot_bringup tianbot_bringup.launch\n"
            ]
            self.execute_terminal_commands(1, commands2)
            self.msleep(10000)  # 等待

            # 终端3命令
            self.progress_signal.emit("\n====== 终端3：启动键盘控制 ======\n")
            commands3 = [
                "source ~/tianbot_ws/devel/setup.bash",
                "rosrun teleop_twist_keyboard teleop_twist_keyboard.py _key_timeout:=0.1 cmd_vel:=/tianbot_01/cmd_vel"
            ]

             # 执行命令
            for cmd in commands3:
                self.terminals[2].send(cmd + "\n")
                self.msleep(200)  # 适当的等待时间

            # 初始化终端
            init_sequence = [
                '\n',  # 回车确认
                ' '    # 空格键，确保终端准备就绪
            ]
            for key in init_sequence:
                self.terminals[2].send(key)
                self.msleep(100)

            self.finished_signal.emit(True, "所有终端任务已启动")

        except Exception as e:
            self.finished_signal.emit(False, str(e))

    def execute_terminal_commands(self, terminal_index, commands):
        for cmd in commands:
            if not self.is_running:
                break
            self.terminals[terminal_index].send(cmd + "\n")
            self.msleep(1000)  # 等待1秒
            while self.terminals[terminal_index].recv_ready():
                output = self.terminals[terminal_index].recv(1024).decode('utf-8')
                self.progress_signal.emit(output)

    def stop(self):
        self.is_running = False



class RealTimePredictor:
    """实时预测器类,用于手势识别"""
    def __init__(self, model, scaler=None):
        self.model = model
        self.data_queue = queue.Queue()
        self.window_size = 10  # 10帧，活动段分割窗口大小（注意和训练过程保持一致）
        self.overlap = 0.5
        self.energy_threshold = 3.0  # 阈值
        self.is_running = False
        self.process_thread = None
        self.buffer = deque(maxlen=self.window_size)
        self.last_prediction = "握拳"
        self.last_active = False
        self.debug = True
        self.debug_info = {
            'buffer_size': 0,
            'energy_value': 0.0,
            'feature_dims': 0,
            'prediction_confidence': 0.0,
            'all_probas': {},
            'top_3_predictions': []
        }


    def start(self, callback):
        """启动预测处理"""
        self.is_running = True
        self.process_thread = Thread(target=self.process_data, args=(callback,))
        self.process_thread.daemon = True
        self.process_thread.start()

    def stop(self):
        """停止预测处理"""
        self.is_running = False
        if self.data_queue:
            self.data_queue.put(None)  # 发送停止信号
        if self.process_thread:
            self.process_thread.join()

    def add_data(self, data):
        """添加新数据到队列"""
        if self.is_running:
            self.data_queue.put(data)

    def extract_features(self, data):
        """特征提取"""
        try:
            # 计算统计特征
            mean_values = np.mean(data, axis=0)
            max_values = np.max(data, axis=0)
            std_values = np.std(data, axis=0)
            
            # 计算变化率
            change_rates = []
            for i in range(data.shape[1]):
                if i < 5:  # 弯曲传感器
                    change_rate = np.mean(np.abs(np.diff(data[:, i])))
                else:  # 压力传感器
                    change_rate = np.sum(np.abs(np.diff(data[:, i])))
                change_rates.append(change_rate)
        
            features = []
            # 弯曲传感器特征 (bend1-5)
            for i in range(5):
                features.extend([
                    mean_values[i],
                    max_values[i],
                    change_rates[i],
                    std_values[i]
                ])
            
            # 压力传感器特征 (stress1-3)
            for i in range(5, 8):
                features.extend([
                    mean_values[i],
                    max_values[i],
                    change_rates[i],
                    std_values[i]
                ])
                
            if self.debug:
                print("\n====== 特征提取 ======")
                print(f"特征维度: {len(features)}")
                print(f"特征值范围: {np.min(features):.4f} ~ {np.max(features):.4f}")
                
            return np.array(features)
            
        except Exception as e:
            print(f"特征提取错误: {str(e)}")
            return None


    def process_data(self, callback):
        """数据处理线程"""
        print("预测处理线程启动")
        while self.is_running:
            try:
                new_data = self.data_queue.get(timeout=0.5)
                if new_data is None:
                    break
                    
                self.buffer.append(new_data)
                self.debug_info['buffer_size'] = len(self.buffer)
                print(f"缓冲区大小: {len(self.buffer)}/{self.window_size}")
                
                if len(self.buffer) >= self.window_size:
                    data_array = np.array(list(self.buffer))
                    
                    # 直接计算能量，不进行滤波
                    bend_energy = np.sum(np.square(data_array[:, :5]), axis=1)
                    stress_energy = np.sum(np.square(data_array[:, 5:8]), axis=1)
                    total_energy = 0.7 * bend_energy + 0.3 * stress_energy
                    mean_energy = np.mean(total_energy)
                    
                    self.debug_info['energy_value'] = mean_energy
                    print(f"\n能量值: {mean_energy:.4f} (阈值: {self.energy_threshold})")
                    
                    is_active = mean_energy > self.energy_threshold
                    
                    if not is_active:
                        self.last_prediction = "握拳"
                        self.last_active = False
                        self.debug_info['feature_dims'] = 0
                        self.debug_info['prediction_confidence'] = 0.0
                        self.debug_info['all_probas'] = {}
                        self.debug_info['top_3_predictions'] = []
                        print("状态: 静止")
                    else:
                        print("状态: 活动")
                        features = self.extract_features(data_array)
                        if features is not None:
                            self.debug_info['feature_dims'] = len(features)
                            
                            # 获取预测结果
                            probas = self.model.predict_proba(features.reshape(1, -1))[0]
                            max_prob_idx = np.argmax(probas)
                            
                            self.last_prediction = self.model.classes_[max_prob_idx]
                            print(f"预测结果: {self.last_prediction}")
                            
                            self.debug_info.update({
                                'prediction_confidence': probas[max_prob_idx],
                                'all_probas': dict(zip(self.model.classes_, probas)),
                                'top_3_predictions': [
                                    (self.model.classes_[i], probas[i])
                                    for i in np.argsort(probas)[-3:][::-1]
                                ]
                            })
                            
                            self.last_active = True
                    
                    callback((self.last_prediction, self.last_active, self.debug_info))
                    
                    # 更新缓冲区
                    overlap_size = int(self.window_size * self.overlap)
                    self.buffer = deque(list(self.buffer)[-overlap_size:], maxlen=self.window_size)
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"数据处理错误: {e}")
                import traceback
                print(traceback.format_exc())
                break

class ExperimentPageController(QObject):
    """实验页面主控制器类"""

    def __init__(self, main_window):
        """初始化控制器"""
        super(ExperimentPageController, self).__init__(main_window)
        self.main_window = main_window
        self.ui = main_window.ui
        self.model = None
        self.predictor = None
        self.predict_thread = None
        self.is_collecting = False
        self.last_prediction = "握拳"  # 默认预测结果

        # 日志配置
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # 创建数据更新定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data_display)

        # 添加手势到控制指令的映射
        self.gesture_to_control = {
            '1': {'key': 'j', 'desc': '左转'},
            '3': {'key': 'l', 'desc': '右转'},
            '4': {'key': ',', 'desc': '后退'},
            '5': {'key': 'i', 'desc': '前进'},
            '6': {'key': 'q', 'desc': '增加速度'},
            '8': {'key': 'z', 'desc': '减少速度'},
            '握拳': {'key': 'k', 'desc': '停止'}
        }
        
        # 添加手势状态跟踪
        self.gesture_state = {
            'current_gesture': '握拳',
            'active_count': 0,
            'last_command_time': time.time(),
            'min_active_count': 2,  # 需要连续识别到2次才触发
            'command_cooldown': 0.05,  # 初始冷却时间
            'continuous_mode': False,  # 是否处于持续发送模式
            'command_timer': QTimer(),  # 用于持续发送命令的定时器
        }
        
        # 只调用一次初始化函数
        self.setup_connections()
        self.setup_ui()

        self.gesture_state['command_timer'].timeout.connect(self.send_continuous_command)
        self.gesture_state['command_timer'].setInterval(50)  # 50ms发送一次命令
    
        
    def setup_ui(self):
        """设置UI初始状态"""
        # 设置数据显示区域
        self.ui.lineEdit_control_ip.setText("192.168.4.2")
        self.ui.lineEdit_control_port.setText("22")
        self.ui.textEdit.setReadOnly(True)
        self.ui.textEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.ui.textEdit.setStyleSheet(
            "QTextEdit { font-family: Consolas; font-size: 16px; }"
        )
        
        # 设置预测结果显示区域
        self.ui.textEdit_result1.setReadOnly(True)
        self.ui.textEdit_result1.setLineWrapMode(QTextEdit.NoWrap)
        self.ui.textEdit_result1.setStyleSheet(
            "QTextEdit { font-family: Consolas; font-size: 16px; }"
        )
        
        # 初始状态设置
        self.ui.pushButton_begin1.setEnabled(True)
        self.ui.pushButton_end1.setEnabled(False)
        self.ui.textEdit_result1.setText("预测结果：握拳\n(静止状态)")

        # 设置ROS节点信息显示区域
        self.ui.textEdit_result2.setReadOnly(True)
        self.ui.textEdit_result2.setLineWrapMode(QTextEdit.NoWrap)
        self.ui.textEdit_result2.setStyleSheet(
            "QTextEdit { font-family: Consolas; font-size: 16px; }"
        )
        # 设置焦点策略，使其可以接收键盘事件
        self.ui.textEdit_result2.setFocusPolicy(Qt.StrongFocus)
        # 安装事件过滤器
        self.ui.textEdit_result2.installEventFilter(self)

    def setup_connections(self):
        """设置信号和槽的连接"""
        self.ui.pushButton_input1.clicked.connect(self.load_model)
        self.ui.pushButton_output1.clicked.connect(self.unload_model)
        self.ui.pushButton_begin1.clicked.connect(self.start_data_collection)
        self.ui.pushButton_end1.clicked.connect(self.stop_data_collection)
        self.ui.pushButton_control.clicked.connect(self.connect_to_device)
        self.ui.pushButton_dis_control.clicked.connect(self.stop_ros_nodes)


    def send_continuous_command(self):
        """持续发送当前手势对应的命令"""
        try:
            if hasattr(self, 'terminals') and len(self.terminals) > 2:
                current_gesture = self.gesture_state['current_gesture']
                if current_gesture in self.gesture_to_control:
                    control = self.gesture_to_control[current_gesture]
                    self.terminals[2].send(control['key'])
                    self.logger.debug(f"持续发送命令: {control['desc']}")
        except Exception as e:
            self.logger.error(f"持续发送命令错误: {str(e)}")
            self.gesture_state['command_timer'].stop()
            self.gesture_state['continuous_mode'] = False

    

    def update_prediction(self, result):
        """更新预测结果显示"""
        try:
            prediction, is_active, debug_info = result
            self.handle_gesture_control(prediction, is_active)
            
            # 构建详细的显示文本
            display_text = "======== 预测状态 ========\n"
            display_text += f"预测结果：{prediction}\n"
            display_text += f"状态：{'活动' if is_active else '静止'}\n"
            display_text += "\n======== 调试信息 ========\n"
            display_text += f"缓冲区大小: {debug_info['buffer_size']}/{self.predictor.window_size}\n"
            display_text += f"能量值: {debug_info['energy_value']:.4f}\n"
            display_text += f"能量阈值: {self.predictor.energy_threshold}\n"
            
            if is_active:
                display_text += f"特征维度: {debug_info['feature_dims']}\n"
                display_text += f"\n======== 预测概率 ========\n"
                
                # 显示当前预测结果及其置信度
                display_text += f"当前预测: {prediction} ({debug_info['prediction_confidence']:.4f})\n"
                
                # 显示前3个最可能的预测结果
                display_text += "\n前3个可能的预测结果:\n"
                for gesture, prob in debug_info['top_3_predictions']:
                    display_text += f"{gesture}: {prob:.4f}\n"
                
                # 显示所有类别的预测概率
                display_text += "\n所有类别预测概率:\n"
                sorted_probas = sorted(
                    debug_info['all_probas'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                for gesture, prob in sorted_probas:
                    display_text += f"{gesture}: {prob:.4f}\n"
            
            # 更新到界面
            self.ui.textEdit_result1.setText(display_text)
            self.ui.textEdit_result1.repaint()
            
            # 记录日志
            self.logger.debug(f"预测结果更新:\n{display_text}")
            
        except Exception as e:
            self.logger.error(f"更新预测结果显示错误: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
    

    def eventFilter(self, obj, event):
        """事件过滤器，处理textEdit_result2的键盘事件"""
        if obj == self.ui.textEdit_result2 and event.type() == event.KeyPress:
            if hasattr(self, 'terminals') and len(self.terminals) > 2:
                key = event.text()
                control_keys = {
                    'i': '前进',
                    ',': '后退',
                    'j': '左转',
                    'l': '右转',
                    'k': '停止',
                    'q': '增加速度',
                    'z': '减少速度'
                }
                
                if key in control_keys:
                    try:
                        self.terminals[2].send(key)
                        self.ui.textEdit_result2.append(f"\n发送控制命令: {control_keys[key]}")
                        self.ui.textEdit_result2.moveCursor(QTextCursor.End)  # 修改这里
                        return True  # 事件已处理
                    except Exception as e:
                        self.logger.error(f"发送控制命令错误: {e}")
                        
            return True  # 阻止事件继续传播
        
        return super().eventFilter(obj, event)  # 其他事件正常处理




    

    def update_data_display(self):
        """更新数据显示"""
        if not self.is_collecting:
            return
                
        try:
            if hasattr(self.main_window, 'connect_controller'):
                connect_ctrl = self.main_window.connect_controller
                
                while not connect_ctrl.data_queue.empty():
                    try:
                        line = connect_ctrl.data_queue.get_nowait()
                        if line.startswith('D1:'):
                            parts = line.split(':')[1].strip().split(',')
                            if len(parts) >= 11:
                                try:
                                    sensor_data = [float(x) for x in parts[:8]]
                                    
                                    # 发送数据到预测器
                                    if self.predictor:
                                        self.predictor.add_data(sensor_data)
                                    
                                    # 更新显示
                                    bend_values = sensor_data[:5]
                                    stress_values = sensor_data[5:8]
                                    
                                    display_text = "数据手套传感器数据:\n"
                                    display_text += "-" * 30 + "\n"
                                    display_text += "弯曲传感器数据:\n"
                                    for i, value in enumerate(bend_values, 1):
                                        display_text += f"Bend{i}: {value:8.3f}\n"
                                    
                                    display_text += "-" * 30 + "\n"
                                    display_text += "压力传感器数据:\n"
                                    for i, value in enumerate(stress_values, 1):
                                        display_text += f"Stress{i}: {value:8.3f}\n"
                                    
                                    self.ui.textEdit.setText(display_text)
                                    
                                except ValueError as e:
                                    self.logger.error(f"数据转换错误: {e}")
                            
                    except queue.Empty:
                        break
                    except Exception as e:
                        self.logger.error(f"数据处理错误: {e}")
                        
        except Exception as e:
            self.logger.error(f"更新显示错误: {e}")
            import traceback
            self.logger.error(traceback.format_exc())

    

    def handle_gesture_control(self, prediction, is_active):
        try:
            current_time = time.time()
            prediction = str(prediction)
            
            # 如果不是活动状态，停止所有控制
            if not is_active:
                if self.gesture_state['continuous_mode']:
                    self.gesture_state['command_timer'].stop()
                    self.gesture_state['continuous_mode'] = False
                if self.gesture_state['current_gesture'] != '握拳':
                    self.ui.textEdit_result2.append("\n状态：静止")
                    self.ui.textEdit_result2.moveCursor(QTextCursor.End)
                self.gesture_state['current_gesture'] = '握拳'
                self.gesture_state['active_count'] = 0
                return
            
            # 如果是当前手势且在手势映射中存在
            if prediction in self.gesture_to_control:
                # 如果手势改变，重置计数和持续模式
                if prediction != self.gesture_state['current_gesture']:
                    if self.gesture_state['continuous_mode']:
                        self.gesture_state['command_timer'].stop()
                        self.gesture_state['continuous_mode'] = False
                    self.gesture_state['current_gesture'] = prediction
                    self.gesture_state['active_count'] = 1
                    status_text = f"\n检测到新手势: {prediction}"
                    self.ui.textEdit_result2.append(status_text)
                else:
                    # 同一手势，增加计数
                    self.gesture_state['active_count'] += 1
                    status_text = f"\n手势 {prediction} 连续识别次数: {self.gesture_state['active_count']}/{self.gesture_state['min_active_count']}"
                    self.ui.textEdit_result2.append(status_text)
                
                self.ui.textEdit_result2.moveCursor(QTextCursor.End)
                
                # 检查是否达到触发条件且未处于持续模式
                if (self.gesture_state['active_count'] >= self.gesture_state['min_active_count'] and 
                    not self.gesture_state['continuous_mode']):
                    
                    if hasattr(self, 'terminals') and len(self.terminals) > 2:
                        try:
                            control = self.gesture_to_control[prediction]
                            
                            # 启动持续发送模式
                            self.gesture_state['continuous_mode'] = True
                            self.gesture_state['command_timer'].start()
                            
                            # 显示控制信息
                            control_info = (
                                f"\n{'='*30}"
                                f"\n开始持续发送控制命令:"
                                f"\n手势: {prediction}"
                                f"\n动作: {control['desc']}"
                                f"\n{'='*30}"
                            )
                            self.ui.textEdit_result2.append(control_info)
                            self.ui.textEdit_result2.moveCursor(QTextCursor.End)
                            
                        except Exception as e:
                            error_msg = f"\n发送控制命令错误: {str(e)}"
                            self.logger.error(error_msg)
                            self.ui.textEdit_result2.append(error_msg)
                            self.ui.textEdit_result2.moveCursor(QTextCursor.End)
            else:
                # 无效手势，停止持续模式
                if self.gesture_state['continuous_mode']:
                    self.gesture_state['command_timer'].stop()
                    self.gesture_state['continuous_mode'] = False
                self.gesture_state['current_gesture'] = prediction
                self.gesture_state['active_count'] = 0

        except Exception as e:
            error_msg = f"\n手势控制处理错误: {str(e)}"
            self.logger.error(error_msg)
            self.ui.textEdit_result2.append(error_msg)
            self.ui.textEdit_result2.moveCursor(QTextCursor.End)


    def load_model(self):
        """加载模型文件"""
        try:
            models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
            file_name, _ = QFileDialog.getOpenFileName(
                self.main_window,
                "选择模型文件",
                models_dir,
                "Model Files (*.pkl);;All Files (*)"
            )

            if file_name:
                # 加载模型和缩放器
                model_data = joblib.load(file_name)
                if isinstance(model_data, dict):
                    self.model = model_data['model']
                    scaler = model_data.get('scaler')
                else:
                    self.model = model_data
                    scaler = None
                    
                # 创建预测器
                self.predictor = RealTimePredictor(
                    model=self.model,
                    scaler=scaler
                )
                self.predict_thread = PredictThread(self.predictor)
                self.predict_thread.prediction_signal.connect(self.update_prediction)
                
                self.ui.textEdit.setText(f"当前加载的模型：{os.path.basename(file_name)}")
                self.show_message("成功", f"模型已成功加载：\n{os.path.basename(file_name)}")
                
        except Exception as e:
            self.logger.error(f"加载模型错误: {e}")
            self.show_error(f"加载模型时出错：\n{str(e)}")

    
    def unload_model(self):
        """删除当前加载的模型"""
        if self.model is not None:
            self.model = None
            if self.predictor:
                self.predictor.stop()
            self.predictor = None
            self.predict_thread = None
            self.ui.textEdit.setText("当前未加载模型")
            self.show_message("成功", "模型已成功卸载")
        else:
            self.show_warning("当前没有加载任何模型")


    def start_data_collection(self):
        """开始数据采集"""
        if not self.model:
            self.show_warning("请先加载模型")
            return
            
        if not hasattr(self.main_window, 'connect_controller') or \
           not self.main_window.connect_controller.is_connected:
            self.show_warning("请先连接设备")
            return
            
        connect_ctrl = self.main_window.connect_controller
        connect_ctrl.data_collection_started = True
        
        # 启动预测线程
        if self.predictor:
            self.predict_thread.start()
        
        self.is_collecting = True
        self.update_timer.start()
        self.ui.pushButton_begin1.setEnabled(False)
        self.ui.pushButton_end1.setEnabled(True)
        self.logger.info("开始数据采集")



    def stop_data_collection(self):
        """停止数据采集"""
        if hasattr(self.main_window, 'connect_controller'):
            self.main_window.connect_controller.data_collection_started = False
        
        # 停止预测器
        if self.predictor:
            self.predictor.stop()
        
        self.is_collecting = False
        self.update_timer.stop()
        self.ui.pushButton_begin1.setEnabled(True)
        self.ui.pushButton_end1.setEnabled(False)
        self.logger.info("停止数据采集")
    

    def connect_to_device(self):
        """连接到设备并启动终端任务"""
        try:
            ip = self.ui.lineEdit_control_ip.text()
            if not ip:
                self.show_warning("请输入设备IP地址")
                return
                
            if "无人车ip：" in ip:
                ip = ip.replace("无人车ip：", "").strip()

            # 禁用按钮，避免重复点击
            self.ui.pushButton_control.setEnabled(False)
            
            # 创建并启动SSH连接线程
            self.ssh_thread = SSHConnectThread(ip, "nvidia", "nvidia")
            self.ssh_thread.connected_signal.connect(self.on_ssh_connected)
            self.ssh_thread.start()
            
        except Exception as e:
            self.logger.error(f"连接设备错误: {e}")
            self.show_error(f"连接设备时出错：\n{str(e)}")
            self.ui.pushButton_control.setEnabled(True)


    def stop_ros_nodes(self):
        """停止ROS节点和清理终端"""
        try:
            if hasattr(self.main_window, 'connect_controller') and \
            self.main_window.connect_controller.ssh_client:
                ssh_client = self.main_window.connect_controller.ssh_client
                
                # 首先清理所有终端会话
                if hasattr(self, 'terminals'):
                    self.ui.textEdit_result2.append("\n====== 停止所有终端进程 ======")
                    for i, terminal in enumerate(self.terminals):
                        try:
                            # 发送Ctrl+C停止进程
                            terminal.send('\x03')
                            time.sleep(1)  # 等待进程响应
                            # 读取终端输出
                            while terminal.recv_ready():
                                output = terminal.recv(1024).decode('utf-8')
                                self.ui.textEdit_result2.append(output)
                            terminal.close()
                            self.logger.info(f"终端 {i+1} 已关闭")
                        except Exception as e:
                            self.logger.error(f"关闭终端 {i+1} 错误: {e}")
                    self.terminals = []
                
                def execute_stop_command(cmd, description):
                    """执行停止命令并显示结果"""
                    self.logger.info(f"{description}...")
                    self.ui.textEdit_result2.append(f"\n====== {description} ======\n")
                    stdin, stdout, stderr = ssh_client.exec_command(cmd)
                    error = stderr.read().decode('utf-8')
                    output = stdout.read().decode('utf-8')
                    if error:
                        self.logger.error(f"{description}错误：{error}")
                        self.ui.textEdit_result2.append(f"错误：\n{error}")
                    if output:
                        self.ui.textEdit_result2.append(output)
                
                # 按顺序停止所有节点
                commands = [
                    ("pkill -f 'rostopic pub.*cmd_vel'", "停止转圈任务"),
                    ("pkill -f teleop_twist_keyboard", "停止键盘控制"),
                    ("pkill -f tianbot_bringup.launch", "停止底盘"),
                    ("sleep 2 && pkill -f roscore", "停止roscore"),  # 延迟确保其他节点先停止
                    ("ps aux | grep ros", "检查ROS进程")  # 检查是否还有ROS进程在运行
                ]
                
                for cmd, desc in commands:
                    execute_stop_command(cmd, desc)
                    time.sleep(1)  # 等待进程完全停止
                
                # 停止定时更新
                if hasattr(self, 'ros_info_timer'):
                    self.ros_info_timer.stop()
                
                # 更新界面显示
                self.ui.textEdit_result2.append("\n====== 清理完成 ======")
                self.ui.textEdit_result2.append("所有ROS节点已停止")
                self.show_message("成功", "所有ROS节点已停止")
                
                # 重置连接状态
                self.main_window.connect_controller.is_connected = False
                
        except Exception as e:
            self.logger.error(f"停止ROS节点错误: {e}")
            self.show_error(f"停止ROS节点时出错：\n{str(e)}")





    def execute_init_commands(self, ssh_client):
        """按顺序在三个终端中执行初始化命令"""
        try:
            # 创建三个终端会话
            terminals = []
            for i in range(3):
                channel = ssh_client.invoke_shell()
                terminals.append(channel)
                self.logger.info(f"创建终端 {i+1}")
            
            # 终端1：编译工作空间并启动roscore
            terminal1_cmds = [
                "cd ~/tianbot_ws",
                "catkin_make",
                "source ~/tianbot_ws/devel/setup.bash",
                "roscore\n"
            ]
            
            # 终端2：启动底盘
            terminal2_cmds = [
                "source ~/tianbot_ws/devel/setup.bash",
                "roslaunch tianbot_bringup tianbot_bringup.launch\n"
            ]
            
            # 终端3：启动键盘控制
            terminal3_cmds = [
                "source ~/tianbot_ws/devel/setup.bash",
                "rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=/tianbot_01/cmd_vel\n"
            ]
            
            # 执行终端1命令
            self.ui.textEdit_result2.append("\n====== 终端1：编译和启动roscore ======\n")
            for cmd in terminal1_cmds:
                terminals[0].send(cmd + "\n")
                time.sleep(1)  # 等待命令执行
                while terminals[0].recv_ready():
                    output = terminals[0].recv(1024).decode('utf-8')
                    self.ui.textEdit_result2.append(output)
                    self.ui.textEdit_result2.repaint()
            
            # 等待roscore完全启动
            time.sleep(15)
            
            # 执行终端2命令
            self.ui.textEdit_result2.append("\n====== 终端2：启动底盘 ======\n")
            for cmd in terminal2_cmds:
                terminals[1].send(cmd + "\n")
                time.sleep(1)
                while terminals[1].recv_ready():
                    output = terminals[1].recv(1024).decode('utf-8')
                    self.ui.textEdit_result2.append(output)
                    self.ui.textEdit_result2.repaint()
            
            # 等待底盘启动
            time.sleep(15)
            
            # 执行终端3命令
            self.ui.textEdit_result2.append("\n====== 终端3：启动键盘控制 ======\n")
            for cmd in terminal3_cmds:
                terminals[2].send(cmd + "\n")
                time.sleep(1)
                while terminals[2].recv_ready():
                    output = terminals[2].recv(1024).decode('utf-8')
                    self.ui.textEdit_result2.append(output)
                    self.ui.textEdit_result2.repaint()
            
            # 保存终端引用以便后续使用
            self.terminals = terminals
            self.show_message("成功", "所有终端任务已启动")
            
        except Exception as e:
            self.logger.error(f"终端命令执行错误: {e}")
            self.show_error(f"终端命令执行错误：\n{str(e)}")

    

    
    
    

    def on_ssh_connected(self, success, message, ssh_client):
        """SSH连接完成回调"""
        try:
            if success:
                if hasattr(self.main_window, 'connect_controller'):
                    self.main_window.connect_controller.ssh_client = ssh_client
                    self.main_window.connect_controller.is_connected = True
                    self.main_window.connect_controller.ip = self.ui.lineEdit_control_ip.text()
                    
                    # 清空显示区域
                    self.ui.textEdit_result2.clear()
                    
                    # 创建并启动命令执行线程
                    self.command_thread = CommandExecuteThread(ssh_client)
                    self.command_thread.progress_signal.connect(self.update_command_progress)
                    self.command_thread.finished_signal.connect(self.on_command_finished)
                    self.command_thread.start()
                else:
                    if ssh_client:
                        ssh_client.close()
                    self.show_error("连接控制器未初始化")
            else:
                self.show_error(f"SSH连接出错：{message}")
                self.logger.error(f"SSH连接异常：{message}")
                
        except Exception as e:
            self.logger.error(f"SSH连接回调错误: {e}")
            self.show_error(f"处理SSH连接时出错：\n{str(e)}")
        finally:
            self.ui.pushButton_control.setEnabled(True)
            if hasattr(self, 'ssh_thread'):
                self.ssh_thread.deleteLater()
                self.ssh_thread = None


    def update_command_progress(self, message):
        """更新命令执行进度"""
        self.ui.textEdit_result2.append(message)
        self.ui.textEdit_result2.repaint()

    def on_command_finished(self, success, message):
        """命令执行完成回调"""
        if success:
            self.show_message("成功", message)
            self.terminals = self.command_thread.terminals
        else:
            self.show_error(f"执行命令出错：{message}")
        
        # 重置命令线程
        self.command_thread.deleteLater()
        self.command_thread = None

    def show_message(self, title, message, icon=QMessageBox.Information):
        """显示消息框"""
        msg = QMessageBox(icon, title, message, QMessageBox.Ok, self.main_window)
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(msg.close)
        timer.start(3000)
        msg.exec_()

    def show_warning(self, message):
        """显示警告消息"""
        self.show_message("警告", message, QMessageBox.Warning)

    def show_error(self, message):
        """显示错误消息"""
        self.show_message("错误", message, QMessageBox.Critical)

    def cleanup(self):
        """清理资源"""
        if self.predictor:
            self.predictor.stop()
        self.is_collecting = False
        if hasattr(self, 'update_timer'):
            self.update_timer.stop()
        
        if hasattr(self, 'ssh_thread'):
            self.ssh_thread.quit()
            self.ssh_thread.wait()

        if hasattr(self, 'command_thread'):
            self.command_thread.stop()
            self.command_thread.wait()

    
    def cleanup_terminals(self):
        """清理终端会话"""
        if hasattr(self, 'terminals'):
            for terminal in self.terminals:
                try:
                    # 发送Ctrl+C停止进程
                    terminal.send('\x03')
                    time.sleep(0.5)
                    # 关闭终端
                    terminal.close()
                except:
                    pass
            self.terminals = []



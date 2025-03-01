from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import numpy as np
import queue
import logging

class WaveThread(QThread):
    # 修改信号类型为列表
    update_signal = pyqtSignal(list)  
    error_signal = pyqtSignal(str)
    
    def __init__(self, channel_count, buffer_size=200):
        """
        初始化波形处理线程
        
        参数:
            channel_count (int): 通道数量
                - 设备1: 11通道 (5弯曲 + 3应力 + 3IMU)
                - 设备2: 4通道 (4个EMG)
                - 设备3: 5通道 (2EOG + 3IMU)
            buffer_size (int): 缓冲区大小，默认200
        """
        super().__init__()
        self.channel_count = channel_count
        self.buffer_size = buffer_size
        self.running = False
        
        # 数据缓冲区
        self.data_buffer = np.zeros((channel_count, buffer_size))
        
        # 线程同步
        self.data_queue = queue.Queue(maxsize=1000)
        self.mutex = QMutex()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"初始化波形线程 - 通道数: {channel_count}")

        
    def run(self):
        """线程运行函数"""
        self.running = True
        self.logger.info("波形处理线程启动")
        
        while self.running:
            try:
                # 等待新数据
                try:
                    data = self.data_queue.get(timeout=0.1)
                    
                    # 使用互斥锁保护数据更新
                    self.mutex.lock()
                    try:
                        # 更新数据缓冲区
                        self.data_buffer = np.roll(self.data_buffer, -1, axis=1)
                        self.data_buffer[:, -1] = data
                        # 发送更新信号，转换为列表
                        self.update_signal.emit(data.tolist() if isinstance(data, np.ndarray) else data)
                    finally:
                        self.mutex.unlock()
                        
                except queue.Empty:
                    continue
                    
            except Exception as e:
                self.error_signal.emit(f"数据处理错误: {str(e)}")
                self.msleep(1)
    
    def add_data(self, data):
        """添加数据到处理队列"""
        try:
            if isinstance(data, list):
                data = np.array(data, dtype=np.float64)
                
            if len(data) != self.channel_count:
                raise ValueError(f"数据通道数不匹配: 期望 {self.channel_count}，实际 {len(data)}")
                
            # 将数据添加到队列
            self.data_queue.put(data, timeout=0.1)
            
        except Exception as e:
            self.error_signal.emit(f"添加数据错误: {str(e)}")
    
    def stop(self):
        """停止线程运行"""
        try:
            self.logger.info("正在停止波形线程...")
            self.running = False
            self.wait()
            self.logger.info("波形线程已停止")
        except Exception as e:
            self.error_signal.emit(f"停止线程错误: {str(e)}")
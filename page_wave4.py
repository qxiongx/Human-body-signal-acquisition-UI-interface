from PyQt5.QtWidgets import QWidget, QVBoxLayout
from wave_widget import WaveWidget
from wave_thread import WaveThread
import logging
import pyqtgraph as pg
import numpy as np

# 设置pyqtgraph全局配置
pg.setConfigOption('background', 'w')  # 白色背景
pg.setConfigOption('foreground', 'k')  # 黑色前景
pg.setConfigOptions(antialias=True)    # 启用抗锯齿

class Wave4PageController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui
        self.logger = logging.getLogger(__name__)
        
        # 初始化波形显示组件
        self.init_wave_widgets()
        
        # 创建波形绘制线程 (3个IMU通道)
        self.wave_thread = WaveThread(channel_count=3, buffer_size=200)
        self.wave_thread.update_signal.connect(self.update_wave_displays)
        self.wave_thread.error_signal.connect(self.handle_error)
        
        # 启动波形线程
        self.wave_thread.start()
        self.logger.info("IMU波形显示线程已启动")
        
    def init_wave_widgets(self):
        """初始化波形显示组件"""
        try:
            # 初始化IMU传感器的波形显示
            self.imu_widgets = []
            
            # 初始化3个IMU传感器波形
            for i in range(3):
                widget = self.create_wave_widget(f'widget_IMU{i+1}', 
                                              f'头动传感器 {i+1}', 'r')
                if widget:
                    self.imu_widgets.append(widget)
                    
        except Exception as e:
            self.logger.error(f"初始化波形显示错误: {e}")

    def create_wave_widget(self, widget_name, title, color):
        """创建单个波形显示组件"""
        try:
            # 获取基础容器
            widget = getattr(self.ui, widget_name)
            if widget is None:
                self.logger.error(f"找不到widget: {widget_name}")
                return None
            
            # 清除可能存在的旧布局
            if widget.layout():
                while widget.layout().count():
                    item = widget.layout().takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
                widget.layout().deleteLater()
            
            # 创建新的波形组件
            wave_widget = WaveWidget(title=title, display_size=200)
            
            # 设置布局
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(wave_widget)
            widget.setLayout(layout)
            
            # 设置波形显示属性
            wave_widget.set_pen_color(color)
            wave_widget.plot_widget.setDownsampling(mode='peak')
            wave_widget.plot_widget.setClipToView(True)
            wave_widget.plot_widget.setMouseEnabled(x=True, y=True)
            
            # 设置网格
            wave_widget.plot_widget.showGrid(x=True, y=True)
            wave_widget.plot_widget.setLabel('left', '角度')
            wave_widget.plot_widget.setLabel('bottom', '采样点')
            
            return wave_widget
                
        except Exception as e:
            self.logger.error(f"创建波形组件错误: {widget_name} - {e}")
            return None
    
    def update_plots(self, data):
        """接收新数据,加入绘制线程队列"""
        try:
            # 验证IMU数据长度
            if len(data) != 3:
                raise ValueError(f"IMU数据长度不正确: {len(data)}")
                
            # 将数据添加到波形线程
            self.wave_thread.add_data(data)
            
        except Exception as e:
            self.logger.error(f"更新波形数据错误: {str(e)}", exc_info=True)
    
    def update_wave_displays(self, data):
        """更新所有波形显示（在主线程中执行）"""
        try:
            # 确保数据是一维数组
            if isinstance(data, np.ndarray):
                data = data.flatten()
            
            # 更新IMU传感器数据
            for i, widget in enumerate(self.imu_widgets):
                if i < 3:
                    try:
                        value = float(data[i])
                        widget.update_data(value)
                    except (ValueError, TypeError) as e:
                        self.logger.error(f"IMU数据转换错误: {e}")
                        
        except Exception as e:
            self.logger.error(f"更新波形显示错误: {str(e)}", exc_info=True)
    
    def handle_error(self, error_msg):
        """处理错误消息"""
        self.logger.error(f"波形显示错误: {error_msg}")
    
    def cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'wave_thread'):
                print("正在停止IMU波形绘制线程...")
                self.wave_thread.stop()
                self.wave_thread.wait()
                print("波形绘制线程已停止")
            
            # 清理所有波形组件
            for widget in self.imu_widgets:
                if widget and widget.parent():
                    widget.setParent(None)
                    widget.deleteLater()
            
            print("IMU波形页面资源清理完成")
            
        except Exception as e:
            self.logger.error(f"清理资源时出错: {e}")

    def start_display(self):
        """开始波形显示"""
        try:
            # 如果线程不存在或已停止，创建新线程
            if not hasattr(self, 'wave_thread') or self.wave_thread is None:
                self.wave_thread = WaveThread(channel_count=3, buffer_size=200)
                self.wave_thread.update_signal.connect(self.update_wave_displays)
                self.wave_thread.error_signal.connect(self.handle_error)
            
            if not self.wave_thread.isRunning():
                self.wave_thread.start()
                print("IMU波形显示已启动")
        except Exception as e:
            print(f"启动IMU波形显示失败: {e}")

    def stop_display(self):
        """停止波形显示"""
        try:
            if hasattr(self, 'wave_thread') and self.wave_thread is not None:
                self.wave_thread.stop()
                self.wave_thread.wait()
                self.wave_thread = None
                print("IMU波形显示已停止")
        except Exception as e:
            print(f"停止IMU波形显示失败: {e}")
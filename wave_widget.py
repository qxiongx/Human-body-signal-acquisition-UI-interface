from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
import numpy as np
import logging

class WaveWidget(QWidget):
    def __init__(self, title="波形图", parent=None, display_size=200):
        super().__init__(parent)
        self.display_size = display_size
        self.logger = logging.getLogger(__name__)
        
        # 初始化数据缓冲
        self.x_data = np.arange(self.display_size)
        self.y_data = np.zeros(self.display_size)
        
        # 设置属性默认值
        self.plot_widget = None
        self.curve = None  # 确保属性存在
        self.auto_range = True
        self.y_margin = 0.1
        
        # 初始化UI
        self._setup_ui(title)
        
    def _setup_ui(self, title):
        """初始化UI组件"""
        try:
            # 创建布局
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # 创建绘图窗口
            self.plot_widget = pg.PlotWidget()
            self.plot_widget.setBackground('w')
            self.plot_widget.setTitle(title, size='12pt')
            self.plot_widget.showGrid(x=True, y=True)
            self.plot_widget.setLabel('left', '数值')
            self.plot_widget.setLabel('bottom', '采样点')
            
            # 设置性能优化参数
            self.plot_widget.setDownsampling(mode='peak')
            self.plot_widget.setClipToView(True)
            self.plot_widget.enableAutoRange(x=False)
            self.plot_widget.setMouseEnabled(x=True, y=True)
            self.plot_widget.setAntialiasing(False)
            
            # 创建曲线对象
            pen = pg.mkPen(color='b', width=1)
            self.curve = self.plot_widget.plot(self.x_data, self.y_data, pen=pen)
            
            # 设置显示范围
            self.plot_widget.setXRange(0, self.display_size)
            self.plot_widget.setYRange(-5, 5)
            
            # 添加到布局
            layout.addWidget(self.plot_widget)
            
            self.logger.debug(f"波形显示组件初始化成功: {title}")
            
        except Exception as e:
            self.logger.error(f"初始化波形显示组件失败: {str(e)}", exc_info=True)
            raise
    
    def update_data(self, new_value):
        """更新波形数据"""
        try:
            # 确保输入数据是浮点数
            value = float(new_value)
            
            # 更新数据缓冲
            self.y_data = np.roll(self.y_data, -1)
            self.y_data[-1] = value
            
            # 更新曲线
            self.curve.setData(self.x_data, self.y_data)
            
            # 如果启用了自动范围，更新Y轴范围
            if self.auto_range:
                self._update_y_range()
                
        except Exception as e:
            self.logger.error(f"更新数据错误: {str(e)}")

    def _update_y_range(self):
        """更新Y轴显示范围"""
        try:
            if len(self.y_data) > 0:
                y_min = float(np.min(self.y_data))
                y_max = float(np.max(self.y_data))
                
                # 确保最大最小值不相等
                if abs(y_max - y_min) < 1e-6:
                    y_min -= 0.1
                    y_max += 0.1
                
                # 计算边距
                margin = (y_max - y_min) * self.y_margin
                
                # 设置新的显示范围
                self.plot_widget.setYRange(
                    y_min - margin,
                    y_max + margin,
                    padding=0
                )
        except Exception as e:
            self.logger.error(f"更新Y轴范围错误: {str(e)}")

    
    def set_pen_color(self, color):
        """设置曲线颜色"""
        self.curve.setPen(pg.mkPen(color=color, width=1))
        
    def set_auto_range(self, enabled=True):
        """设置是否启用自动范围"""
        self.auto_range = enabled
        if enabled:
            self._update_y_range()

    def set_y_margin(self, margin):
        """设置Y轴边距比例"""
        self.y_margin = max(0.0, min(1.0, margin))
        if self.auto_range:
            self._update_y_range()
            
    def reset_y_range(self):
        """重置Y轴范围"""
        self.y_min = float('inf')
        self.y_max = float('-inf')
        self._update_y_range()
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.plot_widget:
                self.plot_widget.close()
                self.plot_widget.deleteLater()
        except Exception as e:
            print(f"清理波形组件错误: {e}")
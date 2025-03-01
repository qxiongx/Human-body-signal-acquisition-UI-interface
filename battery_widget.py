"""
电池电量显示组件模块

此模块负责电池电量的图形显示，包括：
- 电池外观绘制
- 电量状态显示
- 颜色管理
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QSizePolicy

class BatteryWidget(QWidget):
    """电池电量显示组件"""
    
    # 定义颜色常量
    COLOR_HIGH = QColor(0, 255, 0)    # 电量高时显示绿色
    COLOR_MID = QColor(255, 165, 0)   # 电量中等时显示橙色
    COLOR_LOW = QColor(255, 0, 0)     # 电量低时显示红色
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._battery_level = 0
        self.setMinimumSize(150, 45)  # 设置最小尺寸
        self.setMaximumHeight(45)     # 限制最大高度
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    @property
    def battery_level(self):
        return self._battery_level

    @battery_level.setter
    def battery_level(self, value):
        """设置电量值(0-100)"""
        try:
            self._battery_level = max(0, min(100, float(value)))
            self.update()
        except (ValueError, TypeError) as e:
            print(f"电量值设置错误: {e}")

    def _get_battery_color(self):
        """根据电量值获取对应的颜色"""
        if self.battery_level > 50:
            return self.COLOR_HIGH
        elif self.battery_level > 20:
            return self.COLOR_MID
        return self.COLOR_LOW

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # 计算绘制区域
            battery_width = self.width() - 50
            height = 35
            y_offset = (self.height() - height) // 2

            # 绘制电池外框
            pen = QPen(Qt.black, 2)
            painter.setPen(pen)
            painter.drawRect(2, y_offset, battery_width-14, height)
            painter.drawRect(battery_width-12, y_offset + height//3, 10, height//3)

            # 绘制电量条
            if self.battery_level > 0:
                painter.setPen(Qt.NoPen)
                painter.setBrush(self._get_battery_color())
                width = (battery_width-18) * self.battery_level / 100
                painter.drawRect(4, y_offset + 2, width, height - 4)

            # 绘制电量百分比
            painter.setPen(Qt.black)
            text = f"{self.battery_level:.1f}%"
            painter.drawText(battery_width + 5, self.height()//2 + 5, text)

        except Exception as e:
            print(f"电池绘制错误: {e}")
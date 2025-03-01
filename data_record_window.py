from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, 
                           QVBoxLayout, QWidget, QHeaderView)
from PyQt5.QtCore import Qt
import os
from datetime import datetime

class DataRecordWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("数据采集记录")
        self.resize(800, 600)
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "序号",
            "采集时间",
            "手套传感器数据",
            "肌电信号数据",
            "眼电信号数据",
            "惯性测量数据",
            "总采样数",
            "数据标签"
        ])
        
        # 设置表格样式
        header = self.table.horizontalHeader()
        
        # 设置各列的宽度比例
        column_widths = {
            0: 40,   # 序号列
            1: 150,  # 采集时间
            2: 100,  # 手套传感器数据
            3: 100,  # 肌电信号数据
            4: 100,  # 眼电信号数据
            5: 100,  # 惯性测量数据
            6: 80,   # 总采样数
            7: 80    # 数据标签
        }
        
        # 应用列宽设置
        for col, width in column_widths.items():
            self.table.setColumnWidth(col, width)
            header.setSectionResizeMode(col, QHeaderView.Fixed)
        
        # 隐藏垂直表头
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        
    def load_data(self, base_path):
        """加载数据记录"""
        try:
            if not os.path.exists(base_path):
                return
            
            # 获取所有标签文件夹
            data_records = []
            for label_dir in os.listdir(base_path):
                if not label_dir.startswith('label_'):
                    continue
                    
                label_path = os.path.join(base_path, label_dir)
                if os.path.isdir(label_path):
                    try:
                        # 从目录名获取标签
                        label = label_dir.replace('label_', '')
                        
                        # 获取文件修改时间作为采集时间
                        emg_file = os.path.join(label_path, "emg_data.csv")
                        if os.path.exists(emg_file):
                            timestamp = datetime.fromtimestamp(os.path.getmtime(emg_file))
                            data_records.append((timestamp, label_path, label))
                            
                    except Exception as e:
                        print(f"Debug: 处理标签目录 {label_dir} 时出错: {str(e)}")
                        continue
                
            # 按时间倒序排序
            data_records.sort(reverse=True)
            
            # 设置行数
            self.table.setRowCount(len(data_records))
            
            # 填充数据
            for row, (timestamp, label_path, label) in enumerate(data_records):
                # 序号列
                index_item = QTableWidgetItem(str(row + 1))
                index_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 0, index_item)
                
                # 时间列
                time_item = QTableWidgetItem(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                self.table.setItem(row, 1, time_item)
                
                # 统计各类型数据
                total_samples = 0
                data_types = ['glove', 'emg', 'eog', 'imu']
                for col, data_type in enumerate(data_types, 2):
                    file_path = os.path.join(label_path, f"{data_type}_data.csv")
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            line_count = sum(1 for _ in f) - 1  # 减去表头
                            total_samples += line_count
                            count_item = QTableWidgetItem(str(line_count))
                            count_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                            self.table.setItem(row, col, count_item)
                
                # 总采样数
                total_item = QTableWidgetItem(str(total_samples))
                total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, 6, total_item)
                
                # 标签
                label_item = QTableWidgetItem(label)
                label_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, 7, label_item)
            
            # 调整列宽
            self.table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Debug: 加载数据记录时出错: {str(e)}")
            raise
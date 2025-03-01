from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject
import logging

class CleanupHandler(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # 设置窗口关闭事件处理
        self.main_window.closeEvent = self.handle_close_event
        
    def handle_close_event(self, event):
        """处理窗口关闭事件"""
        try:
            self.logger.info("开始清理所有资源...")
            self.cleanup_all()
            event.accept()
        except Exception as e:
            self.logger.error(f"清理资源时出错: {e}")
            event.accept()
        finally:
            QApplication.quit()
            
    def cleanup_all(self):
        """清理所有资源"""
        # 清理波形控制器资源
        if hasattr(self.main_window, 'wave_controller'):
            self.logger.info("正在清理波形控制器...")
            self.main_window.wave_controller.cleanup()
            
        # 清理连接控制器资源
        if hasattr(self.main_window, 'connect_controller'):
            self.logger.info("正在清理连接控制器...")
            self.main_window.connect_controller.cleanup()
            
        # 清理页面控制器资源
        if hasattr(self.main_window, 'page_controller'):
            self.logger.info("正在清理页面控制器...")
            self.main_window.page_controller.cleanup()
            
        self.logger.info("所有资源清理完成")
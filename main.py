import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import Ui_MainWindow
from page_controller import PageController
from page_connect import ConnectPageController
from cleanup_handler import CleanupHandler
from page_wave1 import Wave1PageController
from page_wave2 import Wave2PageController
from page_wave3 import Wave3PageController
from page_wave4 import Wave4PageController
from page_predict import PredictPageController
from page_experiment import ExperimentPageController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.wave_controllers = []  # 用于存储所有波形控制器
        
        # 创建清理处理器
        self.cleanup_handler = CleanupHandler(self)
        
        # 初始化控制器
        self.connect_controller = ConnectPageController(self)
        self.wave1_controller = Wave1PageController(self)
        self.wave2_controller = Wave2PageController(self)
        self.wave3_controller = Wave3PageController(self)
        self.wave4_controller = Wave4PageController(self)
        self.wave_controllers.extend([
            self.wave1_controller,
            self.wave2_controller, 
            self.wave3_controller,
            self.wave4_controller
        ])
        self.predict_controller = PredictPageController(self)
        self.experiment_controller = ExperimentPageController(self)
        # 初始化页面控制器
        self.page_controller = PageController(self)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
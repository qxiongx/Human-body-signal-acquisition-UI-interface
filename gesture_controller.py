import roslibpy
import logging
from collections import deque

class ROSGesturePublisher:
    def __init__(self, host='192.168.4.1', port=9090):
        self.client = roslibpy.Ros(host=host, port=port)
        self.publisher = None
        self.logger = logging.getLogger(__name__)
        self.gesture_buffer = deque(maxlen=5)  # 存储最近5次的手势
        self.last_command = None
        self.gesture_commands = {
            "握拳": "stop",
            "伸掌": "forward",
            "掌心向上": "backward",
            "掌心向左": "turn_left",
            "掌心向右": "turn_right"
        }
        
    def connect(self):
        try:
            self.client.run()
            self.publisher = roslibpy.Topic(
                self.client,
                '/gesture_command',
                'std_msgs/String'
            )
            self.logger.info("已连接到ROS系统")
            return True
        except Exception as e:
            self.logger.error(f"ROS连接失败: {str(e)}")
            return False
            
    def disconnect(self):
        if self.publisher:
            self.publisher.unadvertise()
        if self.client:
            self.client.terminate()
            
    def process_gesture(self, gesture, is_active):
        """处理手势并决定是否发送命令"""
        if not is_active:
            self.gesture_buffer.clear()
            return None
            
        self.gesture_buffer.append(gesture)
        
        # 检查是否从握拳状态转换到其他状态
        if len(self.gesture_buffer) >= 5:
            if all(g == gesture for g in self.gesture_buffer) and \
               gesture != "握拳" and gesture in self.gesture_commands:
                command = self.gesture_commands[gesture]
                if command != self.last_command:
                    self.publish_command(command)
                    self.last_command = command
                    return command
        return None
        
    def publish_command(self, command):
        """发布控制命令到ROS"""
        if not self.publisher:
            return
            
        try:
            message = {'data': command}
            self.publisher.publish(message)
            self.logger.info(f"发布控制命令: {command}")
        except Exception as e:
            self.logger.error(f"发布命令失败: {str(e)}")
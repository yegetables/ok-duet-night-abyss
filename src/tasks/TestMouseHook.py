from ok import TriggerTask, Logger, og
from src.tasks.BaseCombatTask import BaseCombatTask, NotInCombatException, CharDeadException

from pynput import mouse, keyboard
logger = Logger.get_logger(__name__)

class TriggerDeactivateException(Exception):
    """停止激活异常。"""
    pass

class TestMouseHook(BaseCombatTask, TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "测试鼠标按键"
        self.description = "测试鼠标Hook"
        self.connected = False

    def disable(self):
        """禁用任务时，断开信号连接。"""
        if self.connected:
            logger.debug("disconnect on_global_click")
            og.my_app.clicked.disconnect(self.on_global_click)
            self.connected = False
        return super().disable()

    def run(self):
        if not self.connected:
            self.connected = True
            og.my_app.clicked.connect(self.on_global_click)
        return 
        
    def on_global_click(self, x, y, button, pressed):
        if self._executor.paused:
            return
        self.log_info(f"状态: {pressed} 按键: {button} value: {button.value}")

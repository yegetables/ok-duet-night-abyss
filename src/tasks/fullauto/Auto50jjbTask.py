from qfluentwidgets import FluentIcon
import time
import win32con

from ok import Logger, TaskDisabledException
from src.tasks.DNAOneTimeTask import DNAOneTimeTask
from src.tasks.CommissionsTask import CommissionsTask, Mission
from src.tasks.BaseCombatTask import BaseCombatTask

from src.tasks.AutoDefence import AutoDefence

logger = Logger.get_logger(__name__)


class Auto50jjbTask(DNAOneTimeTask, CommissionsTask, BaseCombatTask):
    """
    50jjb 1.1版本新地图
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = FluentIcon.FLAG
        self.name = "50jjb"
        self.description = "全自动"
        self.group_name = "全自动"
        self.group_icon = FluentIcon.CAFE

        self.setup_commission_config()
        # substrings_to_remove = ["轮次"]
        # keys_to_delete = [key for key in self.default_config for sub in substrings_to_remove if sub in key]
        # for key in keys_to_delete:
            # self.default_config.pop(key, None)

        self.action_timeout = 10

    def run(self):
        """主运行方法"""
        DNAOneTimeTask.run(self)
        self.move_mouse_to_safe_position(save_current_pos=False)
        self.set_check_monthly_card()
        try:
            _to_do_task = self.get_task_by_class(AutoDefence)
            _to_do_task.config_external_movement(self.walk_to_aim, self.config)
            original_info_set = _to_do_task.info_set
            _to_do_task.info_set = self.info_set
            return _to_do_task.do_run()
        except TaskDisabledException:
            pass
        except Exception as e:
            logger.error("AutoMyDungeonTask error", e)
            raise
        finally:
            if _to_do_task is not self:
                _to_do_task.info_set = original_info_set

    def walk_to_aim(self, delay=0):
        """
        从起点走到目标位置的路径
        """
        logger.info("开始移动到目标位置")
        move_start = time.time()

        try:

            self.send_key_down("lalt")
            self.sleep(delay)

            # 开始向前移动14s
            self.send_key_down("w")
            self.sleep(14)
            self.send_key_up("w")

            # Shift
            # self.send_key(self.get_dodge_key(), down_time=0.35)

            # 18.89s-18.99s: 释放所有移动键 (4.93s后)
            self.sleep(1)
            self.send_key_up("lalt")

            elapsed = time.time() - move_start
            logger.info(f"移动完成，用时 {elapsed:.1f}秒")

        except TaskDisabledException:
            raise
        except Exception as e:
            logger.error("移动过程出错", e)
            raise
        finally:
            # 确保释放所有按键
            self.send_key_up("w")
            self.send_key_up("a")
            self.send_key_up("s")
            self.send_key_up("d")
            self.send_key_up(self.get_dodge_key())
            self.send_key_up("lalt")

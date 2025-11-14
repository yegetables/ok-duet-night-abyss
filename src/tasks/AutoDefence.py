from qfluentwidgets import FluentIcon
import time

from ok import Logger, TaskDisabledException
from src.tasks.DNAOneTimeTask import DNAOneTimeTask
from src.tasks.BaseCombatTask import BaseCombatTask
from src.tasks.CommissionsTask import CommissionsTask, Mission, QuickMoveTask, _default_movement

logger = Logger.get_logger(__name__)

DEFAULT_ACTION_TIMEOUT = 10
DEFAULT_MISSION_TIMEOUT = 30


class AutoDefence(DNAOneTimeTask, CommissionsTask, BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = FluentIcon.FLAG
        self.name = "自动扼守"
        self.description = "半自动"
        self.group_name = "半自动"
        self.group_icon = FluentIcon.VIEW

        self.default_config.update({
            '轮次': 3,
        })

        self.setup_commission_config()

        self.config_description.update({
            "轮次": "打几个轮次",
            "超时时间": "波次超时后将发出提示",
        })

        self.action_timeout = DEFAULT_ACTION_TIMEOUT
        self.quick_move_task = QuickMoveTask(self)
        self.external_movement = _default_movement
        self._external_config = None
        self._merged_config_cache = None

    @property
    def config(self):
        if self.external_movement == _default_movement:
            return super().config
        else:
            if self._merged_config_cache is None:
                self._merged_config_cache = super().config.copy()
            self._merged_config_cache.update(self._external_config)
            return self._merged_config_cache

    def config_external_movement(self, func: callable, config: dict):
        if callable(func):
            self.external_movement = func
        else:
            self.external_movement = _default_movement
        self._merged_config_cache = None
        self._external_config = config

    def run(self):
        DNAOneTimeTask.run(self)
        self.move_mouse_to_safe_position()
        self.set_check_monthly_card()
        self.external_movement = _default_movement
        try:
            return self.do_run()
        except TaskDisabledException:
            pass
        except Exception as e:
            logger.error("AutoDefence error", e)
            raise

    def do_run(self):
        self.init_param()
        self.load_char()

        self.wave_info = {"wave": -1, "wait_next": False, "start_time": 0}

        if self.external_movement is not _default_movement and self.in_team():
            self.open_in_mission_menu()

        while True:
            if self.in_team():
                self.handle_in_mission()

            _status = self.handle_mission_interface(stop_func=self.stop_func)

            if _status == Mission.START:
                self.handle_mission_start()
            elif _status == Mission.STOP:
                self.quit_mission()
                self.init_param()
                self.log_info("任务中止")
            elif _status == Mission.CONTINUE:
                self.wait_until(self.in_team, time_out=DEFAULT_MISSION_TIMEOUT)
                self.log_info("任务继续")
                self.current_wave = -1

            self.sleep(0.1)  # 降低CPU占用率

    def handle_in_mission(self):
        """处理在副本中的逻辑"""
        self.get_wave_info()
        if self.current_wave != -1:
            # 如果是新的波次，重置状态
            if self.current_wave != self.wave_info["wave"]:
                self.wave_info.update({"wave": self.current_wave, "start_time": time.time(), "wait_next": False})
                self.quick_move_task.reset()

            # 检查波次是否超时
            if not self.wave_info["wait_next"] and time.time() - self.wave_info["start_time"] >= self.config.get(
                    "超时时间", 120):
                if self.external_movement is not _default_movement:
                    self.log_info("任务超时")
                    self.open_in_mission_menu()
                else:
                    self.log_info_notify("任务超时")
                    self.soundBeep()
                self.wave_info["wait_next"] = True

            # 如果未超时，则使用技能
            if not self.wave_info["wait_next"]:
                self.skill_time = self.use_skill(self.skill_time)
        else:
            # 如果不在战斗波次中，执行移动任务
            self.quick_move_task.run()

    def handle_mission_start(self):
        """处理任务开始的逻辑"""
        self.wait_until(self.in_team, time_out=DEFAULT_MISSION_TIMEOUT)
        self.sleep(2)
        self.init_param()
        if self.external_movement is not _default_movement:
            self.log_info("任务开始，执行外部移动逻辑")
            self.external_movement()
            self.log_info(f"外部移动执行完毕，等待战斗开始，{DEFAULT_ACTION_TIMEOUT}秒后超时")
            if not self.wait_until(lambda: self.current_wave != -1, post_action=self.get_wave_info,
                                   time_out=DEFAULT_ACTION_TIMEOUT):
                self.log_info("等待战斗开始超时，重开任务")
                self.open_in_mission_menu()
            else:
                self.log_info("战斗开始")
        else:
            self.log_info_notify("任务开始")
            self.soundBeep()

    def init_param(self):
        self.current_round = -1
        self.current_wave = -1
        self.skill_time = 0

    def stop_func(self):
        self.get_round_info()
        n = self.config.get("轮次", 3)
        if n == 1 or self.current_round >= n:
            return True

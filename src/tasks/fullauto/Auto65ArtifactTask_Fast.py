from qfluentwidgets import FluentIcon
import time
import win32con

from ok import Logger, TaskDisabledException
from src.tasks.DNAOneTimeTask import DNAOneTimeTask
from src.tasks.CommissionsTask import CommissionsTask, Mission
from src.tasks.BaseCombatTask import BaseCombatTask

from src.tasks.AutoDefence import AutoDefence

logger = Logger.get_logger(__name__)


class Auto65ArtifactTask_Fast(DNAOneTimeTask, CommissionsTask, BaseCombatTask):
    """
    移动更快的自动30/65级mod，路径参考EMT
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = FluentIcon.FLAG
        self.name = "自动30/50/65级魔之楔本"
        self.description = "全自动-龙猫添加50级魔之楔"
        self.group_name = "全自动"
        self.group_icon = FluentIcon.CAFE

        self.setup_commission_config()
        substrings_to_remove = ["轮次"]
        keys_to_delete = [key for key in self.default_config for sub in substrings_to_remove if sub in key]
        for key in keys_to_delete:
            self.default_config.pop(key, None)

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

    # def do_run(self):
    #     """执行任务的核心逻辑"""
    #     # 加载角色信息
    #     self.load_char()

    #     # 初始化变量
    #     _start_time = 0  # 任务开始时间
    #     _skill_time = 0  # 上次释放技能的时间
    #     _count = 0  # 完成次数计数器

    #     # 如果已经在队伍中，先放弃当前任务
    #     if self.in_team():
    #         self.log_info("检测到已在队伍中，先放弃当前任务")
    #         self.give_up_mission()
    #         self.wait_until(lambda: not self.in_team(), time_out=30, settle_time=1)

    #     # 主循环
    #     while True:
    #         # 在队伍中时的逻辑（战斗中）
    #         if self.in_team():
    #             # 第一次进入队伍时记录开始时间
    #             if _start_time == 0:
    #                 _start_time = time.time()
    #             self.log_info(f"开始第 {_count + 1} 次任务")

    #             # 持续释放技能
    #             _skill_time = self.use_skill(_skill_time)

    #             # 检查是否超时
    #             elapsed = time.time() - _start_time
    #             if elapsed >= self.config.get("超时时间", 180):
    #                 logger.warning(f"任务超时 ({elapsed:.1f}秒)，重新开始...")
    #             self.give_up_mission()
    #             self.wait_until(lambda: not self.in_team(), time_out=30, settle_time=1)
    #                 _start_time = 0  # 重置计时器

    #         # 处理任务界面
    #         _status = self.handle_mission_interface()

    #         if _status == Mission.START:
    #             # 任务完成
    #             elapsed = time.time() - _start_time if _start_time > 0 else 0
    #             _count += 1
    #             self.log_info(
    #                 f"任务完成 [{_count}/{self.config.get("刷几次", 999)}] 用时: {elapsed:.1f}秒"
    #             )

    #             # 检查是否达到目标次数
    #             if _count >= self.config.get("刷几次", 999):
    #             self.log_info(f"已完成全部 {_count} 次任务")
    #             self.soundBeep()
    #                 return

    #             # 等待重新进入队伍
    #             self.wait_until(self.in_team, time_out=30)

    #             # 重置计时器
    #             _start_time = time.time()

    #             # 走到目标位置
    #             try:
    #             self.walk_to_aim()
    #             except TaskDisabledException:
    #                 raise
    #             except Exception as e:
    #                 logger.error(f"移动到目标位置失败: {e}")
    #             self.give_up_mission()
    #             self.wait_until(lambda: not self.in_team(), time_out=30, settle_time=1)
    #                 _start_time = 0
    #             _skill_time = 0
    #         # 短暂休眠
    #         self.sleep(0.2)

    def find_track_point(self, x1, y1, x2, y2) -> bool:
        box = self.box_of_screen_scaled(2560, 1440, 2560 * x1, 1440 * y1, 2560 * x2, 1440 * y2, name="find_track_point",
                                        hcenter=True)
        return super().find_track_point(threshold=0.7, box=box)

    def _path_30_65_mod(self):
        """
        从起点走到目标位置的路径
        路径参考: EMT中的扼守-30or65.json，使用复位
        """
        logger.info("开始移动到目标位置")
        move_start = time.time()

        try:
            # ===== 根据扼守-30or65.json录制的路径 =====

            # 0.52s: 开始向前移动
            self.send_key_down("lalt")

            self.sleep(0.05)
            self.send_key_down("w")

            # 1.11s: 开始冲刺 (0.59s后)
            self.sleep(0.59)
            self.send_key_down(self.get_dodge_key())

            # 1.33s: 向左移动 (0.22s后)
            self.sleep(0.22)
            self.send_key_down("a")

            # 2.41s: 停止前进 (1.08s后)
            self.sleep(0.88)
            self.send_key_up("w")

            # 3.85s: 再次向前 (1.44s后)
            self.sleep(0.44)
            self.send_key_down("w")

            # 3.94s: 停止向左 (0.09s后)
            self.sleep(0.09)
            self.send_key_up("a")

            # 4.84s: 再次向左 (0.90s后)
            self.sleep(0.11)
            self.send_key_down("a")

            # 5.22s-7.82s: Shift连续切换 (可能在调整位置)
            self.sleep(0.38)
            self.send_key_up(self.get_dodge_key())
            self.sleep(0.24)
            self.send_key(self.get_dodge_key(), down_time=0.35)
            self.sleep(0.79)
            self.send_key(self.get_dodge_key(), down_time=0.41)
            self.sleep(0.80)
            self.send_key_down(self.get_dodge_key())

            # 9.09s: 停止前进 (1.27s后)
            self.sleep(0.97)
            self.send_key_up("w")

            # 9.56s: 短暂前进 (0.47s后)
            self.sleep(0.47)
            self.send_key_down("w")

            # 9.91s: 停止前进 (0.35s后)
            self.sleep(0.35)
            self.send_key_up("w")

            # 10.70s: 跳跃 (0.79s后)
            self.sleep(0.98)
            self.send_key("space", down_time=0.09)

            # 12.83s: 短暂后退调整 (2.04s后)
            self.sleep(0.04)
            self.send_key("s", down_time=0.09)

            # 1.11s: 开始冲刺 (0.59s后)
            self.sleep(0.59)
            self.send_key(self.get_dodge_key(), down_time=0.41)

            # 13.32s: 短暂前进调整 (0.40s后)
            self.sleep(0.59)
            self.send_key("w", down_time=0.10)

            # 1.11s: 开始冲刺 (0.59s后)
            self.sleep(0.61)
            self.send_key(self.get_dodge_key(), down_time=0.40)

            # 13.86s: 再次短暂后退 (0.44s后)
            self.sleep(0.64)
            self.send_key("s", down_time=0.10)

            # 1.11s: 开始冲刺 (0.59s后)
            self.sleep(0.62)
            self.send_key(self.get_dodge_key(), down_time=0.37)

            # 13.86s: 再次短暂后退 (0.44s后)
            self.sleep(0.66)
            self.send_key("s", down_time=0.10)

            # 1.11s: 开始冲刺 (0.59s后)
            self.sleep(0.58)
            self.send_key(self.get_dodge_key(), down_time=0.39)

            # 18.89s-18.99s: 释放所有移动键 (4.93s后)
            self.sleep(0.29)
            self.send_key_up(self.get_dodge_key())
            self.sleep(0.10)
            self.send_key_up("a")

            self.send_key_up("lalt")
            # 19.97s: 复位并传送到目标位置
            if not self.reset_and_transport():
                raise Exception("复位失败")

            # 回身
            self.sleep(0.44)
            self.send_key("s", down_time=0.09)

            # 重置视角
            self.sleep(0.48)
            self.send_forward_key()

            # ===== 路径编写结束 =====

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
    
    def _release_all_move_keys(self):
        """释放所有移动相关按键，防止卡键"""
        keys = ["w", "a", "s", "d", "lalt", self.get_dodge_key()]
        for k in keys:
            self.send_key_up(k)

    def _path_50_center(self):
        self.send_key_down("lalt")
        self.sleep(0.05)
        self.send_key_down("w")
        self.sleep(0.1)
        self.send_key(self.get_dodge_key(), down_time=0.8)
        self.sleep(0.3)
        self.send_key(self.get_dodge_key(), down_time=0.3)
        self.sleep(0.3)
        self.send_key(self.get_dodge_key(), down_time=0.2)
        self.sleep(0.2)
        self.send_key_down("d")
        self.sleep(0.7)
        self.send_key_up("w")
        self.sleep(0.7)
        self.send_key("w", down_time=0.6)
        self.sleep(0.5)
        self.send_key(self.get_dodge_key(), down_time=0.2)
        self.sleep(0.4)
        self.send_key("s", down_time=0.7)
        self.sleep(0.8)
        self.send_key(self.get_dodge_key(), down_time=0.2)
        self.sleep(0.3)
        self.send_key("w", down_time=1.1)
        self.sleep(1.1)
        self.send_key(self.get_dodge_key(), down_time=0.2)
        self.sleep(0.7)
        self.send_key("w", down_time=0.4)
        self.sleep(0.6)
        self.send_key(self.get_dodge_key(), down_time=0.3)
        self.sleep(1.3)
        self.send_key("w", down_time=0.7)
        self.sleep(0.4)
        self.send_key(self.get_dodge_key(), down_time=0.5)
        self.sleep(0.4)
        self.send_key(self.get_dodge_key(), down_time=0.2)
        self.sleep(0.3)
        self.send_key_up("d")

        self.send_forward_key()

        self._release_all_move_keys()


    def _path_50_up(self):
        self.send_key_down("lalt")
        self.sleep(0.05)
        self.send_key_down("w")
        self.sleep(0.1)
        self.send_key(self.get_dodge_key(), down_time=0.7)
        self.sleep(0.7)
        self.send_key(self.get_dodge_key(), down_time=0.3)
        self.sleep(0.9)
        self.send_key_down("space")
        self.sleep(0.1)
        self.send_key_up("space")
        self.sleep(0.3)
        self.send_key_down("space")
        self.sleep(0.1)
        self.send_key_up("space")
        self.sleep(0.3)
        self.send_key_down(self.get_dodge_key())
        self.sleep(0.5)
        self.send_key_down("d")
        self.sleep(0.05)
        self.send_key_up("w")
        self.sleep(0.5)
        self.send_key(self.get_dodge_key(), down_time=0.3)
        self.sleep(0.2)
        self.send_key_up("d")
        self.send_key_down("w")
        self.sleep(0.9)
        self.send_key_down("a")
        self.sleep(0.5)
        self.send_key(self.get_dodge_key(), down_time=0.3)
        self.sleep(1.8)
        self.send_key_up("a")
        self.sleep(1.2)
        if self.find_track_point(0.46, 0.33, 0.49, 0.38):
            # 检测蛇房
            self.sleep(1.2)
            self.send_key_down("d")
            self.sleep(0.2)
            self.send_key(self.get_dodge_key(), down_time=0.3)
            self.sleep(0.1)
            self.send_key_up("d")
            self.sleep(0.2)
            self.send_key("a", down_time=0.06)
            self.sleep(0.4)
            self.send_key(self.get_dodge_key(), down_time=0.5)
            self.sleep(0.6)
            self.send_key("a", down_time=1.1)
            self.sleep(0.1)
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(1.7)
            self.send_key(self.get_dodge_key(), down_time=0.8)
            self.sleep(0.7)
            self.send_key("a", down_time=0.4)
            self.sleep(1.1)
            self.send_key(self.get_dodge_key(), down_time=0.5)
            self.sleep(0.5)
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(0.4)
            self.send_key_up("w")
        else:
            # 检测空房
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(0.9)
            self.send_key(self.get_dodge_key(), down_time=0.5)
            self.sleep(2.1)
            self.send_key(self.get_dodge_key(), down_time=0.3)
            self.sleep(0.7)
            self.send_key("a", down_time=0.4)
            self.sleep(1.1)
            self.send_key(self.get_dodge_key(), down_time=0.3)
            self.sleep(0.7)
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(0.5)
            self.send_key_up("w")

        self._release_all_move_keys()


    def _path_50_down(self):
        self.send_key_down("lalt")
        self.sleep(0.05)
        self.send_key_down("w")
        self.sleep(0.1)
        self.send_key(self.get_dodge_key(), down_time=0.7)
        self.sleep(0.5)
        self.send_key(self.get_dodge_key(), down_time=0.5)
        self.sleep(0.1)
        if self.find_track_point(0.48, 0.33, 0.51, 0.38):
            # 检测蛇房
            self.sleep(1.0)
            self.send_key_down("d")
            self.sleep(0.2)
            self.send_key(self.get_dodge_key(), down_time=0.3)
            self.sleep(0.3)
            self.send_key_up("d")
            self.sleep(0.6)
            self.send_key(self.get_dodge_key(), down_time=0.5)
            self.sleep(0.6)
            self.send_key("a", down_time=1.1)
            self.sleep(0.1)
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(1.9)
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(0.3)
            self.send_key("d", down_time=0.1)
            self.sleep(2.1)
            self.send_key(self.get_dodge_key(), down_time=0.3)
            self.sleep(0.6)
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(0.4)
            self.send_key_up("w")
        else:
            # 检测空房
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(0.9)
            self.send_key(self.get_dodge_key(), down_time=0.5)
            self.sleep(2.1)
            self.send_key(self.get_dodge_key(), down_time=0.3)
            self.sleep(0.7)
            self.send_key("a", down_time=0.4)
            self.sleep(1.1)
            self.send_key(self.get_dodge_key(), down_time=0.3)
            self.sleep(0.7)
            self.send_key(self.get_dodge_key(), down_time=0.2)
            self.sleep(0.5)
            self.send_key_up("w")

        self._release_all_move_keys()


    def walk_to_aim(self, delay=0):
        """
        主寻路函数：根据识别到的坐标选择路径
        """
        try:
            self.send_key_down("lalt")
            self.sleep(delay)

            # 使用 if-elif 结构，优先级清晰，且只执行一个分支
            if self.find_track_point(0.19, 0.54, 0.23, 0.59):
                # 分支1：30/65默认
                self._path_30_65_mod()
                
            elif self.find_track_point(0.74, 0.60, 0.77, 0.64):
                # 分支2：50中平台
                self._path_50_center()
                
            elif self.find_track_point(0.45, 0.26, 0.49, 0.31):
                # 分支3：50上神像
                self._path_50_up()
                
            elif self.find_track_point(0.48, 0.28, 0.51, 0.32):
                # 分支4：50下黑房
                self._path_50_down()
            else:
                self.log_debug("not found any track point,default exec 30_65mod path")
                self._path_30_65_mod()
                
        except Exception as e:
            logger.error("Error in walk_to_aim", e)
            # 可以在这里添加日志记录
        finally:
            self._release_all_move_keys()

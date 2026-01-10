from qfluentwidgets import FluentIcon
import time
import random

from ok import Logger, TaskDisabledException
import re
from src.tasks.DNAOneTimeTask import DNAOneTimeTask
from src.tasks.BaseCombatTask import BaseCombatTask
from src.tasks.CommissionsTask import CommissionsTask, Mission, QuickAssistTask

logger = Logger.get_logger(__name__)

MOUSE_VAL_TO_PIXELS = 10



class AutoExpulsion_Custom(DNAOneTimeTask, CommissionsTask, BaseCombatTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = FluentIcon.FLAG
        self.name = "自动通用 + 自定义指令（单图/无地图识别）"
        self.description = "全自动"
        self.group_name = "全自动"
        self.group_icon = FluentIcon.CAFE

        self.setup_commission_config()

        self.default_config.update({
            "快速继续挑战": True,
            "关闭抖动": False,
            "关闭抖动锁定在窗口范围": False,
            "随机游走": False,
            "随机游走幅度": 1.0,
            "挂机模式": "开局重置角色位置",
            "执行自定义指令": False,
            "自定义指令": "q#1.5 W30 L0.3#0.3L0.3#0.3L0.3#0.3\nS30D26 L0.3#0.3L0.3#0.3\n#2W12 L0.3#0.3L0.3#0.3\nS6A3 L0.3#0.3L0.3#0.3\nD12 L0.3#0.3L0.3#0.3 #3",
            "自定义指令工具": "" 
                + "前进5秒: w5\n" 
                + "前冲5秒: w>5\n" 
                + "飞枪(枯朽+10迅捷): L0.3#0.3\n\n" 
                + "夜航手册60驱逐（永恒 / 黎瑟飞枪 枯朽+10迅捷）: 挂机模式 - 原地待机\nq#1.5 W30 L0.3#0.3L0.3#0.3L0.3#0.3\nS30D26 L0.3#0.3L0.3#0.3\n#2W12 L0.3#0.3L0.3#0.3\nS6A3 L0.3#0.3L0.3#0.3\nD12 L0.3#0.3L0.3#0.3 #3\n\n" 
                + "自动扼守50（JJB）: 挂机模式 - 原地待机\nw>7.1\n\n" 
                + "自动扼守50（JJB）飞枪: 挂机模式 - 原地待机\nwa>1L0.3#0.3L0.3#0.3L0.3#0.3L0.3#2.2\n",
            "自定义指令随机波动": False,
        })
        self.config_description.update({
            "快速继续挑战": "R键快速继续挑战，跳过结算动画。",
            "随机游走": "是否在任务中随机移动",
            "随机游走幅度": "单次走动最大持续时间（秒）",
            "挂机模式": "开局重置角色位置 / 原地待机",
            "执行自定义指令": "处理完挂机模式指令后执行 \n"
                + "注: 处理正则表达式时忽略空格和回车 \n" 
                + "例: w4.6 _ #2 _ wa>2 d>1 #3 < #3 @ \n" 
                + "或: w4.6_#2_wa>2d>1#3<#3@ ", 
            "自定义指令":  ""
                + "任意小写字母: 对应按键\n"
                + "移动: w a s d wa ws sa sd \n" 
                + "鼠标点击: L R \n"
                + "鼠标移动: W A S D (50 := 90°) \n"
                + "螺旋飞跃: @ \n" 
                + "跳跃: _ \n" 
                + "前冲: [wasd]{1,2}> \n" 
                + "后冲: < \n" 
                + "交互: + \n"
                + "等待: # \n" 
                + "\t\t\t\t",
            "自定义指令工具": "记事本 / 剪切板 \n"
                +"可用于记录自定义指令 \n" 
                + "\t\t\t\t",
            "自定义指令随机波动": "每次移动持续时间随机 -/+ 0.0% ~ 7.5%",
        })
        self.config_type["挂机模式"] = {
            "type": "drop_down",
            "options": ["开局重置角色位置", "原地待机"],
        }

        self.action_timeout = 10
        
        self.skill_tick = self.create_skill_ticker()
        self.random_walk_tick = self.create_random_walk_ticker()

    def run(self):
        if self.config.get("关闭抖动", False):
            mouse_jitter_setting = self.afk_config.get("鼠标抖动")
            self.afk_config.update({"鼠标抖动": False}) 
        if self.config.get("关闭抖动锁定在窗口范围", False):
            mouse_jitter_lock_setting = self.afk_config.get("鼠标抖动锁定在窗口范围")
            self.afk_config.update({"鼠标抖动锁定在窗口范围": False}) 
        DNAOneTimeTask.run(self)
        self.move_mouse_to_safe_position(save_current_pos=False)
        self.set_check_monthly_card()
        try:
            return self.do_run()
        except TaskDisabledException:
            pass
        except Exception as e:
            logger.error("AutoExpulsion error", e)
            raise
        finally:
            if self.config.get('关闭抖动', False):
                self.afk_config.update({"鼠标抖动": mouse_jitter_setting})
                self.afk_config.update({"鼠标抖动锁定在窗口范围": mouse_jitter_lock_setting})
                try:
                    self.release_all_move_keys()
                except Exception as e:
                    logger.error("AutoExpulsion key release error", e)
                    raise
    
    def release_all_move_keys(self):
        """释放所有移动相关按键，防止卡键"""
        keys = ['w', 'a', 's', 'd', 'lalt', 
                self.get_dodge_key(), 
                self.get_spiral_dive_key(), 
                self.get_interact_key(), 
            ]
        for k in keys:
            self.send_key_up(k)

    def do_run(self):
        self.count = 0
        self.runtime_state = {}
        self.custom_actions = []
        self.init_all()
        self.load_char()
        while True:
            if self.in_team():
                self.handle_in_mission()
            elif (self.config.get("快速继续挑战", False) 
                and self.current_round ==0
                and not self.wait_until(lambda: self.in_team(), time_out=0.3)
            ):
                self.send_key(key="r", down_time=0.050)

            _status = self.handle_mission_interface(stop_func=self.stop_func)
            if _status == Mission.START:
                self.wait_until(self.in_team, time_out=30)
                self.init_all()
                self.handle_mission_start()
            elif _status == Mission.STOP:
                self.log_info("任务中止")
                self.quit_mission()
            elif _status == Mission.CONTINUE:
                self.log_info("任务继续")
                self.init_for_next_round()
                self.wait_until(self.in_team, time_out=self.action_timeout)

            self.sleep(0.1)

    def init_all(self):
        self.init_for_next_round()
        self.skill_tick.reset()
        self.current_round = 0

    def init_for_next_round(self):
        self.init_runtime_state()

    def init_runtime_state(self):
        self.info_set("完成轮次", self.count)
        self.get_round_info()
        self.info_set("当前轮次", self.current_round)
        self.reset_wave_info()
        self.info_set("上轮耗时", f"{(time.time() - self.runtime_state.get("round_time", time.time())):.1f}秒")
        self.runtime_state = {"start_time": 0, "round_time": time.time(),
                              "wave_start_time": 0, "wave": -1, "wait_next_wave": False}
        self.random_walk_tick.reset()

    def handle_in_mission(self):
        if self.runtime_state["start_time"] == 0:
            self.runtime_state["start_time"] = time.time()
            self.count += 1
        
        self.get_wave_info()
        if self.current_wave != -1:
            # 如果是新的波次，重置状态
            if self.current_wave != self.runtime_state["wave"]:
                self.runtime_state.update(
                    {"wave": self.current_wave, "wave_start_time": time.time(), "wait_next_wave": False})
                
            if not self.runtime_state["wait_next_wave"] and time.time() - self.runtime_state[
                "wave_start_time"] >= self.config.get("超时时间", 120):
                self.log_info("任务超时")
                self.give_up_mission()
                return

        elif time.time() - self.runtime_state["start_time"] >= self.config.get("超时时间", 120):
            logger.info("已经超时，重开任务...")
            self.give_up_mission()
            return

        self.random_walk_tick()
        self.skill_tick()

    def handle_mission_start(self):
        self.sleep(2)
        self.log_info("任务开始")
        self.move_on_begin()
        self.skill_tick()
    
    def stop_func(self):
        pass

    def move_on_begin(self):
        if self.config.get("挂机模式") == "开局重置角色位置":
            # 复位方案
            self.reset_and_transport()
            # 防卡墙
            self.send_key("w", down_time=0.5)
        if self.config.get("执行自定义指令"):
            # 执行自定义指令序列
            self.parse_custom_actions()
            self.execute_custom_actions()
        else:
            self.sleep(2)

    def parse_custom_actions(self):
        """Parse the custom command string from config into self.custom_actions."""
        self.custom_actions = []
        cmd = str(self.config.get("自定义指令", "")).strip()
        if not cmd:
            return

        # regex to match tokens like 'wa1.2', 'w 1.2', '#1.5', '>', '<', '_', '@', '+' or any 1-2 letter key
        token_re = re.compile(r"(#\d+(?:\.\d+)?)|([A-Za-z]{1,2}+(?:>)?\d*(?:\.\d+)?)|(<|_|@|\+)")

        for m in token_re.finditer(cmd.replace(' ', '')):
            t = m.group(0)
            if not t:
                continue
            if t.startswith('#'):
                # wait
                try:
                    dur = float(t[1:])
                except Exception:
                    dur = 1.000
                self.custom_actions.append({'type': 'wait', 'dur': dur})
            elif t == '<':
                self.custom_actions.append({'type': 'dodge', 'dur': 0})
            elif t == '_':
                self.custom_actions.append({'type': 'key', 'key': 'space', 'dur': 0.050})
            elif t == '@':
                self.custom_actions.append({'type': 'key', 'key': self.get_spiral_dive_key(), 'dur': 0.050})
            elif t == '+':
                self.custom_actions.append({'type': 'key', 'key': self.get_interact_key(), 'dur': 0.050})
            else:
                # movement like w,wa,w1.2,ws1.2
                m2 = re.match(r'([A-Za-z]{1,2}+(?:>)?)(\d*(?:\.\d+)?)', t)
                if m2:
                    key_raw = m2.group(1)
                    num = m2.group(2)
                    val = float(num) if num else 1.000
                    if key_raw == 'L':
                        self.custom_actions.append({'type': 'mouse', 'key': 'left', 'dur': val})
                    elif key_raw == 'R':
                        self.custom_actions.append({'type': 'mouse', 'key': 'right', 'dur': val})
                    elif key_raw == 'A':
                        self.custom_actions.append({'type': 'move', 'direction': 'X', 'angel': -val})
                    elif key_raw == 'D':
                        self.custom_actions.append({'type': 'move', 'direction': 'X', 'angel': val})
                    elif key_raw == 'W':
                        self.custom_actions.append({'type': 'move', 'direction': 'Y', 'angel': -val})
                    elif key_raw == 'S':
                        self.custom_actions.append({'type': 'move', 'direction': 'Y', 'angel': val})
                    else:
                        # normalize to lower-case for keyboard keys
                        self.custom_actions.append({'type': 'key', 'key': key_raw.lower(), 'dur': val})

    def execute_custom_actions(self):
        """Execute the parsed custom actions sequentially."""
        if not self.custom_actions:
            return
        for act in self.custom_actions:
            if act['type'] == 'wait':
                self.sleep(act['dur'])
            elif act['type'] == 'dodge':
                self.send_key(self.get_dodge_key(), down_time=0.05)
            elif act['type'] == 'mouse':
                key = act.get('key', 'left')
                dur = act.get('dur', 0.05)
                self.mouse_down(key=key)
                self.sleep(dur)
                self.mouse_up(key=key)
            elif act['type'] == 'move':
                # move mouse relative by 'angel' pixels on X or Y axis
                ang = int(act.get('angel', 0))
                if act.get('direction') == 'X':
                    self.move_mouse_relative(ang * MOUSE_VAL_TO_PIXELS, 0)
                else:
                    self.move_mouse_relative(0, ang * MOUSE_VAL_TO_PIXELS)
            elif act['type'] == 'key':
                dur = act.get('dur', 0.5)
                if self.config.get("自定义指令随机波动", False):
                    dur = dur * random.uniform(1 - 0.075, 1 + 0.075)
                dash = act['key'][-1] == '>'
                if dash:
                    act['key'] = act['key'][:-1]
                if len(act['key']) == 1:
                    self.log_debug(act['key'])
                    self.log_debug(dur)
                    self.send_key_down(act['key'])
                    if dash:
                        self.sleep(0.050)
                        self.send_key(self.get_dodge_key(), down_time=dur)
                    else:
                        self.sleep(dur)
                    self.send_key_up(act['key'])
                elif len(act['key']) == 2:
                    self.send_key_down(act['key'][0])
                    self.send_key_down(act['key'][1])
                    if dash:
                        self.sleep(0.050)
                        self.send_key(self.get_dodge_key(), down_time=dur)
                    else:
                        self.sleep(dur)
                    self.send_key_up(act['key'][0])
                    self.send_key_up(act['key'][1])
                elif act['key']:
                    try:
                        self.send_key(act['key'], down_time=dur)
                    except Exception:
                        pass

    def create_random_walk_ticker(self):
        """创建一个随机游走的计时器函数。"""
        def action():
            if not self.config.get("随机游走", False):
                return
            duration = random.uniform(0, 1) * self.config.get("随机游走幅度", 1.0)
            direction = random.choice(["w", "a", "s", "d"])
            self.send_key(direction, down_time=duration)

        return self.create_ticker(action, interval=5, interval_random_range=(0.8, 2))

    def stop_func(self):
        self.get_round_info()
        n = self.config.get("轮次", 3)
        if self.current_round >= n:
            return True

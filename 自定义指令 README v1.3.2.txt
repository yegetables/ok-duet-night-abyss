自定义指令 v1.3.2 for OK-DNA v1.1.14

OK-DNA 根目录替换以下文件夹 (OK-DNA -> 截图方式 -> 安装目录)
\src
\mod

###使用/编辑鼠标移动指令时 请在 OK-DNA 设置里配置游戏内灵敏度以便分享###

自定义指令范例

    基础指令
        等待:       #
            例:     #2          - 等待2秒
            例:     #2.2        - 等待2.2秒
        交互:       +
            例:     +#1         - 交互后等待1秒
        跳跃:       _
            例:     _#2         - 跳跃后等待2秒
        移动:       w a s d wa ws sa sd
            例:     w3          - 前进3秒
            例:     wa3         - 向左前移动3秒
        移动冲刺:   [wasd]{1,2}>
            例:     w>4.6       - 向前疾跑4.6秒
            例:     wa>4.6      - 向左前疾跑4.6秒
        鼠标点击:   L R
            L       - 鼠标左键
            R       - 鼠标右键
            例:     L0.3#0.4    - 飞枪 按住左键0.3秒后松开0.4秒    
        鼠标移动:   W A S D
            W - 上  S - 下
            A - 左  D - 右
            例:     W20         - 鼠标向上移20
            例:     A30         - 鼠标向左移20
            注:     50 约等于 90度 
        闪避后跳:   <
        螺旋飞跃:   @
        重置位置:   !

    特殊指令
        停止脚本:   STOP         - 结束循环
        退出副本:   EXIT         - 换图
        跳过指令:   SKIP         - 跳过剩余自定义指令
        开启技能:   TICK         - 调用全局技能
        识图参数:   REFW         - 设置识图参照分辨率 宽    默认: 1920
        识图参数:   REFH         - 设置识图参照分辨率 高    默认: 1080
            注:         分辨率为默认 1920x1080 时 无需设置参数
            例:         REFW1600 REFH900                        设置识图参照分辨率为 1600x900

    函数指令
        轮数检测:   :R[round_num]([command], [opt:command_false])
            例:     :R46(STOP) - 累计运行46轮后停止运行
        图片识别:   :M[img_folder][img_name]([command], [opt:command_false])
            注:         图片格式必须为 .png 必须以字母结尾 推荐命名 A.png B.png C.png
            注:         [img_folder] 图片文件夹必须存放于 \mod\CustomCommand\img
            注:         [img_name] 只识别单字母 如 A B C
            例:         :MMapExpulsionSewerA(!wa>1.4w>1, wa>1w>1.4)
                            [img_folder] 图片文件夹 - \mod\CustomCommand\img\MapExpulsionSewer
                            [img_name] 图片名字 - A              对应图片文件 - A.png
                            [command] - !wa>1.4w>1              识别到图 A 时执行
                            [opt:command_false] - wa>1w>1.4     未识别到图 A 时执行
            例:         :MMapExpulsionMineA(! SKIP)             识别到图 A 时执行 ! SKIP
                        :MMapExpulsionMineB(wd>3 SKIP)          识别到图 B 时执行 wd>3 SKIP
                        :MMapExpulsionMineC(w>2.2a>1 SKIP)      识别到图 C 时执行 w>2.2a>1 SKIP
        注释:       ::([comment])
    
    其他指令: 
        任意小写字母: 对应按键



CHANGELOG
v1.3.2
    大全 新增 委托50/70避险 [黎瑟 + 飞枪 1.75]
    大全 优化 委托10/30/40探险 平地位置
v1.3.1
    大全 优化 委托10/30/40探险
    大全 优化 委托20/50探险(锅炉房) 委托70/80调停
v1.3.0
    大全 新增 委托10/30/40探险 [黎瑟/赛琪 + 飞枪 1.75]
    更新UI 自定义指令 + 外部移动逻辑 分类变更 全自动 -> ADD-ONS
    更新地图/图片识别分辨率适配 默认分辨率 1920x1080
    添加新的指令    
        识图参数:   REFW         - 设置识图参照分辨率 宽    默认: 1920
        识图参数:   REFH         - 设置识图参照分辨率 高    默认: 1080
            注:         分辨率为默认 1920x1080 时 无需设置参数
            例:         REFW1600 REFH900                        设置识图参照分辨率为 1600x900
v1.2.2
    大全 新增 夜航手册50扼守 委托80扼守 委托20/50探险(锅炉房) 委托70/80调停
    修复 Unexpected None
v1.2.1
    修复 Unexpected None
v1.2.0
    更新地图/图片识别
    添加新的指令
        重置位置:   !
        停止脚本:   STOP - 结束循环
        退出副本:   EXIT - 换图
        跳过指令:   SKIP - 跳过剩余自定义指令
        开启技能:   TICK - 调用全局技能
        轮数检测:   :R[round_num]([command], [opt:command_false])
            例:     :R46(STOP) - 累计运行46轮后停止运行
        图片识别:   :M[img_folder][img_name]([command], [opt:command_false])
            注:         图片格式必须为 .png 必须以字母结尾 推荐命名 A.png B.png C.png
            注:         [img_folder] 图片文件夹必须存放于 \mod\CustomCommand\img
            注:         [img_name] 只识别单字母 如 A B C
            例:         :MMapExpulsionSewerA(!wa>1.4w>1, wa>1w>1.4)
                            [img_folder] 图片文件夹 - \mod\CustomCommand\img\MapExpulsionSewer
                            [img_name] 图片名字 - A              对应图片文件 - A.png
                            [command] - !wa>1.4w>1              识别到图 A 时执行
                            [opt:command_false] - wa>1w>1.4     未识别到图 A 时执行
            例:         :MMapExpulsionMineA(! SKIP)             识别到图 A 时执行 ! SKIP
                        :MMapExpulsionMineB(wd>3 SKIP)          识别到图 B 时执行 wd>3 SKIP
                        :MMapExpulsionMineC(w>2.2a>1 SKIP)      识别到图 C 时执行 w>2.2a>1 SKIP
        注释:       ::([comment])
    更改代码挂载方式
        添加文件 - \src\tasks\fullauto\CustomCommandTask.py
        修改文件 - \src\config.py
    添加素材 - \mod\CustomCommand\img
        探险出生地图 - MapExploration...
        驱离出生地图 - MapExpulsion...
    附带原版自动驱离文件 - \src\tasks\AutoExpulsion.py
        还原覆盖文件
    附带外部逻辑覆盖文件 - \src\tasks\fullauto\ImportTask.py
        添加快速重新挑战
v1.1.0
    修复技能释放
    修复波次超时
v1.0.0
    自定义指令初版

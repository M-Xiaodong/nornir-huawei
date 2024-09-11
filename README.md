# nornir管理华为交换机
**使用组或者IP地址筛选设备**   

**使用预定义、自定义、文件中获取命令后对设备执行命令**   

**效果如下：**
---
```
D:\python main.py
请选择筛选方式：
1. 按设备组筛选
2. 按IP地址筛选
q. 退出程序
请输入选择 (1/2/q): 1
可用的设备组:
1. BJ
2. SH
3. SZ

请选择设备组 (输入数字): 1
╭──────────────────╮
│ 已选择 2 台设备: │
╰──────────────────╯
  • BJ-office-104 (192.168.1.104)
  • BJ-office-103 (192.168.1.103)
可用的预定义命令：
1. display version
2. display current-configuration
3. display ip interface brief
b. 备份配置
c. 自定义命令
f. 从文件执行多行配置
s. 保存配置
q. 退出
请选择命令编号: 1
正在连接设备 BJ-office-104 并执行任务: netmiko_send_command
正在连接设备 BJ-office-103 并执行任务: netmiko_send_command
⠇ 执行中... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  50% 1/2 0:00:07
vvvv BJ-office-103: netmiko_send_command ** changed : False vvvvvvvvvvvvvvvvvvvv INFO
Huawei Versatile Routing Platform Software
VRP (R) software, Version 5.170 (S5720 V200R019C10SPC500)
Copyright (C) 2000-2020 HUAWEI TECH Co., Ltd.
HUAWEI S5720S-52X-LI-AC Routing Switch uptime is 66 weeks, 5 days, 8 hours, 8 minutes

ES5D2T52S006 0(Master)  : uptime is 66 weeks, 5 days, 8 hours, 6 minutes
DDR             Memory Size : 512   M bytes
FLASH Total     Memory Size : 512   M bytes
FLASH Available Memory Size : 238   M bytes
Pcb           Version   : VER.B
BootROM       Version   : 0213.0000
BootLoad      Version   : 0213.0000
CPLD          Version   : 0106
Software      Version   : VRP (R) Software, Version 5.170 (V200R019C10SPC500)
FLASH         Version   : 0000.0000
^^^^ END netmiko_send_command ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  执行中... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 2/2 0:00:07
╭─ 执行结果汇总 ─╮
│ 设备总数: 2    │
│ 成功设备数: 1  │
│ 失败设备数: 1  │
╰────────────────╯
╔═══════════════╤══════════════╤══════╗
║ 成功设备名称  │ IP地址       │ 状态 ║
╟───────────────┼──────────────┼──────╢
║ BJ-office-103 │ 192.168.1.103 │ ✅   ║
╚═══════════════╧══════════════╧══════╝
╔═══════════════╤══════════════╤════════════════════════╗
║ 失败设备名称  │ IP地址       │ 失败原因               ║
╟───────────────┼──────────────┼────────────────────────╢
║ BJ-office-104 │ 192.168.1.104 │ Authentication failed. ║
╚═══════════════╧══════════════╧════════════════════════╝
是否保存所有成功执行的设备配置？(y/n): n
是否继续操作其他设备？(y/n): n
```

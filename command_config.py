from nornir_utils.plugins.functions import print_result
# 预定义的命令列表
PREDEFINED_COMMANDS = {
    '1': 'display version',
    '2': 'display current-configuration',
    '3': 'display ip interface brief',
}
# TFTP服务器地址
TFTP_SERVER = "10.88.11.119"  # 请根据实际情况修改这个地址

def get_command_choice():
    """获取用户的命令选择"""
    print("可用的预定义命令：")
    for key, cmd in PREDEFINED_COMMANDS.items():
        print(f"{key}. {cmd}")
    print("b. 备份配置")
    print("c. 自定义命令")
    print("f. 从文件执行多行配置")
    print("s. 保存配置")
    print("q. 退出")
    return input("请选择命令编号: ").strip().lower()

def get_command(choice, device_name=None):
    """根据用户选择返回相应的命令"""
    if choice == 'q':
        return 'q'
    elif choice == 'c':
        return input("请输入自定义命令: ").strip().lower()
    elif choice == 'b':
        return f"tftp {TFTP_SERVER} put vrpcfg.zip {device_name}.zip"
    elif choice == 's':
        return "SAVE_CONFIG"
    elif choice == 'f':
        return "FILE_COMMANDS"
    elif choice in PREDEFINED_COMMANDS:
        return PREDEFINED_COMMANDS[choice]
    else:
        print("无效的选择，请重新输入。")
        return None
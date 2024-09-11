from nornir import InitNornir
from nornir_netmiko import netmiko_send_command,netmiko_send_config,netmiko_save_config
from nornir_utils.plugins.functions import print_result
import paramiko
import logging

# 禁用日志以避免显示多余的日志信息
logging.disable(logging.CRITICAL)


# 设置安全加密选项
paramiko.Transport._preferred_kex = ['diffie-hellman-group-exchange-sha256', 'diffie-hellman-group14-sha1']
paramiko.Transport._preferred_ciphers = ['aes128-ctr','aes256-ctr']
paramiko.Transport._preferred_keys = ['ecdsa-sha2-nistp256','ssh-rsa']


def execute_on_device(nr, device_name, task, **kwargs):
    """在指定设备上执行任务"""
    # 筛选指定的设备
    target_device = nr.filter(name=device_name)
    if not target_device.inventory.hosts:
        print(f"错误：未找到名为 {device_name} 的设备")
        return
    print(f"正在连接设备 {device_name} 并执行任务: {task.__name__}")
    # 执行任务
    results = target_device.run(task=task, **kwargs)
    # 结果处理：根据设备成功与否输出对应信息
    for host, result in results.items():
        if result.failed:
            # 捕获异常并转换为字符串
            exception_str = str(result.exception)
            # 分割错误信息并输出最后一行
            error_lines = exception_str.split('\n')
            return f"Host {host} 错误信息 : {error_lines[-1]}"
            # print(f"Host {host}: 错误信息 : {error_lines[-1]}")
        else:
            # 成功时显示完整回显
            return result
            # print_result(result)
    return None



def send_command(nr, device_name, command):
    """连接到设备并执行命令"""
    return execute_on_device(nr, device_name, netmiko_send_command, command_string=command)

def save_config(nr, device_name):
    """保存设备配置"""
    return execute_on_device(nr, device_name, 
                      netmiko_save_config, 
                      cmd="save", 
                      confirm=True, 
                      confirm_response="y")

def commands_from_file(nr, device_name, filename):
    """从文件读取命令并执行"""
    try:
        with open(filename, 'r') as file:
            commands = [line.strip() for line in file if line.strip()]  # 去除空行
        if not commands:
            print(f"警告：文件 '{filename}' 中没有有效的命令。")
            return
    except Exception as e:
        print(f"读取文件时发生错误: {str(e)}")
        return
    return execute_on_device(nr, device_name, 
                      netmiko_send_config, 
                      config_commands=commands, 
                      enter_config_mode=True, 
                      exit_config_mode=True)

# 使用示例
if __name__ == "__main__":
    # 初始化Nornir（确保您有正确的配置文件）
    nr = InitNornir(config_file="config.yaml")
    # 假设您已经使用select_device模块选择了设备
    selected_device = "example_device"  # 这应该是从select_device模块获得的
    command_to_execute = "display version"
    result = send_command(nr, selected_device, command_to_execute)
    print(f"执行结果: {result}")
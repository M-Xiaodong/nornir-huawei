from nornir import InitNornir
from nornir.core.filter import F
def select_group(nr):
    """ 获取所有可用的设备组并让用户选择一个，排除 Huawei 组 """
    available_groups = sorted(group for group in nr.inventory.groups.keys() if group != "Huawei")
    print("可用的设备组:")
    for index, group in enumerate(available_groups, start=1):
        print(f"{index}. {group}")
    while True:
        try:
            choice = int(input("\n请选择设备组 (输入数字): ")) - 1
            if 0 <= choice < len(available_groups):
                return available_groups[choice]
            else:
                print("无效的选择，请重试。")
        except ValueError:
            print("请输入有效的数字。")

def select_device_by_ip(nr):
    """ 让用户输入IP地址来选择设备 """
    available_devices = {host.hostname: name for name, host in nr.inventory.hosts.items()}
    while True:
        ip_address = input("请输入设备IP地址: ").strip()
        if ip_address in available_devices:
            return available_devices[ip_address]
        else:
            print("无效的IP地址,请重试。")

def select_devices(nr):
    """允许用户选择使用设备组或特定IP,或退出程序"""
    while True:
        print("请选择筛选方式：")
        print("1. 按设备组筛选")
        print("2. 按IP地址筛选")
        print("q. 退出程序")
        choice = input("请输入选择 (1/2/q): ").strip().lower()
        if choice in ['q', 'quit', 'exit']:
            print("正在退出程序...")
            return None  # 返回 None 表示用户选择退出
        if choice == '1':
            group = select_group(nr)
            if group:
                return nr.filter(F(groups__contains=group))
        elif choice == '2':
            ip_address = select_device_by_ip(nr)
            if ip_address:
                return nr.filter(F(hostname=ip_address) | F(name=ip_address))
        else:
            print("无效的选择")
        return nr.filter(name="")  # 返回空的设备集合


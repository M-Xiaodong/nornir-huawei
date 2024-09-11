from nornir import InitNornir
from select_device import select_devices
from device_connector import send_command, save_config, commands_from_file
from command_config import get_command_choice, get_command
from nornir_utils.plugins.functions import print_result
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich import box
import io
import sys

def main():
    nr = InitNornir(config_file="config.yaml")
    console = Console()
    while True:
        selected_devices = select_devices(nr)
        if selected_devices is None:
            console.print(Panel("程序已退出", style="bold red", expand=False))
            break
        if len(selected_devices.inventory.hosts) == 0:
            console.print(Panel("未选择任何设备，请重新选择", style="bold yellow", expand=False))
            continue
        
        console.print(Panel(f"已选择 [bold cyan]{len(selected_devices.inventory.hosts)}[/bold cyan] 台设备:", 
                            style="bold green", expand=False))
        for host in selected_devices.inventory.hosts.values():
            console.print(f"  [magenta]•[/magenta] [cyan]{host.name}[/cyan] ([yellow]{host.hostname}[/yellow])")
        
        choice = get_command_choice()
        if choice == 'q':
            console.print(Panel("程序已退出", style="bold red", expand=False))
            break
        success_devices = []
        failed_devices = []
        total_devices = len(selected_devices.inventory.hosts)
        with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(bar_width=None, style="white", complete_style="light_green", finished_style="bold green"),
            "[progress.percentage][bold white]{task.percentage:>3.0f}%[/bold white]",
            "[cyan]{task.completed}/{task.total}[/cyan]",
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task("[bold blue]执行中...", total=total_devices)
            for device_name, device in selected_devices.inventory.hosts.items():
                command = get_command(choice, device_name)
                if command is None:
                    progress.update(task, advance=1)
                    continue
                if command == 'q':
                    break

                try:
                    if command == "SAVE_CONFIG":
                        console.print(f"[bold cyan]正在保存设备 {device_name} 的配置...[/bold cyan]")
                        result = save_config(selected_devices, device_name)
                    elif command == "FILE_COMMANDS":
                        filename = "file_config.txt"
                        result = commands_from_file(selected_devices, device_name, filename)
                    else:
                        result = send_command(selected_devices, device_name, command)

                    if isinstance(result, str) and "错误" in result:
                        reason = result.split(':', 1)[-1].strip()
                        failed_devices.append((device, reason))
                    else:
                        success_devices.append((device, result))
                        # 暂时禁用Rich的控制台输出
                        original_stdout = sys.stdout
                        sys.stdout = io.StringIO()
                        # 执行print_result
                        print_result(result)
                        # 获取捕获的输出并重置stdout
                        output = sys.stdout.getvalue()
                        sys.stdout = original_stdout
                        # 使用Rich的控制台打印捕获的输出
                        console.print(output, highlight=False, markup=False, emoji=False)

                except Exception as e:
                    reason = str(e).split('\n')[-1]
                    failed_devices.append((device, reason))
                    console.print(f"[bold red]设备 {device_name} 执行失败:[/bold red] [yellow]{reason}[/yellow]")
                    
                progress.update(task, advance=1)

        console.print(Panel(
            f"[bold cyan]设备总数: {total_devices}[/bold cyan]\n"
            f"[bold green]成功设备数: {len(success_devices)}[/bold green]\n"
            f"[bold red]失败设备数: {len(failed_devices)}[/bold red]",
            title="执行结果汇总",
            expand=False
        ))

        if success_devices:
            success_table = Table(show_header=True, header_style="bold white", box=box.DOUBLE_EDGE)
            success_table.add_column("成功设备名称", style="bold green")
            success_table.add_column("IP地址", style="bold green")
            success_table.add_column("状态", style="bold green")

            for device, _ in success_devices:
                success_table.add_row(device.name, device.hostname, "✅")

            console.print(success_table)

        if failed_devices:
            failed_table = Table(show_header=True, header_style="bold white", box=box.DOUBLE_EDGE)
            failed_table.add_column("失败设备名称", style="bold red")
            failed_table.add_column("IP地址", style="bold red")
            failed_table.add_column("失败原因", style="bold red")

            for device, reason in failed_devices:
                failed_table.add_row(device.name, device.hostname, reason)

            console.print(failed_table)
        
        if success_devices:
            save_configs = console.input("[bold cyan]是否保存所有成功执行的设备配置？(y/n): [/bold cyan]").strip().lower() == 'y'
            if save_configs:
                for device, _ in success_devices:
                    try:
                        console.print(f"[bold blue]正在保存设备 {device.name} 的配置...[/bold blue]")
                        save_config(selected_devices, device.name)
                    except Exception as e:
                        console.print(f"[bold red]保存设备 {device.name} 配置失败:[/bold red] [yellow]{str(e)}[/yellow]")

        if console.input("[bold cyan]是否继续操作其他设备？(y/n): [/bold cyan]").strip().lower() != 'y':
            break

if __name__ == "__main__":
    main()
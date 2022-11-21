import os
import pathlib
import sys


def install_context_windows(dry_run: bool):
    binary = sys.argv[0]
    binary_dir = pathlib.Path(binary).parent
    exe = binary_dir / "caj2pdf-ec.exe"

    description = "Convert CAJ to PDF"
    command = f'"{exe}" "%1"'
    if dry_run:
        regedit = f"""\
            Windows Registry Editor Version 5.00

            [HKEY_CLASSES_ROOT\\.caj\\shell\\caj2pdf]
            @="{description}"

            [HKEY_CLASSES_ROOT\\.caj\\shell\\caj2pdf\\command]
            @="{command}"
            """
        print(regedit, file=sys.stderr)
    else:
        import ctypes
        import winreg

        if 1 != ctypes.windll.shell32.IsUserAnAdmin():
            # https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecutew
            # https://support.microsoft.com/zh-cn/topic/wd2000-%E5%A6%82%E4%BD%95%E8%B0%83%E7%94%A8-shellexecute-windows-api-%E5%87%BD%E6%95%B0-80da207b-2fa3-ac60-e871-f0a63164bad7
            apifn = ctypes.windll.shell32.ShellExecuteW
            args = (
                # 没有主窗口
                None,
                # 运行 runas 命令
                "runas",
                # 可执行文件
                binary,
                # 运行该程序时的参数
                "install",
                # 工作目录
                os.getcwd(),
                # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
                # 激活并显示窗口
                1,
            )
            # TODO 权限获取失败，弹窗消失太快看不清报错。
            print(apifn, args)
            status = apifn(*args)
            if status <= 32:
                raise WindowsError((f"win32api错误，返回 {status}", ("ShellExecuteW", args)))
        else:
            # 如果拥有管理员权限
            reg = winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT)
            cajshell = winreg.CreateKeyEx(
                key=winreg.HKEY_CLASSES_ROOT,
                sub_key=".caj\\shell\\caj2pdf",
                reserved=0,
                access=winreg.KEY_WRITE,
            )
            winreg.SetValue(
                winreg.HKEY_CLASSES_ROOT,
                ".caj\\shell\\caj2pdf",
                winreg.REG_SZ,
                description,
            )
            cajshellcmd = winreg.CreateKeyEx(
                key=winreg.HKEY_CLASSES_ROOT,
                sub_key=".caj\\shell\\caj2pdf\\command",
                reserved=0,
                access=winreg.KEY_WRITE,
            )
            winreg.SetValue(
                winreg.HKEY_CLASSES_ROOT,
                ".caj\\shell\\caj2pdf\\command",
                winreg.REG_SZ,
                command,
            )
            cajshellcmd.Close()
            cajshell.Close()
            reg.Close()

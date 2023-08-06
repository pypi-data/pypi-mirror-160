import ctypes, sys, os


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def admin_cmd(cmd=None):
    assert_admin = ctypes.windll.shell32.IsUserAnAdmin()
    if assert_admin:
        print("admin_exe函数内，以管理员权限运行")
        os.system(cmd)
    else:
        if sys.version_info[0] == 3:
            print('admin_exe函数内，还没有管理员权限')
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


if __name__ == '__main__':
    admin_cmd("taskkill /F /IM WUDFHost.exe")

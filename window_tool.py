import time

import win32con
import win32gui
from PIL import ImageGrab
from pynput.mouse import Controller, Button


def get_window_position_by_title(window_title):
    """
    根据窗口标题获取窗口的位置和大小。

    :param window_title: 窗口标题（部分匹配即可）
    :return: 包含窗口位置和大小的字典，或 None 如果未找到窗口
    """

    def callback(hwnd, hwnds):
        # 检查窗口标题是否包含指定的字符串
        if window_title.lower() in win32gui.GetWindowText(hwnd).lower():
            hwnds.append(hwnd)
        return True

    hwnds = []
    # 枚举所有顶级窗口
    win32gui.EnumWindows(callback, hwnds)

    if not hwnds:
        print(f"未找到标题包含 '{window_title}' 的窗口")
        return None

    # 获取第一个匹配窗口的句柄
    hwnd = hwnds[0]
    print(f"找到窗口句柄: {hwnd}")

    # 获取窗口的矩形区域 (左, 上, 右, 下)
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect

    # 计算窗口的宽度和高度
    width = right - left
    height = bottom - top

    # 输出窗口信息
    print(f"窗口标题: {win32gui.GetWindowText(hwnd)}")
    print(f"窗口位置: 左={left}, 上={top}, 宽={width}, 高={height}")
    return {
        "title": win32gui.GetWindowText(hwnd),
        "left": left,
        "top": top,
        "width": width,
        "height": height
    }


def is_window_active(window_title):
    """
    判断指定标题的窗口是否处于激活状态。

    :param window_title: 窗口标题（部分匹配即可）
    :return: 如果窗口处于激活状态返回 True，否则返回 False
    """
    # 获取当前激活窗口的句柄
    active_hwnd = win32gui.GetForegroundWindow()
    if active_hwnd == 0:
        return False

    # 获取激活窗口的标题
    active_window_title = win32gui.GetWindowText(active_hwnd)

    # 判断目标窗口标题是否包含在激活窗口标题中
    return window_title.lower() in active_window_title.lower()


def simulate_mouse_click(x, y):
    """
    模拟鼠标点击指定位置。

    :param x: 点击的 X 坐标
    :param y: 点击的 Y 坐标
    """
    mouse = Controller()
    # 移动鼠标到指定位置
    mouse.position = (x, y)
    time.sleep(0.1)  # 等待鼠标移动完成
    # 模拟鼠标左键点击
    mouse.click(Button.left, 1)
    print(f"已点击位置: ({x}, {y})")


def activate_window(window_title):
    """
    激活指定标题的窗口。

    :param window_title: 窗口标题（部分匹配即可）
    :return: 窗口句柄 (HWND)
    """

    def callback(hwnd, hwnds):
        if window_title.lower() in win32gui.GetWindowText(hwnd).lower():
            hwnds.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)

    if not hwnds:
        raise Exception(f"未找到标题包含 '{window_title}' 的窗口")

    hwnd = hwnds[0]
    # 将窗口置于前台
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 还原窗口（如果最小化）
    win32gui.SetForegroundWindow(hwnd)  # 激活窗口
    time.sleep(0.5)  # 等待窗口激活完成
    return hwnd


def capture_window(hwnd):
    """
    截图指定窗口。

    :param hwnd: 窗口句柄 (HWND)
    :return: 截图的 PIL 图像对象
    """
    # 获取窗口的矩形区域 (左, 上, 右, 下)
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect

    # 截取窗口区域
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    return screenshot
# if __name__ == "__main__":
#     # 目标窗口的部分标题
#     target_window_title = "Notepad"  # 示例：记事本窗口
#
#     # 检查目标窗口是否激活
#     if is_window_active(target_window_title):
#         print(f"窗口 '{target_window_title}' 已激活，执行点击操作...")
#         # 在屏幕上的某个位置模拟点击（例如：屏幕坐标 (500, 300)）
#         simulate_mouse_click(500, 300)
#     else:
#         print(f"窗口 '{target_window_title}' 未激活")

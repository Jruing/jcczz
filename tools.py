from window_tool import is_window_active, simulate_mouse_click
from window_tool import get_window_position_by_title
from config import image_items,window_items
from cv2_tool import cv_detections
import pathlib

# 获取窗口位置
title = window_items["title"]
window_info = get_window_position_by_title(title)
print(window_info)
# 获取图片路径并识别
hero_image_path = pathlib.Path(image_items["hero"])
other_image_path = pathlib.Path(image_items["other"])
hero_image = hero_image_path.absolute().joinpath("yasuo.png")
other_image = other_image_path.absolute().joinpath("full.png")
print(hero_image,other_image)
rs = cv_detections(other_image, hero_image)
# 计算坐标并点击
win_x = window_info["left"]
win_y = window_info["top"]
# 检查目标窗口是否激活
if is_window_active(title):
    print(f"窗口 '{title}' 已激活，执行点击操作...")
    # 在屏幕上的某个位置模拟点击（例如：屏幕坐标 (500, 300)）
    for i in rs:
        x = i[0] + win_x
        y = i[1] + win_y
        simulate_mouse_click(x, y)
else:
    print(f"窗口 '{title}' 未激活")

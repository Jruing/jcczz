import pathlib
import threading
import time
import tkinter as tk
from tkinter import ttk

from pynput import keyboard
from pypinyin import lazy_pinyin

from config import image_items, window_items
from cv2_tool import cv_detections
from data.script import DataBatch
from window_tool import is_window_active, simulate_mouse_click, capture_window, activate_window, \
    get_window_position_by_title


class AssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("助手")
        self.root.geometry("650x600")
        self.save_hero = []
        self.data = DataBatch()


        # 第一个容器
        self.frame1 = ttk.Frame(self.root)
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label1 = ttk.Label(self.frame1, text="费用:")
        self.label1.grid(row=0, column=0, padx=5, pady=5)

        self.radio_var1 = tk.StringVar()
        self.radio_var1.set("1")
        self.radio_var1.trace("w", self.update_listbox)

        for i in range(1, 6):
            radio_button = ttk.Radiobutton(self.frame1, text=f"{i}费", variable=self.radio_var1, value=str(i))
            radio_button.grid(row=i, column=0, padx=5, pady=5)

        # 第二个容器
        self.frame2 = ttk.Frame(self.root)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.label2 = ttk.Label(self.frame2, text="特质:")
        self.label2.grid(row=0, column=0, padx=5, pady=5)

        self.radio_var2 = tk.StringVar()
        self.radio_var2.trace("w", self.update_listbox)

        tezhi = self.data.tezhi_list

        for i in range(1, len(tezhi) + 1):
            radio_button = ttk.Radiobutton(self.frame2, text=list(tezhi[i - 1].keys())[0],
                                           variable=self.radio_var2,
                                           value=str(list(tezhi[i - 1].values())[0]))
            radio_button.grid(row=i, column=0, padx=5, pady=5)

        # 第二个容器
        self.frame22 = ttk.Frame(self.root)
        self.frame22.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.label22 = ttk.Label(self.frame22, text="职业:")
        self.label22.grid(row=0, column=0, padx=5, pady=5)

        self.radio_var22 = tk.StringVar()
        self.radio_var22.trace("w", self.update_listbox)

        print(self.data.zhiye_json)
        zhiye_name = self.data.zhiye_list

        for i in range(1, len(zhiye_name) + 1):
            radio_button = ttk.Radiobutton(self.frame22, text=list(zhiye_name[i - 1].keys())[0],
                                           variable=self.radio_var22,
                                           value=str(list(zhiye_name[i - 1].values())[0]))
            radio_button.grid(row=i, column=0, padx=5, pady=5)

        # 第三个容器
        self.frame3 = ttk.Frame(self.root)
        self.frame3.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.label3 = ttk.Label(self.frame3, text="英雄:")
        self.label3.grid(row=0, column=0, padx=5, pady=5)

        self.listbox = tk.Listbox(self.frame3, selectmode=tk.MULTIPLE)
        self.listbox.grid(row=1, column=0, padx=5, pady=5)

        self.update_listbox()
        self.add_button = ttk.Button(self.frame3, text="添加", command=self.add_selected_heroes)
        self.add_button.grid(row=3, column=0)

        # 第四个容器
        self.frame4 = ttk.Frame(self.root)
        self.frame4.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        self.label4 = ttk.Label(self.frame4, text="选中的英雄:")
        self.label4.grid(row=0, column=0, padx=5, pady=5)

        self.selected_heroes_listbox = tk.Listbox(self.frame4, selectmode=tk.MULTIPLE)
        self.selected_heroes_listbox.grid(row=1, column=0, padx=5, pady=5)

        self.remove_button = ttk.Button(self.frame4, text="删除", command=self.remove_selected_heroes)
        self.remove_button.grid(row=3, column=0)
        self.remove_button = ttk.Button(self.frame4, text="重置", command=self.reset_select)
        self.remove_button.grid(row=4, column=0)

        self.save_button = ttk.Button(self.frame4, text="保存", command=self.save_heroes)
        self.save_button.grid(row=45, column=0)

    # 任务 1：键盘监听
    def listen_keyboard(self):
        def on_press(key):
            try:
                print(f"按键 {key.char} 被按下")
                if key.char == "D" or key.char == 'd':
                    # 获取窗口位置
                    title = window_items["title"]
                    # 激活窗口
                    hwnd = activate_window(title)
                    print(f"窗口 '{title}' 已激活")
                    # 获取图片路径并识别
                    time.sleep(0.5)
                    other_image_path = pathlib.Path(image_items["other"])
                    other_image = other_image_path.absolute().joinpath("full.png")
                    try:
                        # 截图窗口
                        screenshot = capture_window(hwnd)
                        images_path = other_image_path.absolute().joinpath("full.png")
                        screenshot.save(images_path)  # 保存截图
                        print(f"截图已保存为 {images_path}")
                    except Exception as e:
                        print(f"发生错误: {e}")
                    # 获取窗口信息
                    window_info = get_window_position_by_title(title)
                    print(window_info)
                    # 识别
                    print("保存的英雄列表", self.save_hero)
                    for i in self.save_hero:
                        result = ''.join(lazy_pinyin(i))
                        print("result",i,result)
                        hero_image_path = pathlib.Path(image_items["hero"])
                        hero_image = hero_image_path.absolute().joinpath(f"{result}.png")
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
                                time.sleep(0.3)
                                simulate_mouse_click(x, y)
                        else:
                            activate_window(title)
                            print(f"窗口 '{title}' 未激活")
            except AttributeError:
                print(f"特殊键 {key} 被按下")
            if key == keyboard.Key.esc:
                return False  # 按下 ESC 键退出监听

        with keyboard.Listener(on_press=on_press) as listener:
            print("开始监听键盘事件...")
            listener.join()

    def save_heroes(self):
        selected_heroes = self.selected_heroes_listbox.get(0, tk.END)
        print("Selected heroes:", selected_heroes)
        self.save_hero.extend(selected_heroes)

    def update_listbox(self, *args):
        data = self.data.save_data()

        price_option = self.radio_var1.get()
        tezhi_option = self.radio_var2.get()
        zhiye_option = self.radio_var22.get()
        if price_option and tezhi_option and zhiye_option:
            key = f"{tezhi_option}_{zhiye_option}_{price_option}"
            items = data.get(f"{tezhi_option}_{zhiye_option}_{price_option}", [])

        elif price_option and tezhi_option and zhiye_option == "":
            key = f"{tezhi_option}_*_{price_option}"
            tezhi, zhiye, price = key.split("_")
            items = []
            for i in data.keys():
                if i.startswith(f"{tezhi}_") and i.endswith(f"_{price}"):
                    items.extend(data.get(i, []))

        elif price_option and zhiye_option and tezhi_option == "":
            key = f"*_{zhiye_option}_{price_option}"
            tezhi, zhiye, price = key.split("_")
            items = []
            for i in data.keys():
                if i.endswith(f"_{zhiye}_{price}"):
                    items.extend(data.get(i, []))
        else:
            key = f"*_*_{price_option}"
            tezhi, zhiye, price = key.split("_")
            items = []
            for i in data.keys():
                if i.endswith(f"_{price}"):
                    items.extend(data.get(i, []))
        print("key", f"{tezhi_option}_{zhiye_option}_{price_option}")
        self.listbox.delete(0, tk.END)
        for item in set(items):
            self.listbox.insert(tk.END, item)

    def add_selected_heroes(self):
        selected_indices = self.listbox.curselection()
        selected_items = [self.listbox.get(i) for i in selected_indices]
        for item in selected_items:
            if item not in self.selected_heroes_listbox.get(0, tk.END):
                self.selected_heroes_listbox.insert(tk.END, item)

    def remove_selected_heroes(self):
        selected_indices = self.selected_heroes_listbox.curselection()
        for index in reversed(selected_indices):
            self.selected_heroes_listbox.delete(index)

    def reset_select(self):
        self.radio_var1.set("1")
        self.radio_var2.set("")
        self.radio_var22.set("")
        self.update_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantApp(root)
    keyboard_thread = threading.Thread(target=app.listen_keyboard, daemon=True)
    keyboard_thread.start()
    # # 主线程等待子线程结束（实际上不会结束，因为是守护线程）
    # keyboard_thread.join()
    root.mainloop()

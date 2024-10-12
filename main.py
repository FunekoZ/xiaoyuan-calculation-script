import cv2
import numpy as np
import pyautogui
import pytesseract
import re
from tkinter import Tk, Toplevel, Canvas, Button, Label
from threading import Thread
import time
from PIL import Image, ImageTk

pytesseract.pytesseract_cmd = r"D:\DBDAFKPRO\tesseract-ocr\tesseract.exe"  # 设置 Tesseract-OCR 的路径

border_size = 80  # 每个正方形边框的大小
recognition_running = False  # 控制识别是否在运行
recognition_thread = None  # 识别线程
left_image_label = None  # 显示左侧预处理图像的Label
right_image_label = None  # 显示右侧预处理图像的Label
left_window_position = [300, 300]  # 左边框初始位置
right_window_position = [500, 300]  # 右边框初始位置
left_window = None  # 左边框窗口
right_window = None  # 右边框窗口
drag_data = {"x": 0, "y": 0}  # 用于拖动窗口的变量

# 绘制左右红色正方形边框，保持中间透明并绑定拖动事件
def draw_red_borders():
    global left_window, right_window, left_image_label, right_image_label

    root = Tk()
    root.title("识别控制")

    # 创建左正方形边框窗口
    left_window = Toplevel(root)
    left_window.overrideredirect(True)
    left_window.geometry(f"{border_size}x{border_size}+{left_window_position[0]}+{left_window_position[1]}")
    left_window.attributes("-topmost", True)
    left_window.config(bg='white')  # 设置白色为背景色并且设置透明区域为白色
    left_window.attributes("-transparentcolor", "white")  # 白色部分透明

    canvas_left = Canvas(left_window, width=border_size, height=border_size, bg='white', highlightthickness=0)
    canvas_left.create_rectangle(0, 0, border_size, border_size, outline="#FFC8C8", width=10)  # 仅绘制边框
    canvas_left.pack()

    # 创建右正方形边框窗口
    right_window = Toplevel(root)
    right_window.overrideredirect(True)
    right_window.geometry(f"{border_size}x{border_size}+{right_window_position[0]}+{right_window_position[1]}")
    right_window.attributes("-topmost", True)
    right_window.config(bg='white')
    right_window.attributes("-transparentcolor", "white")

    canvas_right = Canvas(right_window, width=border_size, height=border_size, bg='white', highlightthickness=0)
    canvas_right.create_rectangle(0, 0, border_size, border_size, outline="#FFC8C8", width=10)
    canvas_right.pack()

    # 绑定鼠标拖动事件到整个透明区域和边框
    canvas_left.bind("<ButtonPress-1>", lambda event: start_drag(event, "left"))
    canvas_left.bind("<B1-Motion>", lambda event: on_drag(event, "left"))

    canvas_right.bind("<ButtonPress-1>", lambda event: start_drag(event, "right"))
    canvas_right.bind("<B1-Motion>", lambda event: on_drag(event, "right"))

    # 添加“开始识别”和“停止识别”按钮
    start_button = Button(root, text="开始识别", command=start_recognition)
    start_button.pack(pady=10)

    stop_button = Button(root, text="停止识别", command=stop_recognition)
    stop_button.pack(pady=10)

    # 添加用于显示左侧和右侧预处理图像的Label
    left_image_label = Label(root, text="左侧图像")
    left_image_label.pack(pady=10, side="left", padx=20)

    right_image_label = Label(root, text="右侧图像")
    right_image_label.pack(pady=10, side="right", padx=20)

    root.mainloop()

# 鼠标按下事件处理，记录初始位置
def start_drag(event, side):
    drag_data["x"] = event.x
    drag_data["y"] = event.y

# 鼠标拖动事件处理，更新窗口位置
def on_drag(event, side):
    global left_window_position, right_window_position

    x_offset = event.x - drag_data["x"]
    y_offset = event.y - drag_data["y"]

    if side == "left":
        left_window_position[0] += x_offset
        left_window_position[1] += y_offset
        left_window.geometry(f"{border_size}x{border_size}+{left_window_position[0]}+{left_window_position[1]}")
    elif side == "right":
        right_window_position[0] += x_offset
        right_window_position[1] += y_offset
        right_window.geometry(f"{border_size}x{border_size}+{right_window_position[0]}+{right_window_position[1]}")

# 将OpenCV图像转换为Tkinter可以显示的格式
def convert_image_to_tk(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image_rgb)
    tk_image = ImageTk.PhotoImage(pil_image)
    return tk_image

# 捕获左边框区域的内容
def capture_left_area():
    try:
        screenshot_left = pyautogui.screenshot(region=(left_window_position[0], left_window_position[1], border_size, border_size))
        return np.array(screenshot_left)
    except Exception as e:
        print(f"左边框截屏时出错: {str(e)}")
        return None

# 捕获右边框区域的内容
def capture_right_area():
    try:
        screenshot_right = pyautogui.screenshot(region=(right_window_position[0], right_window_position[1], border_size, border_size))
        return np.array(screenshot_right)
    except Exception as e:
        print(f"右边框截屏时出错: {str(e)}")
        return None

# 图像预处理以增强识别效果
# 图像预处理以增强识别效果
def enhance_image_for_ocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转为灰度图
    _, thresh = cv2.threshold(gray, zz50, 255, cv2.THRESH_BINARY_INV)  # 阈值化，白底黑字

    return thresh

# 识别纯黑色数字并打印识别的内容
def recognize_black_numbers(image, area_name, label):
    enhanced_image = enhance_image_for_ocr(image)
    tk_image = convert_image_to_tk(enhanced_image)
    label.config(image=tk_image)
    label.image = tk_image

    text = pytesseract.image_to_string(enhanced_image, config=r'--psm 6 -c tessedit_char_whitelist=0123456789')

    numbers = re.findall(r'\d+', text)

    return int(numbers[0]) if numbers else None

# 比较左右正方形边框中的数字并执行操作
def compare_and_draw(left_number, right_number):
    if left_number is None or right_number is None:
        print("...")
        return

    if left_number > right_number:
        pyautogui.press(".")
        print(f"{left_number} > {right_number}")
    elif left_number < right_number:
        pyautogui.press(",")
        print(f"{left_number} < {right_number}")

# 主识别逻辑
def recognition_loop():
    global recognition_running
    try:
        while recognition_running:
            left_image = capture_left_area()
            right_image = capture_right_area()

            if left_image is not None and right_image is not None:
                left_number = recognize_black_numbers(left_image, "左边框", left_image_label)
                right_number = recognize_black_numbers(right_image, "右边框", right_image_label)
                compare_and_draw(left_number, right_number)

            time.sleep(0.5)
    except SystemExit as e:
        print(e)

# 启动识别
def start_recognition():
    global recognition_running, recognition_thread
    if recognition_running:
        return
    recognition_running = True
    recognition_thread = Thread(target=recognition_loop)
    recognition_thread.start()

# 停止识别
def stop_recognition():
    global recognition_running, recognition_thread
    recognition_running = False
    if recognition_thread:
        recognition_thread.join()
        recognition_thread = None

# 启动程序
if __name__ == "__main__":
    border_thread = Thread(target=draw_red_borders)
    border_thread.start()

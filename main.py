import tkinter as tk
import qrcode
from PIL import ImageTk
from tkinter import filedialog, messagebox


# ==============================
# 创建窗口
# ==============================

window = tk.Tk()

window.title("二维码生成器")
window.geometry("960x540")
window.resizable(False, False)

# 设置背景颜色
window.configure(bg="#f5f5f5")


# ==============================
# 当前二维码
# ==============================

current_qr = None


# ==============================
# 生成二维码
# ==============================

def generate_qrcode():
    global current_qr

    text = entry.get()

    # 判断输入是否为空
    if text == "":
        messagebox.showwarning(
            "提示",
            "请输入文字或网址！"
        )
        return

    # 生成二维码
    current_qr = qrcode.make(text)

    # 调整预览大小
    img = current_qr.resize((300, 300))

    # 转换成 Tkinter 可以显示的图片
    qr_image = ImageTk.PhotoImage(img)

    # 显示二维码
    qr_label.config(image=qr_image)

    # 防止图片被 Python 自动删除
    qr_label.image = qr_image


# ==============================
# 保存二维码
# ==============================

def save_qrcode():

    # 如果还没有生成二维码
    if current_qr is None:
        messagebox.showwarning(
            "提示",
            "请先生成二维码！"
        )
        return

    # 打开保存窗口
    file_path = filedialog.asksaveasfilename(
        title="保存二维码",
        defaultextension=".png",
        filetypes=[
            ("PNG 图片", "*.png"),
            ("JPEG 图片", "*.jpg")
        ]
    )

    # 用户选择了保存位置
    if file_path:

        current_qr.save(file_path)

        messagebox.showinfo(
            "成功",
            "二维码保存成功！"
        )


# ==============================
# 清空
# ==============================

def clear_all():
    global current_qr

    # 清空输入框
    entry.delete(0, tk.END)

    # 清除二维码
    qr_label.config(image="")

    qr_label.image = None

    # 清除当前二维码
    current_qr = None


# ==============================
# 标题
# ==============================

title = tk.Label(
    window,
    text="二维码生成器",
    font=("Microsoft YaHei", 26, "bold"),
    bg="#f5f5f5"
)

title.pack(pady=25)


# ==============================
# 主区域
# ==============================

main_frame = tk.Frame(
    window,
    bg="#f5f5f5"
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=60,
    pady=10
)


# ==============================
# 左侧区域
# ==============================

left_frame = tk.Frame(
    main_frame,
    bg="#f5f5f5"
)

left_frame.pack(
    side="left",
    fill="both",
    expand=True
)


# ==============================
# 右侧区域
# ==============================

right_frame = tk.Frame(
    main_frame,
    bg="#f5f5f5"
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True
)


# ==============================
# 输入提示
# ==============================

label = tk.Label(
    left_frame,
    text="输入文字或网址",
    font=("Microsoft YaHei", 13),
    bg="#f5f5f5"
)

label.pack(pady=10)


# ==============================
# 输入框
# ==============================

entry = tk.Entry(
    left_frame,
    width=35,
    font=("Microsoft YaHei", 12),
    relief="solid",
    bd=1
)

entry.pack(
    pady=10,
    ipady=8
)


# ==============================
# 生成二维码按钮
# ==============================

generate_button = tk.Button(
    left_frame,
    text="生成二维码",
    font=("Microsoft YaHei", 12, "bold"),
    width=18,
    relief="flat",
    command=generate_qrcode
)

generate_button.pack(
    pady=15,
    ipady=6
)


# ==============================
# 保存二维码按钮
# ==============================

save_button = tk.Button(
    left_frame,
    text="保存二维码",
    font=("Microsoft YaHei", 12),
    width=18,
    relief="flat",
    command=save_qrcode
)

save_button.pack(
    pady=5,
    ipady=6
)


# ==============================
# 清空按钮
# ==============================

clear_button = tk.Button(
    left_frame,
    text="清空",
    font=("Microsoft YaHei", 12),
    width=18,
    relief="flat",
    command=clear_all
)

clear_button.pack(
    pady=5,
    ipady=6
)


# ==============================
# 二维码预览标题
# ==============================

preview_label = tk.Label(
    right_frame,
    text="二维码预览",
    font=("Microsoft YaHei", 16, "bold"),
    bg="#f5f5f5"
)

preview_label.pack(pady=10)


# ==============================
# 二维码显示区域
# ==============================

qr_label = tk.Label(
    right_frame,
    bg="white",
    width=320,
    height=320
)

qr_label.pack(pady=5)


# ==============================
# 启动程序
# ==============================

window.mainloop()
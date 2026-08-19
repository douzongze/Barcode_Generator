import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
import qrcode


# UI 设置
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BG_COLOR = "#F5F7FA"
CARD_COLOR = "#FFFFFF"
TEXT_COLOR = "#1F2937"
SECONDARY_TEXT = "#6B7280"


window = ctk.CTk()
window.title("二维码生成器")
window.geometry("960x540")
window.resizable(False, False)
window.configure(fg_color=BG_COLOR)


# 当前生成的二维码
current_qr = None


def generate_qrcode():
    global current_qr

    text = entry.get().strip()

    if text == "":
        messagebox.showwarning(
            "提示",
            "请输入文字或网址！"
        )
        return

    current_qr = qrcode.make(text)

    preview_image = current_qr.resize((300, 300))

    qr_image = ctk.CTkImage(
        light_image=preview_image,
        dark_image=preview_image,
        size=(300, 300)
    )

    qr_label.configure(
        image=qr_image,
        text=""
    )

    qr_label.image = qr_image


def save_qrcode():
    if current_qr is None:
        messagebox.showwarning(
            "提示",
            "请先生成二维码！"
        )
        return

    file_path = filedialog.asksaveasfilename(
        title="保存二维码",
        defaultextension=".png",
        filetypes=[
            ("PNG 图片", "*.png"),
            ("JPEG 图片", "*.jpg")
        ]
    )

    if file_path:
        current_qr.save(file_path)

        messagebox.showinfo(
            "保存成功",
            "二维码保存成功！"
        )


def clear_all():
    global current_qr

    entry.delete(0, tk.END)

    qr_label.configure(
        image=None,
        text="二维码将在这里显示"
    )

    qr_label.image = None
    current_qr = None


# 标题
title = ctk.CTkLabel(
    window,
    text="二维码生成器",
    font=("Microsoft YaHei", 28, "bold"),
    text_color=TEXT_COLOR
)

title.pack(
    pady=(25, 3)
)


subtitle = ctk.CTkLabel(
    window,
    text="输入内容，快速生成二维码",
    font=("Microsoft YaHei", 14),
    text_color=SECONDARY_TEXT
)

subtitle.pack(
    pady=(0, 15)
)


# 左右布局
main_frame = ctk.CTkFrame(
    window,
    corner_radius=20,
    fg_color=BG_COLOR
)

main_frame.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=5
)


left_frame = ctk.CTkFrame(
    main_frame,
    corner_radius=20,
    fg_color=CARD_COLOR
)

left_frame.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 10),
    pady=5
)


right_frame = ctk.CTkFrame(
    main_frame,
    corner_radius=20,
    fg_color=CARD_COLOR
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(10, 0),
    pady=5
)


# 输入区域
input_label = ctk.CTkLabel(
    left_frame,
    text="输入内容",
    font=("Microsoft YaHei", 18, "bold"),
    text_color=TEXT_COLOR
)

input_label.pack(
    pady=(30, 10)
)


entry = ctk.CTkEntry(
    left_frame,
    width=320,
    height=48,
    corner_radius=10,
    placeholder_text="例如：https://github.com",
    font=("Microsoft YaHei", 13)
)

entry.pack(
    pady=10
)


generate_button = ctk.CTkButton(
    left_frame,
    text="生成二维码",
    width=220,
    height=45,
    corner_radius=10,
    font=("Microsoft YaHei", 14, "bold"),
    command=generate_qrcode
)

generate_button.pack(
    pady=(25, 10)
)


save_button = ctk.CTkButton(
    left_frame,
    text="保存二维码",
    width=220,
    height=45,
    corner_radius=10,
    font=("Microsoft YaHei", 14),
    command=save_qrcode
)

save_button.pack(
    pady=10
)


clear_button = ctk.CTkButton(
    left_frame,
    text="清空",
    width=220,
    height=45,
    corner_radius=10,
    font=("Microsoft YaHei", 14),
    command=clear_all
)

clear_button.pack(
    pady=10
)


# 二维码预览
preview_title = ctk.CTkLabel(
    right_frame,
    text="二维码预览",
    font=("Microsoft YaHei", 18, "bold"),
    text_color=TEXT_COLOR
)

preview_title.pack(
    pady=(25, 10)
)


qr_container = ctk.CTkFrame(
    right_frame,
    width=340,
    height=340,
    corner_radius=15,
    fg_color="#FFFFFF"
)

qr_container.pack(
    pady=5
)

qr_container.pack_propagate(False)


qr_label = ctk.CTkLabel(
    qr_container,
    text="二维码将在这里显示",
    width=300,
    height=300,
    text_color=SECONDARY_TEXT,
    font=("Microsoft YaHei", 13)
)

qr_label.pack(
    expand=True
)


# 版本号
version_label = ctk.CTkLabel(
    window,
    text="v0.1.0",
    font=("Microsoft YaHei", 11),
    text_color=SECONDARY_TEXT
)

version_label.pack(
    pady=(0, 5)
)


# 回车生成二维码
window.bind(
    "<Return>",
    lambda event: generate_qrcode()
)


window.mainloop()
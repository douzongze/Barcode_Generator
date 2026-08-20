import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

import customtkinter as ctk
import qrcode


# ==================== UI 设置 ====================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ==================== 主题颜色 ====================

BG_COLOR = ("#F5F7FA", "#18181B")
CARD_COLOR = ("#FFFFFF", "#27272A")
INPUT_COLOR = ("#FFFFFF", "#18181B")

TEXT_COLOR = ("#1F2937", "#F9FAFB")
SECONDARY_TEXT = ("#6B7280", "#A1A1AA")
HOVER_COLOR = ("#E5E7EB", "#3F3F46")

# 二维码背景始终保持白色
QR_COLOR = "#FFFFFF"


# ==================== 软件信息 ====================

APP_VERSION = "v0.3.0"
APP_AUTHOR = "douzongze"
GITHUB_URL = "https://github.com/douzongze/Barcode_Generator"


# ==================== 主窗口 ====================

window = ctk.CTk()

window.title("二维码生成器")

# 初始窗口大小
window.geometry("960x540")

# 最小窗口大小
window.minsize(760, 500)

# 允许改变窗口大小
window.resizable(True, True)

window.configure(
    fg_color=BG_COLOR
)


# ==================== 全局变量 ====================

current_qr = None
current_appearance = "浅色"


# ==================== 生成二维码 ====================

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


# ==================== 保存二维码 ====================

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


# ==================== 清空 ====================

def clear_all():

    global current_qr

    entry.delete(
        0,
        tk.END
    )

    qr_label.configure(
        image=None,
        text="二维码将在这里显示"
    )

    qr_label.image = None

    current_qr = None


# ==================== 切换主题 ====================

def change_appearance(choice):

    global current_appearance

    current_appearance = choice

    if choice == "浅色":

        ctk.set_appearance_mode(
            "light"
        )

    elif choice == "深色":

        ctk.set_appearance_mode(
            "dark"
        )

    elif choice == "跟随系统":

        ctk.set_appearance_mode(
            "system"
        )


# ==================== 设置窗口 ====================

def open_settings():

    settings_window = ctk.CTkToplevel(
        window
    )

    settings_window.title(
        "设置"
    )

    settings_window.geometry(
        "400x300"
    )

    settings_window.resizable(
        False,
        False
    )

    settings_window.transient(
        window
    )

    # 标题

    title_label = ctk.CTkLabel(
        settings_window,
        text="设置",
        font=(
            "Microsoft YaHei",
            22,
            "bold"
        ),
        text_color=TEXT_COLOR
    )

    title_label.pack(
        pady=(30, 25)
    )

    # 外观模式

    appearance_label = ctk.CTkLabel(
        settings_window,
        text="外观模式",
        font=(
            "Microsoft YaHei",
            14
        ),
        text_color=TEXT_COLOR
    )

    appearance_label.pack(
        pady=(5, 8)
    )

    # 外观选择

    appearance_menu = ctk.CTkOptionMenu(
        settings_window,
        values=[
            "浅色",
            "深色",
            "跟随系统"
        ],
        width=220,
        height=38,
        corner_radius=8,
        font=(
            "Microsoft YaHei",
            13
        ),
        command=change_appearance
    )

    appearance_menu.set(
        current_appearance
    )

    appearance_menu.pack(
        pady=5
    )


# ==================== 关于窗口 ====================

def open_about():

    about_window = ctk.CTkToplevel(
        window
    )

    about_window.title(
        "关于"
    )

    about_window.geometry(
        "460x330"
    )

    about_window.resizable(
        False,
        False
    )

    about_window.transient(
        window
    )

    # 软件名称

    title_label = ctk.CTkLabel(
        about_window,
        text="二维码生成器",
        font=(
            "Microsoft YaHei",
            24,
            "bold"
        ),
        text_color=TEXT_COLOR
    )

    title_label.pack(
        pady=(30, 20)
    )

    # 版本号

    version_label = ctk.CTkLabel(
        about_window,
        text=f"版本号：{APP_VERSION}",
        font=(
            "Microsoft YaHei",
            14
        ),
        text_color=SECONDARY_TEXT
    )

    version_label.pack(
        pady=5
    )

    # 作者

    author_label = ctk.CTkLabel(
        about_window,
        text=f"作者：{APP_AUTHOR}",
        font=(
            "Microsoft YaHei",
            14
        ),
        text_color=SECONDARY_TEXT
    )

    author_label.pack(
        pady=5
    )

    # GitHub 标题

    github_title = ctk.CTkLabel(
        about_window,
        text="GitHub 仓库",
        font=(
            "Microsoft YaHei",
            14
        ),
        text_color=TEXT_COLOR
    )

    github_title.pack(
        pady=(18, 5)
    )

    # GitHub 链接

    def open_github():

        webbrowser.open(
            GITHUB_URL
        )

    github_button = ctk.CTkButton(
        about_window,
        text=GITHUB_URL,
        width=390,
        height=38,
        corner_radius=8,
        fg_color="transparent",
        hover_color=HOVER_COLOR,
        text_color=(
            "#2563EB",
            "#60A5FA"
        ),
        font=(
            "Microsoft YaHei",
            12
        ),
        command=open_github
    )

    github_button.pack(
        pady=5
    )


# ==================== 顶部功能区 ====================

top_bar = ctk.CTkFrame(
    window,
    height=45,
    fg_color=BG_COLOR,
    corner_radius=0
)

top_bar.pack(
    fill="x",
    padx=20,
    pady=(8, 0)
)

top_bar.pack_propagate(
    False
)


# ==================== 关于按钮 ====================

about_button = ctk.CTkButton(
    top_bar,
    text="关于",
    width=65,
    height=32,
    corner_radius=8,
    fg_color="transparent",
    hover_color=HOVER_COLOR,
    text_color=TEXT_COLOR,
    font=(
        "Microsoft YaHei",
        13
    ),
    command=open_about
)

about_button.pack(
    side="right",
    padx=(5, 0)
)


# ==================== 设置按钮 ====================

settings_button = ctk.CTkButton(
    top_bar,
    text="设置",
    width=65,
    height=32,
    corner_radius=8,
    fg_color="transparent",
    hover_color=HOVER_COLOR,
    text_color=TEXT_COLOR,
    font=(
        "Microsoft YaHei",
        13
    ),
    command=open_settings
)

settings_button.pack(
    side="right"
)


# ==================== 标题 ====================

title = ctk.CTkLabel(
    window,
    text="二维码生成器",
    font=(
        "Microsoft YaHei",
        28,
        "bold"
    ),
    text_color=TEXT_COLOR
)

title.pack(
    pady=(5, 3)
)


subtitle = ctk.CTkLabel(
    window,
    text="输入内容，快速生成二维码",
    font=(
        "Microsoft YaHei",
        14
    ),
    text_color=SECONDARY_TEXT
)

subtitle.pack(
    pady=(0, 15)
)


# ==================== 主区域 ====================

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


# ==================== 主区域网格 ====================

main_frame.grid_columnconfigure(
    0,
    weight=1
)

main_frame.grid_columnconfigure(
    1,
    weight=1
)

main_frame.grid_rowconfigure(
    0,
    weight=1
)


# ==================== 左侧卡片 ====================

left_frame = ctk.CTkFrame(
    main_frame,
    corner_radius=20,
    fg_color=CARD_COLOR
)

left_frame.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 10),
    pady=5
)


# ==================== 右侧卡片 ====================

right_frame = ctk.CTkFrame(
    main_frame,
    corner_radius=20,
    fg_color=CARD_COLOR
)

right_frame.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(10, 0),
    pady=5
)


# ==================== 左侧布局 ====================

left_frame.grid_columnconfigure(
    0,
    weight=1
)

left_frame.grid_rowconfigure(
    0,
    weight=1
)

left_frame.grid_rowconfigure(
    1,
    weight=0
)

left_frame.grid_rowconfigure(
    2,
    weight=0
)

left_frame.grid_rowconfigure(
    3,
    weight=0
)

left_frame.grid_rowconfigure(
    4,
    weight=0
)

left_frame.grid_rowconfigure(
    5,
    weight=1
)


# ==================== 输入标题 ====================

input_label = ctk.CTkLabel(
    left_frame,
    text="输入内容",
    font=(
        "Microsoft YaHei",
        18,
        "bold"
    ),
    text_color=TEXT_COLOR
)

input_label.grid(
    row=0,
    column=0,
    pady=(35, 10),
    sticky="s"
)


# ==================== 输入框 ====================

entry = ctk.CTkEntry(
    left_frame,
    height=48,
    corner_radius=10,
    placeholder_text="例如：https://github.com",
    font=(
        "Microsoft YaHei",
        13
    ),
    fg_color=INPUT_COLOR,
    text_color=TEXT_COLOR
)

entry.grid(
    row=1,
    column=0,
    padx=35,
    pady=10,
    sticky="ew"
)


# ==================== 生成按钮 ====================

generate_button = ctk.CTkButton(
    left_frame,
    text="生成二维码",
    width=220,
    height=45,
    corner_radius=10,
    font=(
        "Microsoft YaHei",
        14,
        "bold"
    ),
    command=generate_qrcode
)

generate_button.grid(
    row=2,
    column=0,
    pady=(25, 10)
)


# ==================== 保存按钮 ====================

save_button = ctk.CTkButton(
    left_frame,
    text="保存二维码",
    width=220,
    height=45,
    corner_radius=10,
    font=(
        "Microsoft YaHei",
        14
    ),
    command=save_qrcode
)

save_button.grid(
    row=3,
    column=0,
    pady=10
)


# ==================== 清空按钮 ====================

clear_button = ctk.CTkButton(
    left_frame,
    text="清空",
    width=220,
    height=45,
    corner_radius=10,
    font=(
        "Microsoft YaHei",
        14
    ),
    command=clear_all
)

clear_button.grid(
    row=4,
    column=0,
    pady=10
)


# ==================== 右侧布局 ====================

right_frame.grid_columnconfigure(
    0,
    weight=1
)

right_frame.grid_rowconfigure(
    0,
    weight=0
)

right_frame.grid_rowconfigure(
    1,
    weight=1
)


# ==================== 预览标题 ====================

preview_title = ctk.CTkLabel(
    right_frame,
    text="二维码预览",
    font=(
        "Microsoft YaHei",
        18,
        "bold"
    ),
    text_color=TEXT_COLOR
)

preview_title.grid(
    row=0,
    column=0,
    pady=(25, 10)
)


# ==================== 二维码容器 ====================

qr_container = ctk.CTkFrame(
    right_frame,
    width=340,
    height=340,
    corner_radius=15,
    fg_color=QR_COLOR
)

qr_container.grid(
    row=1,
    column=0,
    padx=30,
    pady=(5, 25),
    sticky="nsew"
)

qr_container.grid_propagate(
    False
)


# ==================== 二维码显示 ====================

qr_label = ctk.CTkLabel(
    qr_container,
    text="二维码将在这里显示",
    width=300,
    height=300,
    text_color=(
        "#6B7280",
        "#6B7280"
    ),
    font=(
        "Microsoft YaHei",
        13
    )
)

qr_label.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ==================== 回车生成 ====================

window.bind(
    "<Return>",
    lambda event: generate_qrcode()
)


# ==================== 启动 ====================

window.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import tempfile
import os
import sys

import customtkinter as ctk

import qrcode
import barcode

from barcode.writer import ImageWriter
from PIL import Image


# ==================================================
# 基础设置
# ==================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


# ==================================================
# 颜色
# ==================================================

BG_COLOR = (
    "#F5F7FA",
    "#18181B"
)

CARD_COLOR = (
    "#FFFFFF",
    "#27272A"
)

INPUT_COLOR = (
    "#FFFFFF",
    "#18181B"
)

TEXT_COLOR = (
    "#1F2937",
    "#F9FAFB"
)

SECONDARY_TEXT = (
    "#6B7280",
    "#A1A1AA"
)

HOVER_COLOR = (
    "#E5E7EB",
    "#3F3F46"
)

IMAGE_BG = "#FFFFFF"



# ==================================================
# 软件信息
# ==================================================

APP_VERSION = "v0.6.0"

APP_AUTHOR = "douzongze"

GITHUB_URL = (
    "https://github.com/douzongze/Barcode_Generator"
)



# ==================================================
# 资源路径
# ==================================================

def resource_path(relative):

    try:
        base_path = sys._MEIPASS

    except Exception:

        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        relative
    )




# ==================================================
# 主窗口
# ==================================================

window = ctk.CTk()


window.title(
    "Barcode Generator"
)


window.geometry(
    "1050x650"
)


window.minsize(
    850,
    600
)


window.configure(
    fg_color=BG_COLOR
)




# ==================================================
# 全局变量
# ==================================================

current_image = None


# 修复 pyimage1
preview_image_ref = None


# 保存 PIL 图片引用
preview_pil_ref = None



current_appearance = "浅色"


generate_shortcut = "<Control-Return>"




# ==================================================
# 图片预览（修复版）
# ==================================================

def show_preview(image):

    global preview_image_ref
    global preview_pil_ref


    try:

        preview = image.copy()


        max_width = 360

        max_height = 360


        preview.thumbnail(

            (
                max_width,
                max_height
            ),

            Image.Resampling.LANCZOS

        )


        preview_pil_ref = preview



        preview_image_ref = ctk.CTkImage(

            light_image=preview_pil_ref,

            dark_image=preview_pil_ref,

            size=preview_pil_ref.size

        )



        qr_label.configure(

            image=preview_image_ref,

            text=""

        )


        qr_label.update()



    except Exception as e:

        print(
            "Preview Error:",
            e
        )





# ==================================================
# 清除预览
# ==================================================

def clear_preview():

    global preview_image_ref
    global preview_pil_ref


    preview_image_ref = None

    preview_pil_ref = None



    qr_label.configure(

        image=None,

        text="预览区域"

    )


    qr_label.update()




# ==================================================
# 二维码生成
# ==================================================

def generate_qrcode():

    global current_image


    text = entry.get().strip()


    if not text:

        messagebox.showwarning(

            "提示",

            "请输入内容！"

        )

        return



    qr = qrcode.QRCode(

        version=None,

        error_correction=qrcode.constants.ERROR_CORRECT_M,

        box_size=12,

        border=4

    )


    qr.add_data(text)


    qr.make(
        fit=True
    )


    current_image = qr.make_image().convert(
        "RGB"
    )


    show_preview(
        current_image
    )
# ==================================================
# 条形码生成
# ==================================================

def generate_barcode():

    global current_image


    text = entry.get().strip()


    if not text:

        messagebox.showwarning(

            "提示",

            "请输入条形码内容！"

        )

        return



    barcode_types = {

        "Code128": "code128",

        "EAN-13": "ean13",

        "Code39": "code39",

        "UPC": "upc"

    }



    try:

        name = barcode_types[
            barcode_type_menu.get()
        ]



        temp = tempfile.NamedTemporaryFile(

            suffix=".png",

            delete=False

        )


        temp.close()



        filename = barcode.get(

            name,

            text,

            writer=ImageWriter()

        ).save(

            temp.name[:-4]

        )



        image = Image.open(

            filename

        ).convert(

            "RGB"

        )


        # 保存副本

        current_image = image.copy()


        # 不关闭 image
        # 防止 PIL 生命周期问题



        try:

            os.remove(
                filename
            )

        except:

            pass



        show_preview(

            current_image

        )



    except Exception as e:


        messagebox.showerror(

            "错误",

            str(e)

        )





# ==================================================
# 总生成
# ==================================================

def generate():


    if mode_menu.get() == "二维码":

        generate_qrcode()


    else:

        generate_barcode()






# ==================================================
# 保存图片
# ==================================================

def save_image():


    if current_image is None:

        messagebox.showwarning(

            "提示",

            "请先生成图片！"

        )

        return




    file_path = filedialog.asksaveasfilename(

        title="保存图片",

        defaultextension=".png",

        filetypes=[

            (
                "PNG 图片",
                "*.png"
            ),

            (
                "JPEG 图片",
                "*.jpg"
            )

        ]

    )



    if file_path:


        current_image.save(

            file_path

        )


        messagebox.showinfo(

            "完成",

            "图片保存成功！"

        )







# ==================================================
# 清空
# ==================================================

def clear_all():

    global current_image


    current_image = None


    entry.delete(

        0,

        tk.END

    )


    clear_preview()






# ==================================================
# 模式切换
# ==================================================

def change_mode(choice):


    if choice == "二维码":


        barcode_type_label.pack_forget()

        barcode_type_menu.pack_forget()



        entry.configure(

            placeholder_text="输入文字或网址"

        )



        generate_button.configure(

            text="生成二维码"

        )



    else:


        barcode_type_label.pack(

            pady=(10,5)

        )


        barcode_type_menu.pack(

            pady=5

        )



        entry.configure(

            placeholder_text="输入数字或编号"

        )



        generate_button.configure(

            text="生成条形码"

        )







# ==================================================
# 快捷键显示
# ==================================================

def format_key(event):


    keys = []



    if event.state & 0x0004:

        keys.append(
            "Ctrl"
        )



    if event.state & 0x0001:

        keys.append(
            "Shift"
        )



    if event.state & 0x0008:

        keys.append(
            "Alt"
        )



    key = event.keysym



    if key not in (

        "Control_L",

        "Shift_L",

        "Alt_L"

    ):

        keys.append(

            key

        )



    shortcut = "+".join(keys)



    shortcut_entry.delete(

        0,

        tk.END

    )


    shortcut_entry.insert(

        0,

        shortcut

    )



    return "break"






# ==================================================
# 快捷键转换
# ==================================================

def convert_shortcut(text):


    result = "<"



    parts = text.split("+")



    for p in parts[:-1]:


        if p == "Ctrl":

            result += "Control-"


        elif p == "Shift":

            result += "Shift-"


        elif p == "Alt":

            result += "Alt-"



    result += parts[-1]

    result += ">"


    return result
# ==================================================
# 应用快捷键
# ==================================================

def apply_shortcut():

    global generate_shortcut


    shortcut = shortcut_entry.get()



    if not shortcut:

        return



    try:

        window.unbind_all(
            "<Control-Return>"
        )



        generate_shortcut = shortcut



        window.bind(

            convert_shortcut(shortcut),

            lambda e: generate()

        )



        messagebox.showinfo(

            "完成",

            f"快捷键已设置：{shortcut}"

        )


    except:


        messagebox.showerror(

            "错误",

            "快捷键格式错误"

        )






# ==================================================
# 外观设置
# ==================================================

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


    else:

        ctk.set_appearance_mode(
            "system"
        )






# ==================================================
# 设置窗口
# ==================================================

def open_settings():

    settings_window = ctk.CTkToplevel(
        window
    )


    settings_window.title(
        "设置"
    )


    settings_window.geometry(
        "430x420"
    )


    settings_window.resizable(
        False,
        False
    )


    settings_window.transient(
        window
    )



    title = ctk.CTkLabel(

        settings_window,

        text="设置",

        font=(

            "Microsoft YaHei",

            22,

            "bold"

        ),

        text_color=TEXT_COLOR

    )


    title.pack(
        pady=(25,20)
    )



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
        pady=5
    )



    appearance_menu = ctk.CTkOptionMenu(

        settings_window,

        values=[

            "浅色",

            "深色",

            "跟随系统"

        ],

        width=230,

        height=38,

        corner_radius=8,

        command=change_appearance

    )


    appearance_menu.set(
        current_appearance
    )


    appearance_menu.pack(
        pady=10
    )





    shortcut_title = ctk.CTkLabel(

        settings_window,

        text="生成快捷键",

        font=(

            "Microsoft YaHei",

            14,

            "bold"

        ),

        text_color=TEXT_COLOR

    )


    shortcut_title.pack(
        pady=(25,5)
    )



    global shortcut_entry



    shortcut_entry = ctk.CTkEntry(

        settings_window,

        width=230,

        height=38,

        corner_radius=8,

        placeholder_text="例如 Ctrl+S"

    )


    shortcut_entry.pack(
        pady=8
    )



    shortcut_entry.bind(

        "<KeyPress>",

        format_key

    )




    apply_button = ctk.CTkButton(

        settings_window,

        text="应用快捷键",

        width=230,

        height=42,

        corner_radius=10,

        command=apply_shortcut

    )


    apply_button.pack(
        pady=10
    )







# ==================================================
# 关于窗口
# ==================================================

def open_about():


    about_window = ctk.CTkToplevel(
        window
    )


    about_window.title(
        "关于"
    )


    about_window.geometry(
        "460x400"
    )


    about_window.resizable(
        False,
        False
    )


    about_window.transient(
        window
    )



    title = ctk.CTkLabel(

        about_window,

        text="Barcode Generator",

        font=(

            "Microsoft YaHei",

            24,

            "bold"

        ),

        text_color=TEXT_COLOR

    )


    title.pack(
        pady=(30,20)
    )



    version = ctk.CTkLabel(

        about_window,

        text=f"版本号：{APP_VERSION}",

        font=(

            "Microsoft YaHei",

            14

        ),

        text_color=SECONDARY_TEXT

    )


    version.pack(
        pady=5
    )



    author = ctk.CTkLabel(

        about_window,

        text=f"作者：{APP_AUTHOR}",

        font=(

            "Microsoft YaHei",

            14

        ),

        text_color=SECONDARY_TEXT

    )


    author.pack(
        pady=5
    )



    feature = ctk.CTkLabel(

        about_window,

        text=(

            "支持功能：\n\n"

            "✓ QR Code\n"

            "✓ Code128\n"

            "✓ EAN-13\n"

            "✓ Code39\n"

            "✓ UPC"

        ),

        font=(

            "Microsoft YaHei",

            13

        ),

        justify="left",

        text_color=SECONDARY_TEXT

    )


    feature.pack(
        pady=15
    )



    github_button = ctk.CTkButton(

        about_window,

        text="打开 GitHub 项目",

        width=230,

        height=42,

        corner_radius=10,

        command=lambda:

        webbrowser.open(
            GITHUB_URL
        )

    )


    github_button.pack(
        pady=10
    )
# ==================================================
# 顶部工具栏
# ==================================================

top_bar = ctk.CTkFrame(

    window,

    height=45,

    fg_color=BG_COLOR,

    corner_radius=0

)


top_bar.pack(

    fill="x",

    padx=20,

    pady=(8,0)

)


top_bar.pack_propagate(
    False
)




about_button = ctk.CTkButton(

    top_bar,

    text="关于",

    width=70,

    height=32,

    corner_radius=8,

    fg_color="transparent",

    hover_color=HOVER_COLOR,

    text_color=TEXT_COLOR,

    command=open_about

)


about_button.pack(

    side="right",

    padx=5

)




settings_button = ctk.CTkButton(

    top_bar,

    text="设置",

    width=70,

    height=32,

    corner_radius=8,

    fg_color="transparent",

    hover_color=HOVER_COLOR,

    text_color=TEXT_COLOR,

    command=open_settings

)


settings_button.pack(

    side="right"

)





# ==================================================
# 标题
# ==================================================

title_label = ctk.CTkLabel(

    window,

    text="Barcode Generator",

    font=(

        "Microsoft YaHei",

        30,

        "bold"

    ),

    text_color=TEXT_COLOR

)


title_label.pack(
    pady=(5,2)
)



subtitle_label = ctk.CTkLabel(

    window,

    text="二维码与条形码生成器",

    font=(

        "Microsoft YaHei",

        14

    ),

    text_color=SECONDARY_TEXT

)


subtitle_label.pack(
    pady=(0,15)
)





# ==================================================
# 主区域
# ==================================================

main_frame = ctk.CTkFrame(

    window,

    fg_color=BG_COLOR,

    corner_radius=20

)


main_frame.pack(

    fill="both",

    expand=True,

    padx=40,

    pady=5

)


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




left_frame = ctk.CTkFrame(

    main_frame,

    fg_color=CARD_COLOR,

    corner_radius=20

)


left_frame.grid(

    row=0,

    column=0,

    sticky="nsew",

    padx=(0,10),

    pady=5

)




right_frame = ctk.CTkFrame(

    main_frame,

    fg_color=CARD_COLOR,

    corner_radius=20

)


right_frame.grid(

    row=0,

    column=1,

    sticky="nsew",

    padx=(10,0),

    pady=5

)





# ==================================================
# 左侧
# ==================================================

input_title = ctk.CTkLabel(

    left_frame,

    text="输入内容",

    font=(

        "Microsoft YaHei",

        18,

        "bold"

    ),

    text_color=TEXT_COLOR

)


input_title.pack(
    pady=(25,10)
)



mode_title = ctk.CTkLabel(

    left_frame,

    text="生成类型",

    font=(

        "Microsoft YaHei",

        14

    ),

    text_color=TEXT_COLOR

)


mode_title.pack(
    pady=5
)




mode_menu = ctk.CTkOptionMenu(

    left_frame,

    values=[

        "二维码",

        "条形码"

    ],

    width=230,

    height=38,

    corner_radius=8,

    command=change_mode

)


mode_menu.set(
    "二维码"
)


mode_menu.pack(
    pady=5
)





barcode_type_label = ctk.CTkLabel(

    left_frame,

    text="条形码类型",

    font=(

        "Microsoft YaHei",

        14

    )

)


barcode_type_menu = ctk.CTkOptionMenu(

    left_frame,

    values=[

        "Code128",

        "EAN-13",

        "Code39",

        "UPC"

    ],

    width=230,

    height=38,

    corner_radius=8

)


barcode_type_menu.set(
    "Code128"
)


barcode_type_label.pack_forget()

barcode_type_menu.pack_forget()





entry = ctk.CTkEntry(

    left_frame,

    height=45,

    width=270,

    corner_radius=10,

    placeholder_text="输入文字或网址"

)


entry.pack(

    pady=15

)





generate_button = ctk.CTkButton(

    left_frame,

    text="生成二维码",

    width=230,

    height=42,

    corner_radius=10,

    font=(

        "Microsoft YaHei",

        14,

        "bold"

    ),

    command=generate

)


generate_button.pack(
    pady=8
)



save_button = ctk.CTkButton(

    left_frame,

    text="保存图片",

    width=230,

    height=42,

    corner_radius=10,

    command=save_image

)


save_button.pack(
    pady=8
)



clear_button = ctk.CTkButton(

    left_frame,

    text="清空",

    width=230,

    height=42,

    corner_radius=10,

    command=clear_all

)


clear_button.pack(
    pady=8
)






# ==================================================
# 右侧预览
# ==================================================

preview_title = ctk.CTkLabel(

    right_frame,

    text="生成预览",

    font=(

        "Microsoft YaHei",

        18,

        "bold"

    )

)


preview_title.pack(
    pady=(25,10)
)



preview_box = ctk.CTkFrame(

    right_frame,

    width=400,

    height=400,

    corner_radius=15,

    fg_color=IMAGE_BG

)


preview_box.pack(

    padx=20,

    pady=10,

    expand=True

)


preview_box.pack_propagate(
    False
)




qr_label = ctk.CTkLabel(

    preview_box,

    text="预览区域",

    width=360,

    height=360

)


qr_label.place(

    relx=0.5,

    rely=0.5,

    anchor="center"

)





# ==================================================
# 默认快捷键
# ==================================================

window.bind(

    "<Control-Return>",

    lambda e: generate()

)





# ==================================================
# 退出
# ==================================================

def close_window():

    if messagebox.askokcancel(

        "退出",

        "确定退出 Barcode Generator？"

    ):

        window.destroy()



window.protocol(

    "WM_DELETE_WINDOW",

    close_window

)





# ==================================================
# 启动
# ==================================================

if __name__ == "__main__":

    window.mainloop()
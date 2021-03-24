# encoding: utf-8

from PIL import Image, ImageDraw, ImageFont
import sys
import time
import re
import os
import pathlib
import hashlib

FONT_NAME = "meiryo.ttc"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = WHITE
TEXT_COLOR = BLACK
LINE_SPACE_RATE = 0.1
MIN_IMG_RATE = 0.1
MARGIN_CAPTION_RATE = 0.1
MARGIN_BETWEEN_PICTURE_AND_CAPTION_RATE = 0.03
FONT_SIZE_RATE = 0.028

def calc_text_size(text, font):
    """text の文字列を font でレンダリングした際のサイズを調べる関数
    返り値は (width, height)
    """
    dummy_img = Image.new("RGB", (1, 1), BG_COLOR)
    drawer = ImageDraw.Draw(dummy_img)
    return drawer.textsize(text, font=font)

def create_horizontal_text_img(text, font, max_width):
    """text の文字列を font でレンダリングして Image として返す
    指定した横幅を超えない最大の縦幅の画像を作成する
    """
    texts_and_poses = []
    part_text = ""
    height = 0
    for t in text:
        time.sleep(0.01)
        part_text += t
        text_w, text_h = calc_text_size(part_text, font)
        if max_width < text_w:
            texts_and_poses += [[part_text[:-1], (0, height)]]
            part_text = t
            height += text_h + int(LINE_SPACE_RATE * font.size)
    texts_and_poses += [[part_text, (0, height)]]
    height += text_h
    img = Image.new("RGB", (max_width, height), BG_COLOR)
    drawer = ImageDraw.Draw(img)
    for text, pos in texts_and_poses:
        drawer.text(pos, text, fill=TEXT_COLOR, font=font)
    return img

def create_vertical_text_img(text, font, max_height, min_width=10):
    """text の文字列を font でレンダリングして Image として返す
    指定した縦幅を超えない最大の横幅の画像を作成する
    """
    width = min_width
    img_height = max_height + 1
    while max_height < img_height:
        width = width * 2
        img = create_horizontal_text_img(text, font, width)
        _, img_height = img.size
        estimated_max_width = width
    estimated_min_width = width

    while img_height < max_height and min_width < estimated_min_width :
        width = width // 2
        img = create_horizontal_text_img(text, font, width)
        _, img_height = img.size
        estimated_min_width = width
    estimated_min_width = width

    while 10 < abs(estimated_min_width - estimated_max_width):
        width = (estimated_min_width + estimated_max_width) // 2
        img = create_horizontal_text_img(text, font, width)
        _, img_height = img.size
        if img_height < max_height:
            estimated_max_width = width
        else:
            estimated_min_width = width

    width = estimated_max_width
    return create_horizontal_text_img(text, font, width)

def get_or_else(target_list, index, default_value, invalid_values=[None, ""]):
    """target_list にインデックスが index の値が存在しないか、
    invalid_values の値であった場合は default_value を返す関数
    """
    return_value = default_value
    if index < len(target_list) and target_list[index] not in invalid_values:
        return_value = target_list[index]
    return return_value

def file_read(file_path):
    """file_path のファイルをテキストとして読み込んで内容を返す
    """
    with open(file_path) as f:
        return_value = f.read()
    return return_value

def img_shrink(img, rate):
    """img の縦横を rate 倍する
    """
    return img.resize((int(img.width * rate), int(img.height * rate)))

def add_margin(img, new_width, new_height, anchor_x, anchor_y):
    """img を (new_width, new_height) になるように余白を追加する関数
    anchor_x, anchor_y によって余白の付く位置 = 画像が固定される位置を設定できる
    anchor_x: "left", "center", "right"
    anchor_y: "top", "center", "bottom"
    """
    new_img = Image.new(img.mode, (new_width, new_height), BG_COLOR)
    width, height = img.size
    if anchor_x == "left":
        start_x = 0
    elif anchor_x == "center":
        start_x = (new_width - width) // 2
    elif anchor_x == "right":
        start_x = new_width - width
    else:
        raise_value_error_and_generate_command("anchor_x is invalid. anchor_x: {}".format(anchor_x))
    if anchor_y == "top":
        start_y = 0
    elif anchor_y == "center":
        start_y = (new_height - height) // 2
    elif anchor_y == "bottom":
        start_y = new_height - height
    else:
        raise_value_error_and_generate_command("anchor_y is invalid. anchor_y: {}".format(anchor_y))
    new_img.paste(img, (start_x, start_y))
    return new_img

def add_caption(img, text, font, start_x, start_y, mode, max_length, min_length):
    """img にキャプションを追加する関数
    (start_x, start_y) からキャプションを開始し、mode の方向に伸ばす。
    """
    if mode ==  "horizontal":
        create_text_img_func = create_horizontal_text_img
    elif mode == "vertical":
        create_text_img_func = create_vertical_text_img
    else:
        raise_value_error_and_generate_command("mode is invalid. mode: {}".format(mode))

    text_img = create_text_img_func(text, font, max_length, min_length)
    new_img = img.copy()
    new_img.paste(text_img, (start_x, start_y))
    return new_img

def create_font_according_img(img):
    """img に基づいてフォントの大きさを決め、Font を返す関数
    """
    long_side = max(img.size)
    return ImageFont.truetype(FONT_NAME, int(long_side * FONT_SIZE_RATE))

def calc_text(text):
    """文字列を数式として計算する関数
    """
    if "+" in text:
        function = float.__add__
        operator = "+"
    elif "-" in text:
        function = float.__sub__
        operator = "-"
    elif "*" in text:
        function = float.__mul__
        operator = "*"
    else:
        return float(text)
    index = text.find(operator)
    A = text[:index]
    B = text[index+1:]
    return function(calc_text(A), calc_text(B))

def replace_and_calc_text(text, img):
    """文字列の中の予約語を適切な数値に置き換え、それを数式として計算する関数
    """
    width, height = img.size
    long_side, short_side = max(img.size), min(img.size)
    text = re.sub("long", str(long_side), text)
    text = re.sub("short", str(short_side), text)
    text = re.sub("width", str(width), text)
    text = re.sub("height", str(height), text)
    return int(calc_text(text))

def mkdir(path):
    """path のディレクトリを作成する関数
    既に存在する場合は何もしない
    """
    if os.path.exists(path):
        return
    os.mkdir(path)
    return

def raise_value_error_and_generate_command(error_text):
    raise ValueError(error_text + "\n"
        + "fix above error and execute below command\n"
        + "COMMAND: python3 \"" + str(pathlib.Path(__file__).resolve()) + "\" \"" + str(pathlib.Path(csv_path).resolve()) + "\" " + str(csv_index + 1)
    )
    return

def execute_line(line):
    """csv を一行ずつここに読み込ませて、キャプションとマージンを追加する
    """
    elements = line.split(",")[1:]
    img_path = get_or_else(elements, 0, "")
    output_name = get_or_else(elements, 1, img_path)

    print("\033[1A\033[2Kprocessing: {} -> {} ({}/{})".format(img_path, output_name, csv_index + 1, NoL))

    if len(line) < 1 or line[0]  in ["#", '"']:
        return

    if img_path == "" and get_or_else(elements, 2, "") == "":
        elements[2] = "2800"
    width_str = get_or_else(elements, 2, "long")
    if img_path == "":
        try:
            width = int(width_str)
        except ValueError:
            raise_value_error_and_generate_command("filepath is null and width is not numeric.")
        img = Image.new("RGB", (width, 1), BG_COLOR)
    else:
        img = Image.open(img_path)

    img_width, img_height = img.size

    width = replace_and_calc_text(width_str, img)
    height = replace_and_calc_text(get_or_else(elements, 3, "long"), img)
    anchor_x = get_or_else(elements, 4, "left")
    anchor_y = get_or_else(elements, 5, "top")
    margin = replace_and_calc_text(get_or_else(elements, 6, "long*0.01"), img)
    comment = ""
    if 7 < len(elements):
        comment = ",".join(elements[7:])
    if 1 < len(comment):
        if comment[0] == '"':
            comment = comment[1:]
        if comment[-1] == '"':
            comment = comment[:-1]

    mkdir("output")
    if img_path == "":
        if output_name == "":
            output_name = "white_comment_" + hashlib.md5(comment.encode()).hexdigest() + ".jpg"
        elif comment == "":
            raise_value_error_and_generate_command("filepath and comment both are null.")
        new_img = create_horizontal_text_img(comment, create_font_according_img(img), width - int(MARGIN_CAPTION_RATE * width))
        new_width, new_height = new_img.size
        new_img = add_margin(new_img, new_width + int(MARGIN_CAPTION_RATE * new_width) * 2, new_height + int(MARGIN_CAPTION_RATE * new_width) * 2, "center", "center")
        new_width, new_height = new_img.size
        new_img = add_margin(new_img, new_width, new_width, "center", "top")
        if new_width < new_height:
            print("CAUTION: There are too many characters in the comment.\n")
    elif comment != "":
        img_long, img_short = max(img.size), min(img.size)
        if width != img_long or height != img_long:
            raise_value_error_and_generate_command("width and height must be \"long\" when comment is not null.")
        elif img_height <= img_width:
            if anchor_y != "top":
                raise_value_error_and_generate_command("anchor_y must be \"top\" when source image is landscape.")
            margin_caption = int(img_long * MARGIN_CAPTION_RATE)
            text_img = create_horizontal_text_img(comment, create_font_according_img(img), width - margin_caption * 2)
            text_width, text_height = text_img.size
            text_img = add_margin(text_img, text_width, text_height + int(img_long * MARGIN_BETWEEN_PICTURE_AND_CAPTION_RATE), "center", "bottom")
            text_img = add_margin(text_img, text_width + margin_caption * 2, text_height + margin_caption, "center", "top")
        elif img_width < img_height:
            if anchor_x != "left":
                raise_value_error_and_generate_command("anchor_x must be \"left\" when source image is portrait.")
            margin_caption = int(img_long * MARGIN_CAPTION_RATE)
            text_img = create_vertical_text_img(comment, create_font_according_img(img), height- margin_caption * 2, img_long - img_short - margin_caption)
            text_width, text_height = text_img.size
            text_img = add_margin(text_img, text_width + int(img_long * MARGIN_BETWEEN_PICTURE_AND_CAPTION_RATE), text_height, "right", "center")
            text_img = add_margin(text_img, text_width + margin_caption, text_height + margin_caption * 2, "left", "center")

        text_long, text_short = max(text_img.size), min(text_img.size)
        if img_long < img_short + text_short:
            rate = (img_long - text_short) / img_short
            if rate < MIN_IMG_RATE:
                rate = MIN_IMG_RATE
                print("CAUTION: There are too many characters in the comment.\n")
            img = img_shrink(img, rate)
            img_width, img_height = img.size
        if img_height <= img_width:
            img_paste_pos = ((width - img_width) // 2, 0)
            text_img_paste_pos = (0, img_height)
        elif img_width < img_height:
            img_paste_pos = (0, (height - img_height) // 2)
            text_img_paste_pos = (img_width, 0)

        new_img = Image.new(img.mode, (width, height), BG_COLOR)
        new_img.paste(img, img_paste_pos)
        new_img.paste(text_img, text_img_paste_pos)
    else:
        new_img = add_margin(img, width, height, anchor_x, anchor_y)
    new_img_width, new_img_height = new_img.size
    new_img = add_margin(new_img, new_img_width + margin * 2, new_img_height + margin * 2, "center", "center")
    new_img.save("output\\" + output_name)
    return

args = sys.argv[1:]
csv_path = args[0]
start_index = int(get_or_else(args, 1, 1)) - 1
csv_body = file_read(csv_path)
lines = csv_body.split("\n")[start_index:]
NoL = len(lines) + start_index
print()
for csv_index, line in enumerate(lines):
    csv_index += start_index
    execute_line(line)

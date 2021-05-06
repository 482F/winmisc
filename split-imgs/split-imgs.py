# encoding: utf-8

from PIL import Image, ImageDraw, ImageFont
import sys
import time
import re
import os
import pathlib
import hashlib

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
    with open(file_path, encoding = "utf-16") as f:
        return_value = f.read()
    return return_value

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
        + "COMMAND: python3 \"" + str(pathlib.Path(__file__).resolve()) + "\" \"" + str(pathlib.Path(separated_values_path).resolve()) + "\" " + str(separated_values_index + 1)
    )
    return

def trim_img(img, upper_left, lower_right):
    size = (lower_right[0] - upper_left[0], lower_right[1] - upper_left[1])
    new_img = Image.new("RGB", size, (255, 255, 255))
    new_img.paste(img, (-upper_left[0], -upper_left[1]))
    return new_img

def execute_line(line):
    """csv, tsv を一行ずつここに読み込ませて、キャプションとマージンを追加する
    """
    elements_index_dict = {}
    elements_index_dict["filepath"] = 1
    elements_index_dict["square_side"] = 2
    elements = line.split(separater)
    img_path = get_or_else(elements, elements_index_dict["filepath"], "")
    square_side = get_or_else(elements, elements_index_dict["square_side"], "left")

    if len(line) < 1 or line[0]  in ["#", '"']:
        return

    if square_side not in ["left", "right"]:
        raise_value_error_and_generate_command("square_side must be \"right\" or \"left\".")

    img = Image.open(img_path)
    img_width, img_height = img.size

    img_name = pathlib.Path(img_path)
    img_name = img_name.name.replace(img_name.suffix, "")

    left_upper_left = (0, 0)
    right_lower_right = (img_width, img_height)
    if square_side == "left":
        left_suffix = "s"
        right_suffix = "c"
        left_lower_right = (img_height, img_height)
        right_upper_left = (img_height + 1, 0)
    else:
        left_suffix = "c"
        right_suffix = "s"
        left_lower_right = (img_width - img_height - 1, img_height)
        right_upper_left = (img_width - img_height , 0)

    left_name = img_name + "_l_" + left_suffix + ".jpg"
    right_name = img_name + "_r_" + right_suffix + ".jpg"

    mkdir("split-output")

    trim_img(img, left_upper_left, left_lower_right).save("output\\" + left_name)
    trim_img(img, right_upper_left, right_lower_right).save("output\\" + right_name)
    return

args = sys.argv[1:]
separated_values_path = args[0]
start_index = int(get_or_else(args, 1, 1)) - 1
separated_values_body = file_read(separated_values_path)
separated_values_index = 0
if separated_values_path[-3:] == "csv":
    separater = ","
elif separated_values_path[-3:] == "tsv":
    separater = "	"
else:
    raise_value_error_and_generate_command("Extension of source text file must be .csv or .tsv.")
lines = separated_values_body.split("\n")[start_index:]
NoL = len(lines) + start_index
print()
for separated_values_index, line in enumerate(lines):
    separated_values_index += start_index
    execute_line(line)

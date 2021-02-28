#required: Pillow
from PIL import ImageGrab, Image
import sys
import os
import datetime

def make_name():
    d = datetime.datetime.now()
    name = "screenshot_{:04}-{:02}-{:02}_{:02}-{:02}-{:02}-{}.jpg".format(d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond)
    return name

im = ImageGrab.grabclipboard()

args = sys.argv
if (len(args) < 2):
    sys.exit(1)

target_dir = args[1]
if target_dir[-1] != "\\":
    target_dir += "\\"

if not os.path.isdir(target_dir):
    sys.exit(1)

file_name = make_name()
target_path = target_dir + file_name

if os.path.exists(target_path):
    sys.exit(1)

if im == None:
    sys.exit(1)
if (3 < len(im.split())):
    background = Image.new("RGB", im.size, (255, 255, 255))
    background.paste(im, mask=im.split()[3])
    im = background
im.save(target_path, "jpeg")

sys.exit(0)

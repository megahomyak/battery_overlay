import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path")
args = parser.parse_args()
path = args.path

full_file_name = os.path.split(args.output)[1]
trimmed_file_name = os.path.splitext(full_file_name)[0]

last_array_number = 0

def make_array(output, image):
    global last_array_number
    """
    Returns the name of the array
    """
    array = "static unsigned int "
    for pixel in image.getdata():
        red, green, blue, opacity = pixel
        for color_value in [red, green, blue, opacity]:
            f.write(str(color_value))
            f.write(",")
        f.write("\n")

IMAGES = """
struct {
    unsigned int width, height;
    unsigned char* data;
} images[] = {
    %s
}
""".strip()
IMAGES_ROW = "{%s, %s, %s}"

with open(args.output, "w", encoding="utf-8") as f:
    f.write(f"""
        struct {{
            unsigned int width, height;
            unsigned char data[];
        }} {trimmed_file_name}[] = {{
    """)
    image = Image.open(args.input)
    f.write(f"{image.width}, {image.height},\n")
    for pixel in image.getdata():
        red, green, blue, opacity = pixel
        for color_value in [red, green, blue, opacity]:
            f.write(str(color_value))
            f.write(",")
        f.write("\n")
    f.write("};")

import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output")
args = parser.parse_args()

last_image_array_number = 0
image_arrays = []
def make_image_array(image):
    """
    Returns the name of the array
    """
    global last_image_array_number
    name = f"ARR{last_image_array_number}"
    array = f"static unsigned char {name}[] = {{\n"
    last_image_array_number += 1
    for pixel in image.getdata():
        red, green, blue, opacity = pixel
        for color_value in [red, green, blue, opacity]:
            array += str(color_value)
            array += ","
        array += "\n"
    array += "};"
    image_arrays.append(array)
    return name

levels = []
with open(args.input, encoding="utf-8") as f:
    for line in f.read().splitlines():
        if not line:
            continue
        line = line.split("#")
        percentage = line[0].strip()
        input_relative_path = line[1].strip()
        actual_relative_path = os.path.join(
            os.path.split(args.input)[0],
            input_relative_path,
        )
        image = Image.open(actual_relative_path)
        if image.mode != "RGBA":
            raise Exception("only RGBA images are supported")
        array_name = make_image_array(image)
        levels.append("{{%s, %s, %s}, %s}" % (
            image.width, image.height, array_name, percentage
        ))

output = "\n\n".join(image_arrays) + "\n\n" + """
struct {
    struct {
        unsigned long width, height;
        unsigned char* bytes;
    } image;
    unsigned char percentage;
} levels[] = {
""".strip() + "\n" + "\n".join(levels) + "\n};"

with open(args.output, "w", encoding="utf-8") as f:
    f.write(output)
